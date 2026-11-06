# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Defines the GPUMicroarch class, describing a detected GPU microarchitecture."""

# This class deliberately mirrors archspec.cpu.microarchitecture.Microarchitecture.
# Reimplementation here is to reference GPU specific targets while keeping CPU independent.
# pylint: disable=duplicate-code

import functools
import re
import warnings
from typing import Any, Dict, List, Optional, Set

from ..cpu.microarchitecture import (
    InvalidCompilerVersion,
    UnsupportedMicroarchitecture,
    version_components,
)
from ..cpu.schema import LazyDictionary
from . import schema
from .gpu import GPU


def coerce_target_names(func):
    """Decorator that automatically converts a known target name to a proper
    GPUMicroarch object, so comparisons accept strings: ``host >= "100f"``.
    """

    @functools.wraps(func)
    def _impl(self, other):
        if isinstance(other, str):
            if other not in TARGETS:
                msg = '"{0}" is not a valid target name'
                raise ValueError(msg.format(other))
            other = TARGETS[other]

        return func(self, other)

    return _impl


class GPUMicroarch:
    """Represents a GPU Microarchitecture"""

    def __init__(
        self,
        name: str = "",
        vendor: str = "",
        parents: Optional[List["GPUMicroarch"]] = None,
        compilers: Optional[Dict[str, List[Dict[str, str]]]] = None,
    ):
        """
        Args:
            name: compatibility identifier name (e.g. ``90`` for NVIDIA, ``gfx90a`` for AMD)
            vendor: name of chip manufacturer (e.g. ``nvidia``)
            parents: list of parent micro-architectures, if any. Parenthood follows binary
                compatibility, not chronology: a micro-architecture runs code built for any of
                its ancestors. For example NVIDIA ``86``, which has ``80`` as a parent, runs
                SASS compiled for ``80``.
            compilers: compiler support to generate code for this micro-architecture. Keys are
                compiler names, values are lists of dictionaries with fields:

                * versions: compiler versions that support this micro-architecture, as a
                    ``min:max`` range where either bound may be empty.
                * flags: flags to be passed to the compiler to target this micro-architecture.
                * name: optional, the micro-architecture name as the compiler spells it. Defaults
                    to ``self.name`` when formatting ``flags``.
        """
        self.name = name
        self.vendor = vendor
        self.parents: List["GPUMicroarch"] = parents or []
        self.compilers: Dict[str, List[Dict[str, str]]] = compilers or {}

        # Cache the "ancestor" computation
        self._ancestors: Optional[List["GPUMicroarch"]] = None
        # Cache the "family" computation
        self._family: Optional["GPUMicroarch"] = None

    @property
    def ancestors(self) -> List["GPUMicroarch"]:
        """All the ancestors of this microarchitecture."""
        if self._ancestors is None:
            value = self.parents[:]
            for parent in self.parents:
                value.extend(a for a in parent.ancestors if a not in value)
            self._ancestors = value
        return self._ancestors

    @property
    def family(self) -> "GPUMicroarch":
        """Returns the architecture family a given target belongs to"""
        if self._family is None:
            roots = [x for x in [self] + self.ancestors if not x.ancestors]
            msg = "a target is expected to belong to just one architecture family"
            msg += f"[found {', '.join(str(x) for x in roots)}]"
            assert len(roots) == 1, msg
            self._family = roots.pop()

        return self._family

    def _to_set(self) -> Set[str]:
        """Returns a set of the nodes in this microarchitecture DAG."""
        # This function is used to implement subset semantics with
        # comparison operators
        return set([self.name] + [x.name for x in self.ancestors])

    @coerce_target_names
    def __eq__(self, other):
        if not isinstance(other, GPUMicroarch):
            return NotImplemented
        return (
            self.name == other.name
            and self.vendor == other.vendor
            and self.parents == other.parents  # avoid ancestors here
            and self.compilers == other.compilers
        )

    @coerce_target_names
    def __ne__(self, other):
        return not self == other

    def __hash__(self) -> int:
        return hash((self.vendor, self.name))

    @coerce_target_names
    def __lt__(self, other):
        if not isinstance(other, GPUMicroarch):
            return NotImplemented
        return self._to_set() < other._to_set()

    @coerce_target_names
    def __le__(self, other):
        return (self == other) or (self < other)

    @coerce_target_names
    def __gt__(self, other):
        if not isinstance(other, GPUMicroarch):
            return NotImplemented
        return self._to_set() > other._to_set()

    @coerce_target_names
    def __ge__(self, other):
        return (self == other) or (self > other)

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{field}={value!r}" for field, value in self.to_dict().items() if value
        )
        return f"{self.__class__.__name__}({fields})"

    def __str__(self) -> str:
        return self.name

    @property
    def display_name(self) -> str:
        """What the device reports about itself, without any compiler-target suffix: the
        compute capability ``10.0`` for the ``100a`` node, ``gfx90a`` for ``gfx90a:xnack-``.

        Meant for human-readable output such as the CLI. ``name`` (and ``str()``) is the node's
        identifier in ``TARGETS`` and is what code should use.
        """
        if self.vendor == "nvidia":
            # The minor version is always a single digit, so the split is unambiguous
            digits = re.sub(r"[af]$", "", self.name)
            return f"{digits[:-1]}.{digits[-1]}"
        if self.vendor == "amd":
            return self.name.partition(":")[0]
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of this object."""
        return {
            "name": self.name,
            "vendor": self.vendor,
            "parents": [str(x.name) for x in self.parents],
            "compilers": self.compilers,
        }

    @classmethod
    def from_dict(cls, gpu_dict: Dict[str, Any]) -> "GPUMicroarch":
        """Returns a GPUMicroarch object from a raw dictionary

        Raises:
            ValueError if parent name is not a known target in TARGETS
        """
        parents = []
        for parent in gpu_dict.get("parents") or []:
            if parent not in TARGETS:
                raise ValueError(f'"{parent}" is not a valid target name')
            parents.append(TARGETS[parent])

        compilers = gpu_dict.get("compilers") or {}

        return cls(
            name=gpu_dict["name"],
            vendor=gpu_dict["vendor"],
            parents=parents,
            compilers=compilers,
        )

    def optimization_flags(self, compiler: str, version: str) -> str:
        """Returns a string containing the flags that need to be passed to ``compiler`` to
        produce code for this micro-architecture.

        The version is expected to be a string of dot-separated digits.

        If neither this micro-architecture nor any of its ancestors has information on the
        compiler passed as argument, the function returns an empty string. If it is known that
        the compiler version we want to use does not support this architecture, the function
        raises an exception.

        Args:
            compiler: name of the compiler to be used
            version: version of the compiler to be used

        Raises:
            ~archspec.cpu.microarchitecture.UnsupportedMicroarchitecture: if the requested
                compiler does not support this micro-architecture.
            ~archspec.cpu.microarchitecture.InvalidCompilerVersion: if the version doesn't
                match the expected format
        """
        if compiler not in self.compilers:
            # If an ancestor knows the compiler, support stops before this micro-architecture
            known = [x for x in self.ancestors if compiler in x.compilers]
            if not known:
                return ""
            best_target = known[0]
            msg = (
                f"'{compiler}' compiler is known to target up to the '{best_target.name}'"
                f" microarchitecture in the '{best_target.family.name}' architecture family"
            )
            raise UnsupportedMicroarchitecture(msg)

        if not re.match(r"^(?:\d+\.)*\d+$", version):
            msg = (
                "invalid format for the compiler version argument. "
                "Only dot separated digits are allowed."
            )
            raise InvalidCompilerVersion(msg)

        compiler_info = self.compilers[compiler]
        for compiler_entry in compiler_info:
            if not _satisfies_version_constraint(compiler_entry["versions"], version):
                continue

            # If there's no field name, use the name of the micro-architecture
            compiler_entry.setdefault("name", self.name)

            warning_message = compiler_entry.get("warnings", None)
            if warning_message:
                warnings.warn(warning_message)

            return compiler_entry["flags"].format(**compiler_entry)

        msg = f"cannot produce binary for micro-architecture '{self.name}'"
        msg += f" with {compiler}@{version}"
        if compiler_info:
            versions = [x["versions"] for x in compiler_info]
            msg += f' [supported compiler versions are {", ".join(versions)}]'
        else:
            msg += " [no supported compiler versions]"
        raise UnsupportedMicroarchitecture(msg)

    @classmethod
    def from_gpu(cls, gpu: GPU) -> "GPUMicroarch":
        """Returns the known micro-architecture for a detected GPU.

        The result is the matching entry of ``TARGETS``, so it carries parents, ancestors and
        compiler support. A device is placed at the most capable node for its silicon: NVIDIA
        devices resolve to their architecture-specific ``a`` target when one exists, then the
        family-specific ``f`` target, then the plain compute capability. A device whose name is
        not in ``TARGETS`` (e.g. newer than the JSON data) yields a bare node with no parents.

        Raises:
            ValueError: if the vendor is missing or unsupported, or the vendor-specific
                identifier is missing.
        """
        if not gpu.vendor:
            raise ValueError(f"Cannot construct GPUMicroarch from {gpu!r}: missing vendor")

        if gpu.vendor == "nvidia":
            if not gpu.compute_capability:
                raise ValueError(
                    f"Cannot construct GPUMicroarch from {gpu!r}: missing compute_capability"
                )
            name = gpu.compute_capability.name
            # Most specific first. ``a`` is a superset of ``f``, which is a superset of the plain
            # target; ``f`` is kept as a candidate in case a device ever has one without an ``a``.
            candidates = [name + "a", name + "f", name]

        elif gpu.vendor == "amd":
            if not gpu.gfx_target:
                raise ValueError(f"Cannot construct GPUMicroarch from {gpu!r}: missing gfx_target")
            name = gpu.gfx_target.name
            candidates = [name]

        # If vendor field is populated but unsupported (e.g. Intel for the time being)
        else:
            raise ValueError(
                f"Cannot construct GPUMicroarch from {gpu!r}: invalid vendor {gpu.vendor!r}"
            )

        for candidate in candidates:
            if candidate in TARGETS:
                return TARGETS[candidate]

        # Unknown to the JSON data: still report the device, but with no ancestry
        return cls(name=name, vendor=gpu.vendor)


def _satisfies_version_constraint(constraint: str, version: str) -> bool:
    """Returns True if ``version`` falls within the ``min:max`` range in ``constraint``.

    Either bound may be empty. Version suffixes are ignored, and versions are compared as tuples
    of integers.
    """
    min_version, max_version = constraint.split(":")

    def tuplify(ver: str):
        ver, _ = version_components(ver)
        return tuple(int(y) for y in ver.split("."))

    version_tuple = tuplify(version)
    if min_version and tuplify(min_version) > version_tuple:
        return False
    if max_version and tuplify(max_version) < version_tuple:
        return False
    return True


def _known_microarchitectures() -> Dict[str, GPUMicroarch]:
    """Returns a dictionary of the known GPU microarchitectures, keyed by name.

    Every ``from`` entry in the JSON is resolved to the corresponding object, so the returned
    nodes are connected: ancestors, family and the ordering operators all work on them.
    """

    def fill_target_from_dict(name: str, data: Dict[str, Any], targets: Dict[str, GPUMicroarch]):
        """Recursively fills targets by adding the microarchitecture passed as argument and
        all its ancestors.

        Args:
            name: micro-architecture to be added to targets.
            data: raw data loaded from JSON.
            targets: dictionary that maps micro-architecture names to ``GPUMicroarch`` objects
        """
        values = data[name]

        # Recursively fill parents so they exist before we add them
        for parent in values["from"]:
            if parent not in targets:
                fill_target_from_dict(parent, data, targets)

        targets[name] = GPUMicroarch(
            name=name,
            vendor=values["vendor"],
            parents=[targets[parent] for parent in values["from"]],
            compilers=values.get("compilers", {}),
        )

    known_targets: Dict[str, GPUMicroarch] = {}
    data = schema.TARGETS_JSON["microarchitectures"]
    for name in data:
        if name in known_targets:
            # name was already brought in as ancestor to a target
            continue
        fill_target_from_dict(name, data, known_targets)

    return known_targets


#: Dictionary of known GPU micro-architectures
TARGETS = LazyDictionary(_known_microarchitectures)
