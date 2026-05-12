# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Pre-solver rewriting of deprecated variant constraints."""

import warnings
from typing import Dict, List, Optional, Set, Tuple

import spack.error
import spack.repo
import spack.spec
from spack.enums import DeprecationReason
from spack.variant import ValueType

ReplacementsT = Dict[
    spack.spec.Spec, Tuple[DeprecationReason, Dict[str, Optional[str]], Optional[str]]
]


def rewrite_deprecated_variants(
    spec: spack.spec.Spec,
    replacements: ReplacementsT,
    provenance: str,
    errors: Optional[List[str]] = None,
) -> bool:
    """Rewrites deprecated variants in place and returns True when any change was made, False
    otherwise.

    Args:
        spec: the spec to rewrite
        replacements: a mapping from deprecated specs to replacements
        provenance: a string describing the context in which the replacement is being applied
        errors: a list to which errors are appended, or None to raise an error immediately
    """
    # Phase 1: evaluate ALL triggers against the original spec before any mutations.
    # Accumulate every change across all matching triggers so that the second trigger
    # always sees the original spec, not one already mutated by the first.
    to_remove: Dict[str, Set[ValueType]] = {}  # variant -> set of values to strip out
    to_add = {}
    to_warn = []
    to_error = []
    any_trigger_matched = False

    for trigger, (reason, mapping, message) in replacements.items():
        if not spec.satisfies(trigger):
            continue
        any_trigger_matched = True
        key_matched = False

        for key_str, value_str in mapping.items():
            key_spec = spack.spec.Spec(key_str)
            if not spec.satisfies(key_spec):
                continue
            key_matched = True
            for vname, vobj in key_spec.variants.items():
                to_remove.setdefault(vname, set()).update(vobj.values)
            before = spack.spec.Spec(f"{spec.name}{key_str}").cformat()
            if value_str is None:
                msg = f"{provenance}: {before} is deprecated with no replacement"
                if message:
                    msg += f" [{message}]"
                to_error.append(msg)
            elif value_str:
                to_add.update(spack.spec.Spec(value_str).variants)
                after = spack.spec.Spec(f"{spec.name} {value_str}").cformat()
                msg = f"{provenance}: {before} is deprecated, use {after} instead"
                if message:
                    msg += f" [{message}]"
                to_warn.append(msg)
            else:
                msg = f"{provenance}: {before} is deprecated and has been removed"
                if message:
                    msg += f" [{message}]"
                to_warn.append(msg)

        if not key_matched:
            for vname, vobj in trigger.variants.items():
                to_remove.setdefault(vname, set()).update(vobj.values)
            pkg = spack.spec.Spec(spec.name).cformat()
            msg = (
                f"{provenance}: {pkg} has a deprecated variant "
                f"(reason: {reason.value}) with no migration path for the current spec"
            )
            if message:
                msg += f" [{message}]"
            to_warn.append(msg)

    if not any_trigger_matched:
        return False

    # Phase 2: apply mutations and emit messages.
    # For each variant, remove only the matched values; delete the variant entirely
    # when no values remain (handles both boolean and multi-valued variants).
    for vname, values_to_remove in to_remove.items():
        if vname not in spec.variants:
            continue
        current = spec.variants[vname]
        remaining = tuple(v for v in current.values if v not in values_to_remove)
        if not remaining:
            del spec.variants[vname]
        else:
            current.set(*remaining)
    spec.variants.update(to_add)
    for msg in to_warn:
        warnings.warn(msg, UserWarning, stacklevel=2)
    for msg in to_error:
        if errors is not None:
            errors.append(msg)
        else:
            raise spack.error.SpackError(msg)

    return True


def apply_replacements_to_spec(
    spec, *, pkg_name: Optional[str] = None, provenance: str, errors: Optional[List[str]] = None
):
    """Rewrite deprecated variants in *spec* in place using the named package's replacements.

    Returns True when any change was made.
    When *errors* is provided, None-mapped variants append to it instead of raising.
    """
    name = pkg_name or spec.name
    if not name:
        return False
    try:
        pkg_cls = spack.repo.PATH.get_pkg_class(name)
    except spack.repo.UnknownPackageError:
        return False
    if not pkg_cls.replacements:
        return False
    return rewrite_deprecated_variants(spec, pkg_cls.replacements, provenance, errors)


def rewritten_copy(
    spec, *, pkg_name: Optional[str] = None, provenance: str, errors: Optional[List[str]] = None
):
    """Return a copy of *spec* with deprecated variants rewritten.

    Never mutates *spec*. If nothing matches, returns *spec* unchanged (no copy made).
    When *errors* is provided, None-mapped variants append to it instead of raising.
    """
    name = pkg_name or spec.name
    if not name:
        return spec
    try:
        pkg_cls = spack.repo.PATH.get_pkg_class(name)
    except spack.repo.UnknownPackageError:
        return spec
    if not pkg_cls.replacements:
        return spec
    copy = spec.copy()
    if rewrite_deprecated_variants(copy, pkg_cls.replacements, provenance, errors):
        return copy
    return spec
