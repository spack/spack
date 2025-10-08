# Copyright 2019-2020 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Types and functions to manage information on CPU microarchitectures."""
import functools
import platform
import re
import sys
import warnings
from typing import IO, Any, Dict, List, Optional, Set, Tuple, Union

from . import schema
from .alias import FEATURE_ALIASES
from .schema import LazyDictionary


def coerce_target_names(func):
    """Decorator that automatically converts a known target name to a proper
    Microarchitecture object.
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


class Microarchitecture:
    """A specific CPU micro-architecture"""

    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-instance-attributes
    #: Aliases for micro-architecture's features
    feature_aliases = FEATURE_ALIASES

    def __init__(
        self,
        name: str,
        parents: List["Microarchitecture"],
        vendor: str,
        features: Set[str],
        compilers: Dict[str, List[Dict[str, str]]],
        generation: int = 0,
        cpu_part: str = "",
    ):
        """
        Args:
            name: name of the micro-architecture (e.g. ``icelake``)
            parents: list of parent micro-architectures, if any. Parenthood is considered by
                cpu features and not chronologically. As such, each micro-architecture is
                compatible with its ancestors. For example, ``skylake``, which has ``broadwell``
                as a parent, supports running binaries optimized for ``broadwell``.
            vendor: vendor of the micro-architecture
            features: supported CPU flags. Note that the semantic of the flags in this field might
                vary among architectures, if at all present. For instance, x86_64 processors will
                list all the flags supported by a given CPU, while Arm processors will list instead
                only the flags that have been added on top of the base model for the current
                micro-architecture.
            compilers: compiler support to generate tuned code for this micro-architecture. This
                dictionary has as keys names of supported compilers, while values are a list of
                dictionaries with fields:

                * name: name of the micro-architecture according to the compiler. This is the name
                    passed to the ``-march`` option or similar. Not needed if it is the same as
                    ``self.name``.
                * versions: versions that support this micro-architecture.
                * flags: flags to be passed to the compiler to generate optimized code

            generation: generation of the micro-architecture, if relevant.
            cpu_part: cpu part of the architecture, if relevant.
        """
        self.name = name
        self.parents = parents
        self.vendor = vendor
        self.features = features
        self.compilers = compilers
        # Only relevant for PowerPC
        self.generation = generation
        # Only relevant for AArch64
        self.cpu_part = cpu_part

        # Cache the "ancestor" computation
        self._ancestors: Optional[List["Microarchitecture"]] = None
        # Cache the "generic" computation
        self._generic: Optional["Microarchitecture"] = None
        # Cache the "family" computation
        self._family: Optional["Microarchitecture"] = None

        # ssse3 implies sse3; on Linux sse3 is not mentioned in /proc/cpuinfo, so add it ad-hoc.
        if "ssse3" in self.features:
            self.features.add("sse3")

    @property
    def ancestors(self) -> List["Microarchitecture"]:
        """All the ancestors of this microarchitecture."""
        if self._ancestors is None:
            value = self.parents[:]
            for parent in self.parents:
                value.extend(a for a in parent.ancestors if a not in value)
            self._ancestors = value
        return self._ancestors

    def _to_set(self) -> Set[str]:
        """Returns a set of the nodes in this microarchitecture DAG."""
        # This function is used to implement subset semantics with
        # comparison operators
        return set([str(self)] + [str(x) for x in self.ancestors])

    @coerce_target_names
    def __eq__(self, other: Union[str, "Microarchitecture"]) -> bool:
        if not isinstance(other, Microarchitecture):
            return NotImplemented

        return (
            self.name == other.name
            and self.vendor == other.vendor
            and self.features == other.features
            and self.parents == other.parents  # avoid ancestors here
            and self.compilers == other.compilers
            and self.generation == other.generation
            and self.cpu_part == other.cpu_part
        )

    def __hash__(self) -> int:
        return hash(self.name)

    @coerce_target_names
    def __ne__(self, other: Union[str, "Microarchitecture"]) -> bool:
        return not self == other

    @coerce_target_names
    def __lt__(self, other: Union[str, "Microarchitecture"]) -> bool:
        if not isinstance(other, Microarchitecture):
            return NotImplemented

        return self._to_set() < other._to_set()

    @coerce_target_names
    def __le__(self, other: Union[str, "Microarchitecture"]) -> bool:
        return (self == other) or (self < other)

    @coerce_target_names
    def __gt__(self, other: Union[str, "Microarchitecture"]) -> bool:
        if not isinstance(other, Microarchitecture):
            return NotImplemented

        return self._to_set() > other._to_set()

    @coerce_target_names
    def __ge__(self, other: Union[str, "Microarchitecture"]) -> bool:
        return (self == other) or (self > other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r})"

    def __str__(self) -> str:
        return self.name

    def tree(self, fp: IO[str] = sys.stdout, indent: int = 4) -> None:
        """Format the partial order of this microarchitecture's ancestors as a tree."""
        seen: Set[str] = set()
        stack: List[Tuple[int, Microarchitecture]] = [(0, self)]
        while stack:
            level, current = stack.pop()
            print(f"{'':>{level}}{current.name}", file=fp)

            if current.name in seen:
                continue

            for parent in reversed(current.parents):
                stack.append((level + indent, parent))

    def __contains__(self, feature: str) -> bool:
        # Feature must be of a string type, so be defensive about that
        if not isinstance(feature, str):
            msg = "only objects of string types are accepted [got {0}]"
            raise TypeError(msg.format(str(type(feature))))

        # Here we look first in the raw features, and fall-back to
        # feature aliases if not match was found
        if feature in self.features:
            return True

        # Check if the alias is defined, if not it will return False
        match_alias = Microarchitecture.feature_aliases.get(feature, lambda x: False)
        return match_alias(self)

    @property
    def family(self) -> "Microarchitecture":
        """Returns the architecture family a given target belongs to"""
        if self._family is None:
            roots = [x for x in [self] + self.ancestors if not x.ancestors]
            msg = "a target is expected to belong to just one architecture family"
            msg += f"[found {', '.join(str(x) for x in roots)}]"
            assert len(roots) == 1, msg
            self._family = roots.pop()

        return self._family

    @property
    def generic(self) -> "Microarchitecture":
        """Returns the best generic architecture that is compatible with self"""
        if self._generic is None:
            generics = [x for x in [self] + self.ancestors if x.vendor == "generic"]
            self._generic = max(generics, key=lambda x: len(x.ancestors))
        return self._generic

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of this object."""
        return {
            "name": str(self.name),
            "vendor": str(self.vendor),
            "features": sorted(str(x) for x in self.features),
            "generation": self.generation,
            "parents": [str(x) for x in self.parents],
            "compilers": self.compilers,
            "cpupart": self.cpu_part,
        }

    @staticmethod
    def from_dict(data) -> "Microarchitecture":
        """Construct a microarchitecture from a dictionary representation."""
        return Microarchitecture(
            name=data["name"],
            parents=[TARGETS[x] for x in data["parents"]],
            vendor=data["vendor"],
            features=set(data["features"]),
            compilers=data.get("compilers", {}),
            generation=data.get("generation", 0),
            cpu_part=data.get("cpupart", ""),
        )

    def optimization_flags(self, compiler: str, version: str) -> str:
        """Returns a string containing the optimization flags that needs to be used to produce
        code optimized for this micro-architecture.

        The version is expected to be a string of dot-separated digits.

        If there is no information on the compiler passed as an argument, the function returns an
        empty string. If it is known that the compiler version we want to use does not support
        this architecture, the function raises an exception.

        Args:
            compiler: name of the compiler to be used
            version: version of the compiler to be used

        Raises:
            UnsupportedMicroarchitecture: if the requested compiler does not support
                this micro-architecture.
            ValueError: if the version doesn't match the expected format
        """
        # If we don't have information on compiler at all return an empty string
        if compiler not in self.family.compilers:
            return ""

        # If we have information, but it stops before this
        # microarchitecture, fall back to the best known target
        if compiler not in self.compilers:
            best_target = [x for x in self.ancestors if compiler in x.compilers][0]
            msg = (
                "'{0}' compiler is known to optimize up to the '{1}'"
                " microarchitecture in the '{2}' architecture family"
            )
            msg = msg.format(compiler, best_target, best_target.family)
            raise UnsupportedMicroarchitecture(msg)

        # Check that the version matches the expected format
        if not re.match(r"^(?:\d+\.)*\d+$", version):
            msg = (
                "invalid format for the compiler version argument. "
                "Only dot separated digits are allowed."
            )
            raise InvalidCompilerVersion(msg)

        # If we have information on this compiler we need to check the
        # version being used
        compiler_info = self.compilers[compiler]

        def satisfies_constraint(entry, version):
            min_version, max_version = entry["versions"].split(":")

            # Check version suffixes
            min_version, _ = version_components(min_version)
            max_version, _ = version_components(max_version)
            version, _ = version_components(version)

            # Assume compiler versions fit into semver
            def tuplify(ver):
                return tuple(int(y) for y in ver.split("."))

            version = tuplify(version)
            if min_version:
                min_version = tuplify(min_version)
                if min_version > version:
                    return False

            if max_version:
                max_version = tuplify(max_version)
                if max_version < version:
                    return False

            return True

        for compiler_entry in compiler_info:
            if satisfies_constraint(compiler_entry, version):
                flags_fmt = compiler_entry["flags"]
                # If there's no field name, use the name of the
                # micro-architecture
                compiler_entry.setdefault("name", self.name)

                # Check if we need to emit a warning
                warning_message = compiler_entry.get("warnings", None)
                if warning_message:
                    warnings.warn(warning_message)

                flags = flags_fmt.format(**compiler_entry)
                return flags

        msg = "cannot produce optimized binary for micro-architecture '{0}' with {1}@{2}"
        if compiler_info:
            versions = [x["versions"] for x in compiler_info]
            msg += f' [supported compiler versions are {", ".join(versions)}]'
        else:
            msg += " [no supported compiler versions]"
        msg = msg.format(self.name, compiler, version)
        raise UnsupportedMicroarchitecture(msg)


def generic_microarchitecture(name: str) -> Microarchitecture:
    """Returns a generic micro-architecture with no vendor and no features.

    Args:
        name: name of the micro-architecture
    """
    return Microarchitecture(name, parents=[], vendor="generic", features=set(), compilers={})


def version_components(version: str) -> Tuple[str, str]:
    """Decomposes the version passed as input in version number and
    suffix and returns them.

    If the version number or the suffix are not present, an empty
    string is returned.

    Args:
        version: version to be decomposed into its components
    """
    match = re.match(r"([\d.]*)(-?)(.*)", str(version))
    if not match:
        return "", ""

    version_number = match.group(1)
    suffix = match.group(3)

    return version_number, suffix


def _known_microarchitectures():
    """Returns a dictionary of the known micro-architectures. If the
    current host platform is unknown, add it too as a generic target.
    """

    def fill_target_from_dict(name, data, targets):
        """Recursively fills targets by adding the micro-architecture
        passed as argument and all its ancestors.

        Args:
            name (str): micro-architecture to be added to targets.
            data (dict): raw data loaded from JSON.
            targets (dict): dictionary that maps micro-architecture names
                to ``Microarchitecture`` objects
        """
        values = data[name]

        # Get direct parents of target
        parent_names = values["from"]
        for parent in parent_names:
            # Recursively fill parents so they exist before we add them
            if parent in targets:
                continue
            fill_target_from_dict(parent, data, targets)
        parents = [targets.get(parent) for parent in parent_names]

        vendor = values["vendor"]
        features = set(values["features"])
        compilers = values.get("compilers", {})
        generation = values.get("generation", 0)
        cpu_part = values.get("cpupart", "")

        targets[name] = Microarchitecture(
            name, parents, vendor, features, compilers, generation=generation, cpu_part=cpu_part
        )

    known_targets = {}
    data = schema.TARGETS_JSON["microarchitectures"]
    for name in data:
        if name in known_targets:
            # name was already brought in as ancestor to a target
            continue
        fill_target_from_dict(name, data, known_targets)

    # Add the host platform if not present
    host_platform = platform.machine()
    known_targets.setdefault(host_platform, generic_microarchitecture(host_platform))

    return known_targets


#: Dictionary of known micro-architectures
TARGETS = LazyDictionary(_known_microarchitectures)


class ArchspecError(Exception):
    """Base class for errors within archspec"""


class UnsupportedMicroarchitecture(ArchspecError, ValueError):
    """Raised if a compiler version does not support optimization for a given
    micro-architecture.
    """


class InvalidCompilerVersion(ArchspecError, ValueError):
    """Raised when an invalid format is used for compiler versions in archspec."""
