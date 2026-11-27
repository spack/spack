# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Record of the environment modifications Spack applied to the user's shell.

The record is an ordered stack of units, stored in exported variables of the shell itself:

* ``SPACK_UNDO_STACK``: the keys of the units, bottom first, separated by spaces;
* ``SPACK_UNDO_U_<KIND>_<ID>``: the modifications of one unit, resolved when they were applied;
* ``SPACK_UNDO_BASE``: the value each variable touched by a Spack unit had before the first unit
  touched it (``None`` for unset);
* ``SPACK_UNDO_SEEN``: a hash of the value Spack last wrote to each of those variables.

Units and base values are stored as JSON, compressed with zlib and encoded in base64.

The value of a variable is computed by applying the units on the stack, in order, to its base
value. Undoing a unit removes it from the stack and computes the value again. Changes made to a
variable outside Spack are detected through ``SPACK_UNDO_SEEN`` and pushed on the stack as a
``user`` unit, so that they are kept when other units are removed.
"""

import base64
import binascii
import difflib
import hashlib
import os
import re
import sys
import warnings
import zlib
from typing import Callable, Dict, List, Mapping, Optional, Set, Tuple

import spack.error
import spack.util.spack_json as sjson
from spack.util.environment import (
    AppendFlagsEnv,
    AppendPath,
    DeprioritizeSystemPaths,
    EnvironmentModifications,
    PrependPath,
    PruneDuplicatePaths,
    RemoveFirstPath,
    RemoveFlagsEnv,
    RemoveLastPath,
    RemovePath,
    SetEnv,
    SetPath,
    UnsetEnv,
    deprioritize_system_paths,
    shell_assignments,
)
from spack.util.lang import dedupe
from spack.util.path import path_to_os_path

STACK_VAR = "SPACK_UNDO_STACK"
BASE_VAR = "SPACK_UNDO_BASE"
SEEN_VAR = "SPACK_UNDO_SEEN"
UNIT_VAR_PREFIX = "SPACK_UNDO_U_"

#: Kind of the units holding changes made outside Spack
USER_KIND = "user"

_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_KEY_RE = re.compile(r"[a-z]+:[A-Za-z0-9]+\Z")
_HASH_RE = re.compile(r"([0-9a-f]{16}|-)\Z")

#: Upper bound on the decompressed size of a single record variable
_MAX_DECODED_SIZE = 16 * 1024 * 1024

#: Linux refuses to exec a process with a single environment string of this size or more
_LINUX_MAX_ARG_STRLEN = 32 * 4096

#: An op is a list ``[kind, *arguments]``, so that it is stored as JSON as is
Op = list
Ops = Dict[str, List[Op]]


def _split(value: Optional[str], sep: str) -> List[str]:
    return value.split(sep) if value else []


def _same_path(entry: str):
    """Returns a predicate that is true for the non-empty entries equal to ``entry`` after
    ``os.path.normpath``."""
    key = os.path.normpath(entry)
    return lambda x: bool(x) and os.path.normpath(x) == key


def _keep_first(entries: List[str], entry: str, sep: str) -> str:
    """Joins ``entries``, keeping only the first copy of the path ``entry``."""
    same = _same_path(entry)
    # Copies of entry share the key True, every other entry gets a unique key and is kept
    return sep.join(dedupe(entries, key=lambda x: True if same(x) else object()))


def _prepend(value: Optional[str], entry: str, sep: str) -> str:
    return _keep_first([entry] + _split(value, sep), entry, sep)


def _append(value: Optional[str], entry: str, sep: str) -> str:
    return _keep_first(_split(value, sep) + [entry], entry, sep)


def _insert(
    value: Optional[str], entry: str, left: Optional[str], right: Optional[str], sep: str
) -> str:
    """Inserts ``entry`` after ``left``, else before ``right``, else at the end. A ``left`` of
    None means the front."""
    entries = _split(value, sep)
    if left is None:
        entries.insert(0, entry)
    elif left in entries:
        entries.insert(entries.index(left) + 1, entry)
    elif right in entries:
        entries.insert(entries.index(right), entry)
    else:
        entries.append(entry)
    return sep.join(entries)


def _remove(value: str, entry: str, sep: str) -> str:
    same = _same_path(entry)
    return sep.join(x for x in _split(value, sep) if not same(x))


def _remove_match(value: str, entry: str, sep: str, index: int) -> str:
    """Removes the entry at position ``index`` among those that are the same path as ``entry``
    (0 for the first, -1 for the last)."""
    entries = _split(value, sep)
    same = _same_path(entry)
    matches = [i for i, x in enumerate(entries) if same(x)]
    if matches:
        del entries[matches[index]]
    return sep.join(entries)


def _remove_first(value: str, entry: str, sep: str) -> str:
    return _remove_match(value, entry, sep, 0)


def _remove_last(value: str, entry: str, sep: str) -> str:
    return _remove_match(value, entry, sep, -1)


def _remove_copy(value: str, entry: str, nth: int, sep: str) -> str:
    """Removes the copy of ``entry`` at position ``nth``, counting from 0 and comparing strings
    exactly, or the last copy if there are fewer."""
    entries = _split(value, sep)
    positions = [i for i, x in enumerate(entries) if x == entry]
    if positions:
        del entries[positions[min(nth, len(positions) - 1)]]
    return sep.join(entries)


def _deprioritize(value: str, sep: str) -> str:
    return sep.join(deprioritize_system_paths(_split(value, sep)))


def _prune(value: str, sep: str) -> str:
    # Empty entries get a key of their own, so that they are never merged
    return sep.join(
        dedupe(_split(value, sep), key=lambda x: os.path.normpath(x) if x else object())
    )


def _append_flags(value: Optional[str], flags: str, sep: str) -> str:
    return f"{value}{sep}{flags}" if value else flags


def _remove_flags(value: Optional[str], flags: str, sep: str) -> str:
    return sep.join(f for f in _split(value, sep) if f != flags)


def _is_str(x: object) -> bool:
    return isinstance(x, str)


def _is_optional_str(x: object) -> bool:
    return x is None or isinstance(x, str)


def _is_count(x: object) -> bool:
    return type(x) is int and x >= 0


def _is_sep(x: object) -> bool:
    return isinstance(x, str) and bool(x)


_ArgChecks = Tuple[Callable[[object], bool], ...]
_ENTRY_SEP: _ArgChecks = (_is_str, _is_sep)
_SEP: _ArgChecks = (_is_sep,)

#: For each op, the checks on its arguments, used to validate ops read from the environment, and
#: the function computing the new value
_OPS: Dict[str, Tuple[_ArgChecks, Callable[..., Optional[str]]]] = {
    "set": ((_is_str,), lambda value, new: new),
    "unset": ((), lambda value: None),
    "prepend": (_ENTRY_SEP, _prepend),
    "append": (_ENTRY_SEP, _append),
    "insert": ((_is_str, _is_optional_str, _is_optional_str, _is_sep), _insert),
    "remove": (_ENTRY_SEP, _remove),
    "remove_first": (_ENTRY_SEP, _remove_first),
    "remove_last": (_ENTRY_SEP, _remove_last),
    "remove_copy": ((_is_str, _is_count, _is_sep), _remove_copy),
    "append_flags": (_ENTRY_SEP, _append_flags),
    "remove_flags": (_ENTRY_SEP, _remove_flags),
    "deprioritize": (_SEP, _deprioritize),
    "prune": (_SEP, _prune),
    "trailing_sep": (_SEP, lambda value, sep: value if value.endswith(sep) else value + sep),
}

#: Ops that only remove or reorder entries, or add a separator, so an unset variable stays unset
_KEEP_UNSET = {
    "remove",
    "remove_first",
    "remove_last",
    "remove_copy",
    "deprioritize",
    "prune",
    "trailing_sep",
}

#: Ops that leave the value unchanged when applied twice in a row
_IDEMPOTENT = {
    "set",
    "unset",
    "prepend",
    "append",
    "remove",
    "remove_flags",
    "deprioritize",
    "prune",
}

#: Ops of Spack units that split the variable into a list of paths
_PATH_OPS = {"prepend", "append", "remove", "remove_first", "remove_last", "deprioritize", "prune"}


def _apply_op(value: Optional[str], op: Op) -> Optional[str]:
    """Returns the value of a variable after applying ``op`` to ``value``, where None means unset.

    The ops of Spack units compare path entries after ``os.path.normpath``, and an entry that
    ``prepend`` or ``append`` inserts is kept only once in the variable. The ``insert`` and
    ``remove_copy`` ops of user units compare entries exactly and insert duplicates as they are.
    No op rewrites an entry it does not insert or remove, and empty entries are never merged.
    """
    kind, *args = op
    if value is None and kind in _KEEP_UNSET:
        return None
    return _OPS[kind][1](value, *args)


def _os_path(path: str) -> str:
    return path_to_os_path(os.path.normpath(path)).pop()


def ops_from_modifications(modifications: EnvironmentModifications) -> Ops:
    """Converts environment modifications to the ops of a unit, grouped by variable.

    Paths that ``prepend`` and ``append`` insert are normalized as ``PrependPath`` and
    ``AppendPath`` normalize them. Paths to remove are stored as given, and matched after
    ``os.path.normpath`` when applied. Consecutive identical ops in ``_IDEMPOTENT`` are merged.
    """
    ops: Ops = {}
    for mod in modifications:
        if isinstance(mod, (SetEnv, SetPath)):
            op: Op = ["set", mod.value]
        elif isinstance(mod, UnsetEnv):
            op = ["unset"]
        elif isinstance(mod, PrependPath):
            op = ["prepend", _os_path(mod.value), mod.separator]
        elif isinstance(mod, AppendPath):
            op = ["append", _os_path(mod.value), mod.separator]
        elif isinstance(mod, RemovePath):
            op = ["remove", mod.value, mod.separator]
        elif isinstance(mod, RemoveFirstPath):
            op = ["remove_first", mod.value, mod.separator]
        elif isinstance(mod, RemoveLastPath):
            op = ["remove_last", mod.value, mod.separator]
        elif isinstance(mod, AppendFlagsEnv):
            op = ["append_flags", mod.value, mod.separator]
        elif isinstance(mod, RemoveFlagsEnv):
            op = ["remove_flags", mod.value, mod.separator]
        elif isinstance(mod, DeprioritizeSystemPaths):
            op = ["deprioritize", mod.separator]
        elif isinstance(mod, PruneDuplicatePaths):
            op = ["prune", mod.separator]
        else:
            raise TypeError(f"cannot record environment modification {type(mod).__name__}")
        var_ops = ops.setdefault(mod.name, [])
        if op[0] not in _IDEMPOTENT or not var_ops or var_ops[-1] != op:
            var_ops.append(op)

    # The shell output of EnvironmentModifications ends MANPATH with a separator, so that man
    # also searches its default paths
    if "MANPATH" in ops:
        ops["MANPATH"].append(["trailing_sep", os.pathsep])
    return ops


class Unit:
    """A set of modifications applied to the shell in one step, and removed in one step."""

    __slots__ = ("key", "ops")

    def __init__(self, key: str, ops: Ops):
        self.key = key
        self.ops = ops

    @property
    def kind(self) -> str:
        return self.key.split(":", 1)[0]

    @property
    def is_user(self) -> bool:
        return self.kind == USER_KIND


def _unit_variable(key: str) -> str:
    """Name of the variable storing a unit, in upper case since Windows does not distinguish case
    in variable names."""
    return UNIT_VAR_PREFIX + key.replace(":", "_").upper()


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", "surrogateescape")).hexdigest()[:16]


def unit_key(kind: str, name: str) -> str:
    """Returns the key of the unit of ``kind`` identified by ``name``, which is hashed."""
    return f"{kind}:{_digest(name)}"


def _validate_ops(key: str, ops: object) -> Ops:
    if not isinstance(ops, dict):
        raise UndoRecordError(f"unit {key} has invalid ops")
    for name, var_ops in ops.items():
        if not isinstance(name, str) or not _NAME_RE.match(name) or not isinstance(var_ops, list):
            raise UndoRecordError(f"unit {key} has invalid ops for {name!r}")
        for op in var_ops:
            if not _valid_op(op):
                raise UndoRecordError(f"unit {key} has an invalid op for {name}: {op!r}")
    return ops


def _valid_op(op: object) -> bool:
    if not isinstance(op, list) or not op or not isinstance(op[0], str) or op[0] not in _OPS:
        return False
    checks, _ = _OPS[op[0]]
    return len(op) == len(checks) + 1 and all(check(arg) for check, arg in zip(checks, op[1:]))


def _encode(obj: object) -> str:
    data = sjson.dumps(obj).encode("utf-8")
    return base64.b64encode(zlib.compress(data, 9)).decode("ascii")


def _decode(data: str) -> object:
    try:
        compressed = base64.b64decode(data.encode("ascii"), validate=True)
        decompressor = zlib.decompressobj()
        raw = decompressor.decompress(compressed, _MAX_DECODED_SIZE)
        if decompressor.unconsumed_tail or not decompressor.eof:
            raise UndoRecordError("record is truncated or too large")
        return sjson.load(raw.decode("utf-8"))
    except (UnicodeError, binascii.Error, zlib.error, ValueError, RecursionError) as e:
        raise UndoRecordError(f"record cannot be decoded: {e}") from e


def _value_hash(value: Optional[str]) -> str:
    return "-" if value is None else _digest(value)


def _diff_ops(expected: Optional[str], actual: Optional[str], sep: Optional[str]) -> List[Op]:
    """Returns ops of a user unit turning ``expected`` into ``actual``.

    Path variables get entry-level ops from a diff of the two lists of entries: entries that were
    removed, and entries that were inserted with their neighbors as anchors. Other variables, and
    path variables that share no entry with the expected value, get a ``set`` or ``unset``.
    """
    if actual is None:
        return [["unset"]]
    if expected is None or sep is None:
        return [["set", actual]]

    old, new = _split(expected, sep), _split(actual, sep)
    codes = difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes()
    if not any(tag == "equal" for tag, *_ in codes):
        return [["set", actual]]
    changed = [code for code in codes if code[0] != "equal"]

    occurrence: List[int] = []
    counts: Dict[str, int] = {}
    for x in old:
        occurrence.append(counts.get(x, 0))
        counts[x] = occurrence[-1] + 1

    ops: List[Op] = []
    # Remove from the right, so that the occurrence index of earlier copies stays valid
    for _, i1, i2, _, _ in reversed(changed):
        for i in reversed(range(i1, i2)):
            ops.append(["remove_copy", old[i], occurrence[i], sep])

    # The left anchor is the previous entry, which is kept or inserted by an earlier op, and the
    # right anchor is the kept entry after the changed range, if any
    for _, _, _, j1, j2 in changed:
        right = new[j2] if j2 < len(new) else None
        for j in range(j1, j2):
            ops.append(["insert", new[j], new[j - 1] if j > 0 else None, right, sep])
    return ops


class UndoRecord:
    """The undo record of a shell environment.

    Args:
        environ: the environment of the shell, which is not modified
        units: units on the stack, bottom first
        base: value of each tracked variable before the first unit touched it
    """

    def __init__(
        self,
        environ: Mapping[str, str],
        units: Optional[List[Unit]] = None,
        base: Optional[Dict[str, Optional[str]]] = None,
    ):
        self.environ = environ
        self.units: List[Unit] = units or []
        self.base: Dict[str, Optional[str]] = base or {}

    @staticmethod
    def from_environ(environ: Mapping[str, str]) -> "UndoRecord":
        """Reads the record from ``environ``, and pushes the changes made to tracked variables
        outside Spack as a user unit. An unreadable record is treated as absent, with a warning.
        """
        try:
            record, seen = UndoRecord._read(environ)
        except UndoRecordError as e:
            warnings.warn(f"ignoring the undo record of the shell environment: {e}")
            return UndoRecord(environ)
        record._fold_edits(seen)
        return record

    @staticmethod
    def _read(environ: Mapping[str, str]) -> Tuple["UndoRecord", Dict[str, str]]:
        """Returns the record stored in ``environ``, and the hash of the value Spack last wrote to
        each tracked variable. Raises UndoRecordError if the record cannot be read."""
        keys = environ.get(STACK_VAR, "").split()
        if not keys:
            return UndoRecord(environ), {}
        units = []
        for key in keys:
            if not _KEY_RE.match(key):
                raise UndoRecordError(f"invalid unit {key!r} in {STACK_VAR}")
            data = environ.get(_unit_variable(key))
            if data is None:
                raise UndoRecordError(f"{_unit_variable(key)} is not set")
            units.append(Unit(key, _validate_ops(key, _decode(data))))
        if len({u.key for u in units}) != len(units):
            raise UndoRecordError(f"duplicate units in {STACK_VAR}")

        base = _decode(environ.get(BASE_VAR, ""))
        if not isinstance(base, dict) or not all(
            isinstance(k, str) and _NAME_RE.match(k) and (v is None or isinstance(v, str))
            for k, v in base.items()
        ):
            raise UndoRecordError(f"{BASE_VAR} has an unexpected structure")

        seen = {}
        for item in environ.get(SEEN_VAR, "").split():
            name, _, value_hash = item.rpartition(":")
            if not _NAME_RE.match(name) or not _HASH_RE.match(value_hash):
                raise UndoRecordError(f"invalid item {item!r} in {SEEN_VAR}")
            seen[name] = value_hash

        record = UndoRecord(environ, units, base)
        missing = record._spack_variables() - set(base)
        if missing:
            raise UndoRecordError(f"{BASE_VAR} has no value for {', '.join(sorted(missing))}")
        return record, seen

    def _spack_variables(self) -> Set[str]:
        return {name for u in self.units if not u.is_user for name in u.ops}

    def _separator(self, name: str) -> Optional[str]:
        """Separator of the first path op of a Spack unit on the variable, or None if there is
        no such op."""
        for unit in self.units:
            if unit.is_user:
                continue
            for op in unit.ops.get(name, ()):
                if op[0] in _PATH_OPS:
                    return op[-1]
        return None

    def value(self, name: str) -> Optional[str]:
        """Returns the value of ``name`` computed from its base and the units on the stack."""
        value = self.base.get(name)
        for unit in self.units:
            for op in unit.ops.get(name, ()):
                value = _apply_op(value, op)
        return value

    def find(self, kind: str) -> Optional[Unit]:
        """Returns the lowest unit of ``kind`` on the stack, or None."""
        return next((u for u in self.units if u.kind == kind), None)

    def remove(self, key: str) -> None:
        """Removes the unit with ``key`` from the stack, if any, so that its ops are undone."""
        self.units = [u for u in self.units if u.key != key]

    def forget(self, key: str) -> None:
        """Removes a unit that was undone outside the record. The variables keep their value: what
        differs from the remaining units is pushed as a user unit."""
        self.remove(key)
        self._fold_edits({})

    def push(self, unit: Unit) -> None:
        """Pushes a Spack unit on top of the stack, recording the base of the variables it is the
        first to touch. A unit with the same key is removed first."""
        self.remove(unit.key)
        for name in unit.ops:
            if name not in self.base:
                self.base[name] = self.environ.get(name)
        self.units.append(unit)

    def _fold_edits(self, seen: Mapping[str, str]) -> None:
        """Pushes as a user unit the difference between the value of each tracked variable and
        the value computed from the stack, skipping variables whose value has the hash in
        ``seen``."""
        for name in sorted(self.base):
            actual = self.environ.get(name)
            if seen.get(name) == _value_hash(actual):
                continue
            expected = self.value(name)
            if expected == actual:
                continue
            self._push_user_ops(name, _diff_ops(expected, actual, self._separator(name)), actual)

    def _push_user_ops(self, name: str, ops: List[Op], actual: Optional[str]) -> None:
        """Adds ops on ``name`` to the user unit on top of the stack, pushing a new user unit if
        the top is not one, so that the value of ``name`` becomes ``actual``.

        The ops stored are the first of these that gives ``actual``: the earlier user ops with
        ``ops`` appended, after cancelling removals against earlier inserts; the same without
        cancelling; a single ``set`` or ``unset``.
        """
        top = self.units[-1] if self.units else None
        if top is None or not top.is_user:
            used = {u.key for u in self.units}
            n = 1
            while f"{USER_KIND}:{n}" in used:
                n += 1
            top = Unit(f"{USER_KIND}:{n}", {})
            self.units.append(top)

        previous = top.ops.get(name, [])
        candidates = [_cancel_removals(previous, ops), previous + ops, [_assign(actual)]]
        if candidates[0] == candidates[1]:
            del candidates[1]
        for candidate in candidates:
            top.ops[name] = candidate
            if self.value(name) == actual:
                break
        if not top.ops[name]:
            del top.ops[name]
        if not top.ops:
            self.units.remove(top)

    def environment_changes(self) -> Dict[str, Optional[str]]:
        """Returns the variables to set (or unset, for None) so that the shell matches the record,
        including the record variables themselves. Variables already at their value are omitted.

        Variables no longer touched by a Spack unit are released: the record written to the shell
        has no base and no user ops for them.
        """
        new = {name: self.value(name) for name in self.base}

        tracked = self._spack_variables()
        base = {name: value for name, value in self.base.items() if name in tracked}
        units = []
        for unit in self.units:
            ops = {name: o for name, o in unit.ops.items() if name in tracked}
            if ops or not unit.is_user:
                units.append(Unit(unit.key, ops))

        for name in self.environ:
            if name.startswith(UNIT_VAR_PREFIX):
                new[name] = None
        if units:
            new[STACK_VAR] = " ".join(u.key for u in units)
            new[BASE_VAR] = _encode(base)
            new[SEEN_VAR] = " ".join(f"{n}:{_value_hash(new[n])}" for n in sorted(base))
            for unit in units:
                new[_unit_variable(unit.key)] = _encode(unit.ops)
        else:
            new[STACK_VAR] = new[BASE_VAR] = new[SEEN_VAR] = None

        return {name: value for name, value in new.items() if self.environ.get(name) != value}

    def shell_commands(self, shell: str) -> str:
        """Returns the shell code that makes the shell environment match the record. Raises
        EnvironmentTooLargeError if the new environment would be too large to start processes."""
        changes = self.environment_changes()
        check_environment_size(self.environ, changes)
        return shell_assignments(changes, shell)


def _assign(value: Optional[str]) -> Op:
    return ["unset"] if value is None else ["set", value]


def _cancel_removals(previous: List[Op], ops: List[Op]) -> List[Op]:
    """Returns ``previous`` followed by ``ops``, where each ``remove_copy`` in ``ops`` is dropped
    together with the latest ``insert`` of the same entry in ``previous``, if there is one."""
    result = list(previous)
    remaining = []
    for op in ops:
        if op[0] == "remove_copy":
            inserted = [k for k, x in enumerate(result) if x[0] == "insert" and x[1] == op[1]]
            if inserted:
                del result[inserted[-1]]
                continue
        remaining.append(op)
    return result + remaining


def apply_changes(
    environ: Mapping[str, str], changes: Mapping[str, Optional[str]]
) -> Dict[str, str]:
    """Returns a copy of ``environ`` with each variable in ``changes`` set to its value, or
    removed if the value is None."""
    result = dict(environ)
    for name, value in changes.items():
        if value is None:
            result.pop(name, None)
        else:
            result[name] = value
    return result


def check_environment_size(environ: Mapping[str, str], changes: Mapping[str, Optional[str]]):
    """Raises EnvironmentTooLargeError if applying ``changes`` would make the environment too
    large to start processes. Nothing is checked on Windows."""
    if sys.platform == "win32":
        return
    env = apply_changes(environ, changes)

    sizes: List[Tuple[int, str]] = [
        (len(f"{k}={v}".encode("utf-8", "surrogateescape")) + 1, k) for k, v in env.items()
    ]
    if sys.platform.startswith("linux"):
        largest, name = max(sizes, default=(0, ""))
        if largest >= _LINUX_MAX_ARG_STRLEN:
            raise EnvironmentTooLargeError(
                f"the shell environment was not modified: {name} would be {largest} bytes long, "
                f"and Linux cannot start processes with a variable of {_LINUX_MAX_ARG_STRLEN} "
                "bytes or more"
            )
    try:
        arg_max = os.sysconf("SC_ARG_MAX")
    except (ValueError, OSError):
        return
    pointer_size = 8
    total = sum(size + pointer_size for size, _ in sizes)
    if arg_max > 0 and total >= arg_max:
        raise EnvironmentTooLargeError(
            f"the shell environment was not modified: it would be {total} bytes long, and the "
            f"limit for starting processes is {arg_max} bytes"
        )


class UndoRecordError(spack.error.SpackError):
    """Raised when the undo record stored in the environment cannot be read."""


class EnvironmentTooLargeError(spack.error.SpackError):
    """Raised when the modified environment would not fit in the limits of the OS."""
