# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import copy
import re
from bisect import bisect_left
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

from spack.util.typing import SupportsRichComparison

from .common import (
    ALPHA,
    FINAL,
    PRERELEASE_TO_STRING,
    STRING_TO_PRERELEASE,
    EmptyRangeError,
    VersionLookupError,
    infinity_versions,
    is_git_commit_sha,
    is_git_version,
    iv_min_len,
)

# Valid version characters
VALID_VERSION = re.compile(r"^[A-Za-z0-9_.-][=A-Za-z0-9_.-]*$")

# regex for version segments
SEGMENT_REGEX = re.compile(r"(?:(?P<num>[0-9]+)|(?P<str>[a-zA-Z]+))(?P<sep>[_.-]*)")


class VersionStrComponent:
    """Internal representation of the string (non-integer) components of Spack versions.

    Versions comprise string and integer components (see ``SEGMENT_REGEX`` above).

    This represents a string component, which is either some component consisting only
    of alphabetical characters, *or* a special "infinity version" like ``main``,
    ``develop``, ``master``, etc.

    For speed, Spack versions are designed to map to Python tuples, so that we can use
    Python's fast lexicographic tuple comparison on them. ``VersionStrComponent`` is
    designed to work as a component in these version tuples, and as such must compare
    directly with ``int`` or other ``VersionStrComponent`` objects.

    """

    __slots__ = ["data"]

    data: Union[int, str]

    def __init__(self, data: Union[int, str]):
        # int for infinity index, str for literal.
        self.data = data

    @staticmethod
    def from_string(string: str) -> "VersionStrComponent":
        value: Union[int, str] = string
        if len(string) >= iv_min_len:
            try:
                value = infinity_versions.index(string)
            except ValueError:
                pass

        return VersionStrComponent(value)

    def __hash__(self) -> int:
        return hash(self.data)

    def __str__(self) -> str:
        return (
            ("infinity" if self.data >= len(infinity_versions) else infinity_versions[self.data])
            if isinstance(self.data, int)
            else self.data
        )

    def __repr__(self) -> str:
        return f'VersionStrComponent("{self}")'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VersionStrComponent) and self.data == other.data

    # ignore typing for certain parts of these methods b/c a) they are performance-critical, and
    # b) mypy isn't smart enough to figure out that if l_inf and r_inf are the same, comparing
    # self.data and other.data is type safe.
    def __lt__(self, other: object) -> bool:
        l_inf = isinstance(self.data, int)
        if isinstance(other, int):
            return not l_inf
        r_inf = isinstance(other.data, int)  # type: ignore
        return (not l_inf and r_inf) if l_inf ^ r_inf else self.data < other.data  # type: ignore

    def __gt__(self, other: object) -> bool:
        l_inf = isinstance(self.data, int)
        if isinstance(other, int):
            return l_inf
        r_inf = isinstance(other.data, int)  # type: ignore
        return (l_inf and not r_inf) if l_inf ^ r_inf else self.data > other.data  # type: ignore

    def __le__(self, other: object) -> bool:
        return self < other or self == other

    def __ge__(self, other: object) -> bool:
        return self > other or self == other


# Tuple types that make up the internal representation of StandardVersion.
# We use Tuples so that Python can quickly compare versions.

#: Version components are integers for numeric parts, VersionStrComponents for string parts.
VersionComponentTuple = Tuple[Union[int, VersionStrComponent], ...]

#: A Prerelease identifier is a constant for alpha/beta/rc/final and one optional number.
#: Most versions will have this set to ``(FINAL,)``. Prereleases will have some other
#: initial constant followed by a number, e.g. ``(RC, 1)``.
PrereleaseTuple = Tuple[int, ...]

#: Actual version tuple, including the split version number itself and the prerelease,
#: all represented as tuples.
VersionTuple = Tuple[VersionComponentTuple, PrereleaseTuple]

#: Separators from a parsed version.
SeparatorTuple = Tuple[str, ...]


def parse_string_components(string: str) -> Tuple[VersionTuple, SeparatorTuple]:
    """Parse a string into a ``VersionTuple`` and ``SeparatorTuple``."""
    string = string.strip()

    if string and not VALID_VERSION.match(string):
        raise ValueError("Bad characters in version string: %s" % string)

    segments = SEGMENT_REGEX.findall(string)
    separators: Tuple[str] = tuple([m[2] for m in segments])
    prerelease: Tuple[int, ...]

    # <version>(alpha|beta|rc)<number>
    if len(segments) >= 3 and segments[-2][1] in STRING_TO_PRERELEASE and segments[-1][0]:
        prerelease = (STRING_TO_PRERELEASE[segments[-2][1]], int(segments[-1][0]))
        segments = segments[:-2]

    # <version>(alpha|beta|rc)
    elif len(segments) >= 2 and segments[-1][1] in STRING_TO_PRERELEASE:
        prerelease = (STRING_TO_PRERELEASE[segments[-1][1]],)
        segments = segments[:-1]

    # <version>
    else:
        prerelease = (FINAL,)

    release: VersionComponentTuple = tuple(
        [int(m[0]) if m[0] else VersionStrComponent.from_string(m[1]) for m in segments]
    )

    return (release, prerelease), separators


class VersionType(SupportsRichComparison):
    """Base type for all versions in Spack (ranges, lists, regular versions, and git versions).

    Versions in Spack behave like sets, and support some basic set operations. There are
    four subclasses of ``VersionType``:

    * ``StandardVersion``: a single, concrete version, e.g. 3.4.5 or 5.4b0.
    * ``GitVersion``: subclass of ``StandardVersion`` for handling git repositories.
    * ``ClosedOpenRange``: an inclusive version range, closed or open, e.g. ``3.0:5.0``,
      ``3.0:``, or ``:5.0``
    * ``VersionList``: An ordered list of any of the above types.

    Notably, when Spack parses a version, it's always a range *unless* specified with
    ``@=`` to make it concrete.

    """

    __slots__ = ()

    def intersection(self, other: "VersionType") -> "VersionType":
        """Any versions contained in both self and other, or empty VersionList if no overlap."""
        raise NotImplementedError

    def intersects(self, other: "VersionType") -> bool:
        """Whether self and other overlap."""
        raise NotImplementedError

    def overlaps(self, other: "VersionType") -> bool:
        """Whether self and other overlap (same as ``intersects()``)."""
        return self.intersects(other)

    def satisfies(self, other: "VersionType") -> bool:
        """Whether self is entirely contained in other."""
        raise NotImplementedError

    def union(self, other: "VersionType") -> "VersionType":
        """Return a VersionType containing self and other."""
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __contains__(rhs, lhs) -> bool:
        # We should probably get rid of `x in y` for versions, since
        # versions still have a dual interpretation as singleton sets
        # or elements. x in y should be: is the lhs-element in the
        # rhs-set. Instead this function also does subset checks.
        if isinstance(lhs, VersionType):
            return lhs.satisfies(rhs)
        raise TypeError(f"'in' not supported for instances of {type(lhs)}")


class ConcreteVersion(VersionType):
    """Base type for versions that represents a single (non-range or list) version."""

    __slots__ = ()


def _stringify_version(versions: VersionTuple, separators: Tuple[str, ...]) -> str:
    """Create a string representation from version components."""
    release, prerelease = versions

    components = [f"{rel}{sep}" for rel, sep in zip(release, separators)]
    if prerelease[0] != FINAL:
        components.append(PRERELEASE_TO_STRING[prerelease[0]])
    if len(prerelease) > 1:
        components.append(separators[len(release)])
        components.append(str(prerelease[1]))

    return "".join(components)


class StandardVersion(ConcreteVersion):
    """Class to represent versions"""

    __slots__ = ("version", "_string", "separators")

    _string: str
    version: VersionTuple
    separators: Tuple[str, ...]

    def __init__(self, string: str, version: VersionTuple, separators: Tuple[str, ...]):
        """Create a StandardVersion from a string and parsed version components.

        Arguments:
            string: The original version string, or ``""``  if the it is not available.
            version: A tuple as returned by ``parse_string_components()``. Contains two tuples:
                one with alpha or numeric components and another with prerelease components.
            separators: separators parsed from the original version string.

        If constructed with ``string=""``, the string will be lazily constructed from components
        when ``str()`` is called.
        """
        self._string = string
        self.version = version
        self.separators = separators

    @staticmethod
    def from_string(string: str) -> "StandardVersion":
        version, separators = parse_string_components(string)
        return StandardVersion(string, version, separators)

    @staticmethod
    def typemin() -> "StandardVersion":
        return _STANDARD_VERSION_TYPEMIN

    @staticmethod
    def typemax() -> "StandardVersion":
        return _STANDARD_VERSION_TYPEMAX

    @property
    def string(self) -> str:
        if not self._string:
            self._string = _stringify_version(self.version, self.separators)
        return self._string

    @string.setter
    def string(self, string) -> None:
        self._string = string

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, StandardVersion):
            return self.version == other.version
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, StandardVersion):
            return self.version != other.version
        return True

    def __lt__(self, other: object) -> bool:
        if isinstance(other, StandardVersion):
            return self.version < other.version
        if isinstance(other, ClosedOpenRange):
            # Use <= here so that Version(x) < ClosedOpenRange(Version(x), ...).
            return self <= other.lo
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, StandardVersion):
            return self.version <= other.version
        if isinstance(other, ClosedOpenRange):
            # Versions are never equal to ranges, so follow < logic.
            return self <= other.lo
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, StandardVersion):
            return self.version >= other.version
        if isinstance(other, ClosedOpenRange):
            # Versions are never equal to ranges, so follow > logic.
            return self > other.lo
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, StandardVersion):
            return self.version > other.version
        if isinstance(other, ClosedOpenRange):
            return self > other.lo
        return NotImplemented

    def __iter__(self) -> Iterator:
        return iter(self.version[0])

    def __len__(self) -> int:
        return len(self.version[0])

    def __getitem__(self, idx: Union[int, slice]):
        cls = type(self)

        release = self.version[0]

        if isinstance(idx, int):
            return release[idx]

        elif isinstance(idx, slice):
            string_arg = []

            pairs = zip(release[idx], self.separators[idx])
            for token, sep in pairs:
                string_arg.append(str(token))
                string_arg.append(str(sep))

            if string_arg:
                string_arg.pop()  # We don't need the last separator
                return cls.from_string("".join(string_arg))
            else:
                return StandardVersion.from_string("")

        raise TypeError(f"{cls.__name__} indices must be integers or slices")

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        # Print indirect repr through Version(...)
        return f'Version("{str(self)}")'

    def __hash__(self) -> int:
        # If this is a final release, do not hash the prerelease part for backward compat.
        return hash(self.version if self.is_prerelease() else self.version[0])

    def intersects(self, other: VersionType) -> bool:
        if isinstance(other, StandardVersion):
            return self == other
        return other.intersects(self)

    def satisfies(self, other: VersionType) -> bool:
        if isinstance(other, VersionList):
            return other.intersects(self)

        if isinstance(other, ClosedOpenRange):
            return other.intersects(self)

        if isinstance(other, GitVersion):
            return False

        if isinstance(other, StandardVersion):
            return self == other

        raise NotImplementedError

    def union(self, other: VersionType) -> VersionType:
        if isinstance(other, StandardVersion):
            return self if self == other else VersionList([self, other])
        return other.union(self)

    def intersection(self, other: VersionType) -> VersionType:
        if isinstance(other, StandardVersion):
            return self if self == other else VersionList()
        return other.intersection(self)

    def isdevelop(self) -> bool:
        """Triggers on the special case of the ``@develop-like`` version."""
        return any(
            isinstance(p, VersionStrComponent) and isinstance(p.data, int) for p in self.version[0]
        )

    def is_prerelease(self) -> bool:
        return self.version[1][0] != FINAL

    @property
    def dotted_numeric_string(self) -> str:
        """Replaces all non-numeric components of the version with 0.

        This can be used to pass Spack versions to libraries that have stricter version schema.
        """
        numeric = tuple(0 if isinstance(v, VersionStrComponent) else v for v in self.version[0])
        if self.is_prerelease():
            numeric += (0, *self.version[1][1:])
        return ".".join(str(v) for v in numeric)

    @property
    def dotted(self) -> "StandardVersion":
        """The dotted representation of the version.

        Example:

        >>> version = Version('1-2-3b')
        >>> version.dotted
        Version('1.2.3b')

        Returns:
            Version: The version with separator characters replaced by dots
        """
        return type(self).from_string(self.string.replace("-", ".").replace("_", "."))

    @property
    def underscored(self) -> "StandardVersion":
        """The underscored representation of the version.

        Example:

        >>> version = Version("1.2.3b")
        >>> version.underscored
        Version("1_2_3b")

        Returns:
            Version: The version with separator characters replaced by underscores
        """
        return type(self).from_string(self.string.replace(".", "_").replace("-", "_"))

    @property
    def dashed(self) -> "StandardVersion":
        """The dashed representation of the version.

        Example:

        >>> version = Version("1.2.3b")
        >>> version.dashed
        Version("1-2-3b")

        Returns:
            Version: The version with separator characters replaced by dashes
        """
        return type(self).from_string(self.string.replace(".", "-").replace("_", "-"))

    @property
    def joined(self) -> "StandardVersion":
        """The joined representation of the version.

        Example:

        >>> version = Version("1.2.3b")
        >>> version.joined
        Version("123b")

        Returns:
            Version: The version with separator characters removed
        """
        return type(self).from_string(
            self.string.replace(".", "").replace("-", "").replace("_", "")
        )

    def up_to(self, index: int) -> "StandardVersion":
        """The version up to the specified component.

        Examples:

        >>> version = Version("1.23-4b")
        >>> version.up_to(1)
        Version("1")
        >>> version.up_to(2)
        Version("1.23")
        >>> version.up_to(3)
        Version("1.23-4")
        >>> version.up_to(4)
        Version("1.23-4b")
        >>> version.up_to(-1)
        Version("1.23-4")
        >>> version.up_to(-2)
        Version("1.23")
        >>> version.up_to(-3)
        Version("1")

        Returns:
            Version: The first index components of the version
        """
        return self[:index]

    @property
    def up_to_1(self):
        """The version truncated to the first component."""
        return self.up_to(1)

    @property
    def up_to_2(self):
        """The version truncated to the first two components."""
        return self.up_to(2)

    @property
    def up_to_3(self):
        """The version truncated to the first three components."""
        return self.up_to(3)


#: A git version can be mapped to a specific version, or be constrained by a version range
GitConstraint = Union[StandardVersion, "ClosedOpenRange"]


class GitVersion(ConcreteVersion):
    """Class to represent versions interpreted from git refs.

    A git version is a ref together with a constraint on the Spack version the ref stands for:

    1) ``git.foo=1.2``: the ref is assigned the version 1.2, and is concrete
    2) ``git.foo``: short for ``git.foo=:`` (unconstrained ref)
    3) ``git.foo=1.2:1.3``: the ref is constrained to the range 1.2:1.3

    Assignment queries the git repo for the most recent version previous to this git ref, as
    well as the distance between them expressed as a number of commits. If the previous
    version is ``X.Y.Z`` and the distance is ``D``, the git commit version is represented by
    the tuple ``(X, Y, Z, '', D)``. The component ``''`` cannot be parsed as part of any valid
    version, but is a valid component. This allows a git ref version to be less than (older
    than) every Version newer than its previous version, but still newer than its previous
    version.

    To find the previous version from a git ref version, Spack queries the git repo for its
    tags. Any tag that matches a version known to Spack is associated with that version, as
    is any tag that is a known version prepended with the character ``v`` (i.e., a tag
    ``v1.0`` is associated with the known version ``1.0``). Additionally, any tag that
    represents a semver version (X.Y.Z with X, Y, Z all integers) is associated with the
    version it represents, even if that version is not known to Spack. Each tag is then
    queried in git to see whether it is an ancestor of the git ref in question, and if so
    the distance between the two. The previous version is the version that is an ancestor
    with the least distance from the git ref in question.

    This procedure can be circumvented if the user supplies a known version to associate
    with the GitVersion (e.g. ``[hash]=develop``).  If the user prescribes the version then
    there is no need to do a lookup and the standard version comparison operations are
    sufficient.
    """

    __slots__ = ("has_git_prefix", "commit_sha", "ref", "is_commit", "constraint")

    def __init__(self, string: str):
        # TODO will be required for concrete specs when commit lookup added
        self.commit_sha: Optional[str] = None

        #: The Spack versions this ref is constrained to (``@:`` for unconstrained).
        self.constraint: GitConstraint

        self.has_git_prefix = string.startswith("git.")

        # Drop `git.` prefix
        normalized_string = string[4:] if self.has_git_prefix else string

        if "=" in normalized_string:
            # Store the git reference, and parse the user provided version or range.
            self.ref, constraint = normalized_string.split("=")
            if ":" in constraint:
                self.constraint = _parse_range(constraint)
            else:
                self.constraint = StandardVersion.from_string(constraint)
        else:
            self.ref = normalized_string
            self.constraint = _UNBOUNDED_RANGE

        # Used by fetcher
        self.is_commit: bool = is_git_commit_sha(self.ref)

        # translations
        if self.is_commit:
            self.commit_sha = self.ref

    def _with_constraint(self, constraint: "GitConstraint") -> "GitVersion":
        """The same ref under another constraint."""
        result = copy.copy(self)
        result.constraint = constraint
        return result

    @property
    def std_version(self) -> Optional[StandardVersion]:
        """The Spack version assigned to this ref, or None while it is only constrained."""
        return self.constraint if isinstance(self.constraint, StandardVersion) else None

    def assigned(self, version: StandardVersion) -> "GitVersion":
        """Returns a copy of this git ref with the specific version assigned. Raises a
        ``VersionLookupError`` when the version is outside the constraint on the ref."""
        if not version.satisfies(self.constraint):
            raise VersionLookupError(
                f"git ref '{self.ref}' corresponds to version {version}, "
                f"which is outside the range {self.constraint} it is constrained to"
            )
        return self._with_constraint(version)

    @property
    def ref_version(self) -> StandardVersion:
        """The Spack version assigned to this git ref, used for ordering.

        Raises a ``VersionLookupError`` when no version has been assigned yet."""
        if self.std_version is None:
            raise VersionLookupError(
                f"git ref '{self.ref}' has no Spack version assigned: "
                f"use '{self._ref_str}=<version>'"
            )
        return self.std_version

    @property
    def _ref_str(self) -> str:
        return f"git.{self.ref}" if self.has_git_prefix else self.ref

    def intersects(self, other: VersionType) -> bool:
        if isinstance(other, GitVersion):
            return self.ref == other.ref and self.constraint.intersects(other.constraint)
        if isinstance(other, StandardVersion):
            return False
        if isinstance(other, ClosedOpenRange):
            return self.constraint.intersects(other)
        if isinstance(other, VersionList):
            return any(self.intersects(rhs) for rhs in other)
        raise TypeError(f"'intersects()' not supported for instances of {type(other)}")

    def intersection(self, other: VersionType) -> VersionType:
        if isinstance(other, GitVersion):
            if self.ref != other.ref:
                return VersionList()
            constraint = self.constraint.intersection(other.constraint)
        elif isinstance(other, StandardVersion):
            return VersionList()
        elif isinstance(other, ClosedOpenRange):
            constraint = self.constraint.intersection(other)
        else:
            return other.intersection(self)
        if isinstance(constraint, (StandardVersion, ClosedOpenRange)):
            return self._with_constraint(constraint)
        return VersionList()

    def union(self, other: VersionType) -> VersionType:
        result = VersionList([self])
        result.add(other)
        return result[0] if len(result) == 1 else result

    def satisfies(self, other: VersionType) -> bool:
        if isinstance(other, GitVersion):
            return self.ref == other.ref and self.constraint.satisfies(other.constraint)
        if isinstance(other, StandardVersion):
            return False
        if isinstance(other, ClosedOpenRange):
            return self.constraint.satisfies(other)
        if isinstance(other, VersionList):
            return any(self.satisfies(rhs) for rhs in other)
        raise TypeError(f"'satisfies()' not supported for instances of {type(other)}")

    def __str__(self) -> str:
        if isinstance(self.constraint, StandardVersion):
            return f"{self._ref_str}={self.constraint}"
        if self.constraint == _UNBOUNDED_RANGE:
            return self._ref_str
        # Never collapse lo:lo to lo, which would read as an assigned version.
        constraint = str(self.constraint)
        if ":" not in constraint:
            constraint = f"{constraint}:{constraint}"
        return f"{self._ref_str}={constraint}"

    def __repr__(self):
        return f'GitVersion("{self}")'

    def __bool__(self):
        return True

    def __eq__(self, other: object) -> bool:
        # GitVersion cannot be equal to StandardVersion, otherwise == is not transitive.
        return (
            isinstance(other, GitVersion)
            and self.ref == other.ref
            and self.constraint == other.constraint
        )

    def __ne__(self, other: object) -> bool:
        return not self == other

    def _order(self, other: object) -> int:
        """The sign of ``self`` compared to ``other``, defining the storage order of versions.
        A git ref without an assigned version comes after every other version, since we
        don't know what version it will correspond to.
        """
        if isinstance(other, GitVersion):
            if self.std_version is None and other.std_version is None:
                # both constrained to a range, order by ref then constraint
                lhs_ranged = (self.ref, self.constraint)
                rhs_ranged = (other.ref, other.constraint)
                return (lhs_ranged > rhs_ranged) - (lhs_ranged < rhs_ranged)
            if self.std_version is None:
                return 1
            if other.std_version is None:
                return -1
            # both assigned, order by assigned version then ref
            lhs_assigned = (self.std_version, self.ref)
            rhs_assigned = (other.std_version, other.ref)
            return (lhs_assigned > rhs_assigned) - (lhs_assigned < rhs_assigned)
        if not isinstance(other, (StandardVersion, ClosedOpenRange)):
            raise TypeError(f"ordering not supported between {type(self)} and {type(other)}")
        if self.std_version is None:
            return 1
        # otherwise compare by assigned version
        return -1 if self.std_version < other else 1

    def __lt__(self, other: object) -> bool:
        return self._order(other) < 0

    def __le__(self, other: object) -> bool:
        return self._order(other) <= 0

    def __ge__(self, other: object) -> bool:
        return self._order(other) >= 0

    def __gt__(self, other: object) -> bool:
        return self._order(other) > 0

    def __hash__(self):
        # hashing should not cause version lookup
        return hash(self.ref)

    def __iter__(self):
        return self.ref_version.__iter__()

    def __len__(self):
        return self.ref_version.__len__()

    def __getitem__(self, idx):
        return self.ref_version.__getitem__(idx)

    def isdevelop(self):
        return self.ref_version.isdevelop()

    def is_prerelease(self) -> bool:
        return self.ref_version.is_prerelease()

    @property
    def dotted(self) -> StandardVersion:
        return self.ref_version.dotted

    @property
    def underscored(self) -> StandardVersion:
        return self.ref_version.underscored

    @property
    def dashed(self) -> StandardVersion:
        return self.ref_version.dashed

    @property
    def joined(self) -> StandardVersion:
        return self.ref_version.joined

    def up_to(self, index) -> StandardVersion:
        return self.ref_version.up_to(index)


def _str_range(lo: StandardVersion, hi: StandardVersion) -> str:
    """Create a string representation from lo:hi range."""
    if lo == _STANDARD_VERSION_TYPEMIN:
        if hi == _STANDARD_VERSION_TYPEMAX:
            return ":"
        else:
            return f":{hi}"
    elif hi == _STANDARD_VERSION_TYPEMAX:
        return f"{lo}:"
    elif lo == hi:
        return str(lo)
    else:
        return f"{lo}:{hi}"


class ClosedOpenRange(VersionType):
    __slots__ = ("lo", "hi", "_string", "_hash")

    def __init__(self, lo: StandardVersion, hi: StandardVersion):
        if hi < lo:
            raise EmptyRangeError(f"{lo}..{hi} is an empty range")
        self.lo: StandardVersion = lo
        self.hi: StandardVersion = hi
        self._string: Optional[str] = None
        self._hash: Optional[int] = None

    @classmethod
    def from_version_range(cls, lo: StandardVersion, hi: StandardVersion) -> "ClosedOpenRange":
        """Construct ClosedOpenRange from lo:hi range."""
        try:
            r = ClosedOpenRange(lo, _next_version(hi))
        except EmptyRangeError as e:
            raise EmptyRangeError(f"{lo}:{hi} is an empty range") from e

        # Cache hash and string representation
        r._hash = hash((lo, hi))
        r._string = _str_range(lo, hi)
        return r

    def __str__(self) -> str:
        if self._string:
            return self._string
        self._string = _str_range(self.lo, _prev_version(self.hi))
        return self._string

    def __repr__(self):
        return str(self)

    def __hash__(self):
        if self._hash is not None:
            return self._hash
        self._hash = hash((self.lo, _prev_version(self.hi)))
        return self._hash

    def __eq__(self, other):
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) == (other.lo, other.hi)
        if isinstance(other, StandardVersion):
            return False
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, StandardVersion):
            return True
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) != (other.lo, other.hi)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) < (other.lo, other.hi)
        if isinstance(other, StandardVersion):
            return other > self
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, StandardVersion):
            return other >= self
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) <= (other.lo, other.hi)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, StandardVersion):
            return other <= self
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) >= (other.lo, other.hi)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, StandardVersion):
            return other < self
        if isinstance(other, ClosedOpenRange):
            return (self.lo, self.hi) > (other.lo, other.hi)
        return NotImplemented

    def intersects(self, other: VersionType) -> bool:
        if isinstance(other, StandardVersion):
            return self.lo <= other < self.hi
        if isinstance(other, ClosedOpenRange):
            return (self.lo < other.hi) and (other.lo < self.hi)
        if isinstance(other, GitVersion):
            return other.intersects(self)
        if isinstance(other, VersionList):
            return any(self.intersects(rhs) for rhs in other)
        raise TypeError(f"'intersects' not supported for instances of {type(other)}")

    def satisfies(self, other: VersionType) -> bool:
        if isinstance(other, ConcreteVersion):
            return False
        if isinstance(other, ClosedOpenRange):
            return not (self.lo < other.lo or other.hi < self.hi)
        if isinstance(other, VersionList):
            return any(self.satisfies(rhs) for rhs in other)
        raise TypeError(f"'satisfies()' not supported for instances of {type(other)}")

    def _union_if_not_disjoint(self, other: VersionType) -> Optional["ClosedOpenRange"]:
        """Same as union, but returns None when the union is not connected. This function is not
        implemented for version lists as right-hand side, as that makes little sense."""
        if isinstance(other, ClosedOpenRange):
            # Notice <= cause we want union(1:2, 3:4) = 1:4.
            return (
                ClosedOpenRange(min(self.lo, other.lo), max(self.hi, other.hi))
                if self.lo <= other.hi and other.lo <= self.hi
                else None
            )

        if isinstance(other, StandardVersion):
            return self if self.lo <= other < self.hi else None

        if isinstance(other, GitVersion):
            return self if other.satisfies(self) else None

        raise TypeError(f"'union()' not supported for instances of {type(other)}")

    def union(self, other: VersionType) -> VersionType:
        if isinstance(other, VersionList):
            v = other.copy()
            v.add(self)
            return v

        result = self._union_if_not_disjoint(other)
        return result if result is not None else VersionList([self, other])

    def intersection(self, other: VersionType) -> VersionType:
        # range - version -> singleton or nothing.
        if isinstance(other, ClosedOpenRange):
            # range - range -> range or nothing.
            max_lo = max(self.lo, other.lo)
            min_hi = min(self.hi, other.hi)
            return ClosedOpenRange(max_lo, min_hi) if max_lo < min_hi else VersionList()

        if isinstance(other, GitVersion):
            return other.intersection(self)

        if isinstance(other, StandardVersion):
            return other if self.intersects(other) else VersionList()

        raise TypeError(f"'intersection()' not supported for instances of {type(other)}")


def _is_ranged_ref(v: VersionType) -> bool:
    """Whether ``v`` is a git ref constrained to a range, rather than assigned a version."""
    return isinstance(v, GitVersion) and v.std_version is None


def _element_str(v: VersionType) -> str:
    return f"={v}" if type(v) is StandardVersion else str(v)


class VersionList(VersionType):
    """Sorted, non-redundant list of Version and ClosedOpenRange elements."""

    __slots__ = ("versions",)

    versions: List[VersionType]

    def __init__(self, vlist: Optional[Union[str, VersionType, Iterable]] = None):
        if isinstance(vlist, str):
            vlist = from_string(vlist)
            if isinstance(vlist, VersionList):
                self.versions = vlist.versions
            else:
                self.versions = [vlist]

        elif vlist is None:
            self.versions = []

        elif isinstance(vlist, VersionList):
            self.versions = vlist[:]

        elif isinstance(vlist, (ConcreteVersion, ClosedOpenRange)):
            self.versions = [vlist]

        elif isinstance(vlist, Iterable):
            self.versions = []
            for v in vlist:
                self.add(ver(v))

        else:
            raise TypeError(f"Cannot construct VersionList from {type(vlist)}")

    def _ranged_refs_start(self) -> int:
        """The index where the git refs constrained to a range start: they sort last."""
        i = len(self.versions)
        while i > 0 and _is_ranged_ref(self.versions[i - 1]):
            i -= 1
        return i

    def _add_ranged_ref(self, item: GitVersion) -> None:
        """Add a git ref constrained to a range."""
        # Skip when already covered: by a plain range, or by a wider constraint on the ref.
        if item.satisfies(self):
            return
        # Widen it over the plain ranges it touches, then merge it with the constraints on the
        # same ref it touches. One pass in list order suffices: plain ranges come first and are
        # pairwise disjoint, and a constraint on the ref already contains the plain ranges it
        # touches, so merging it cannot make the result touch anything new.
        constraint = item.constraint
        assert isinstance(constraint, ClosedOpenRange)
        for v in self.versions:
            if isinstance(v, ClosedOpenRange):
                union = constraint._union_if_not_disjoint(v)
            elif isinstance(v, GitVersion) and v.ref == item.ref:
                union = constraint._union_if_not_disjoint(v.constraint)
            else:
                continue
            if union is not None:
                constraint = union
        item = item._with_constraint(constraint)
        # It covers assigned versions of the ref, and the constraints on it that were merged.
        self.versions = [v for v in self.versions if not v.satisfies(item)]
        self.versions.insert(bisect_left(self.versions, item), item)

    def add(self, item: VersionType) -> None:
        if isinstance(item, ClosedOpenRange):
            i = bisect_left(self.versions, item)

            # Note: can span multiple concrete versions to the left (as well as to the right).
            # For instance insert 1.2: into [1.2, hash=1.2, 1.3, 1.4:1.5]
            # would bisect at i = 1 and merge i = 0 too.
            while i > 0:
                union = item._union_if_not_disjoint(self[i - 1])
                if union is None:  # disjoint
                    break
                item = union
                del self.versions[i - 1]
                i -= 1

            while i < len(self):
                union = item._union_if_not_disjoint(self[i])
                if union is None:
                    break
                item = union
                del self.versions[i]

            self.versions.insert(i, item)
            # Re-add the constraints on git refs: it may cover or touch them, and they come
            # after it, not necessarily next to it.
            if _is_ranged_ref(self.versions[-1]):
                start = self._ranged_refs_start()
                refs, self.versions = self.versions[start:], self.versions[:start]
                for v in refs:
                    self.add(v)

        elif isinstance(item, VersionList):
            for v in item:
                self.add(v)

        elif _is_ranged_ref(item):
            assert isinstance(item, GitVersion)
            self._add_ranged_ref(item)

        elif isinstance(item, (StandardVersion, GitVersion)):
            # Skip when covered by a constraint on the ref, which comes after everything else.
            if isinstance(item, GitVersion) and any(
                item.satisfies(v) for v in self.versions[self._ranged_refs_start() :]
            ):
                return
            i = bisect_left(self.versions, item)
            # Only insert when prev and next do not cover it.
            if (i == 0 or not item.satisfies(self[i - 1])) and (
                i == len(self) or not item.satisfies(self[i])
            ):
                self.versions.insert(i, item)

        else:
            raise TypeError("Can't add %s to VersionList" % type(item))

    @property
    def concrete(self) -> Optional[ConcreteVersion]:
        return self[0] if len(self) == 1 and isinstance(self[0], ConcreteVersion) else None

    @property
    def concrete_range_as_version(self) -> Optional[ConcreteVersion]:
        """Like concrete, but collapses VersionRange(x, x) to Version(x).
        This is just for compatibility with old Spack."""
        if len(self) != 1:
            return None
        v = self[0]
        if isinstance(v, ConcreteVersion):
            return v
        if isinstance(v, ClosedOpenRange) and _next_version(v.lo) == v.hi:
            return v.lo
        return None

    def copy(self) -> "VersionList":
        return VersionList(self)

    def lowest(self) -> Optional[StandardVersion]:
        """Get the lowest version in the list."""
        return next((v for v in self.versions if isinstance(v, StandardVersion)), None)

    def highest(self) -> Optional[StandardVersion]:
        """Get the highest version in the list."""
        return next((v for v in reversed(self.versions) if isinstance(v, StandardVersion)), None)

    def highest_numeric(self) -> Optional[StandardVersion]:
        """Get the highest numeric version in the list."""
        numeric = (
            v
            for v in reversed(self.versions)
            if isinstance(v, StandardVersion) and not v.isdevelop()
        )
        return next(numeric, None)

    def preferred(self) -> Optional[StandardVersion]:
        """Get the preferred (latest) version in the list."""
        return self.highest_numeric() or self.highest()

    def satisfies(self, other: VersionType) -> bool:
        # This exploits the fact that version lists are "reduced" and normalized, so we can
        # never have a list like [1:3, 2:4] since that would be normalized to [1:4]
        if isinstance(other, VersionList):
            return all(any(lhs.satisfies(rhs) for rhs in other) for lhs in self)

        if isinstance(other, (ConcreteVersion, ClosedOpenRange)):
            return all(lhs.satisfies(other) for lhs in self)

        raise TypeError(f"'satisfies()' not supported for instances of {type(other)}")

    def intersects(self, other: VersionType) -> bool:
        if isinstance(other, (ClosedOpenRange, ConcreteVersion)):
            return any(v.intersects(other) for v in self)

        if isinstance(other, VersionList):
            # Walk the two lists in lockstep, up to the git refs without an assigned version
            s_tail, o_tail = self._ranged_refs_start(), other._ranged_refs_start()
            s = o = 0
            while s < s_tail and o < o_tail:
                if self[s].intersects(other[o]):
                    return True
                elif self[s] < other[o]:
                    s += 1
                else:
                    o += 1
            if s_tail == len(self.versions) and o_tail == len(other.versions):
                return False
            # Those refs can intersect elements anywhere in the other list: check them one by one
            return any(v.intersects(other) for v in self.versions[s_tail:]) or any(
                v.intersects(self) for v in other.versions[o_tail:]
            )

        raise TypeError(f"'intersects()' not supported for instances of {type(other)}")

    def to_dict(self) -> Dict:
        """Generate human-readable dict for YAML."""
        if self.concrete:
            return {"version": str(self[0])}
        return {"versions": [_element_str(v) for v in self]}

    @staticmethod
    def from_dict(dictionary) -> "VersionList":
        """Parse dict from to_dict."""
        if "versions" in dictionary:
            return VersionList(dictionary["versions"])
        elif "version" in dictionary:
            return VersionList([Version(dictionary["version"])])
        raise ValueError("Dict must have 'version' or 'versions' in it.")

    @classmethod
    def any(cls) -> "VersionList":
        """Return a VersionList that matches any version."""
        version_list = cls.__new__(cls)
        version_list.versions = [_UNBOUNDED_RANGE]
        return version_list

    def update(self, other: "VersionList") -> None:
        self.add(other)

    def union(self, other: VersionType) -> VersionType:
        result = self.copy()
        result.add(other)
        return result

    def intersection(self, other: VersionType) -> "VersionList":
        result = VersionList()
        if isinstance(other, VersionList):
            for lhs, rhs in ((self, other), (other, self)):
                lhs_tail, rhs_tail = lhs._ranged_refs_start(), rhs._ranged_refs_start()
                # Up to the git refs without an assigned version, an element meets at most its
                # two neighbors in the other list
                for x in lhs.versions[:lhs_tail]:
                    i = bisect_left(rhs.versions, x, 0, rhs_tail)
                    if i > 0:
                        result.add(rhs[i - 1].intersection(x))
                    if i < rhs_tail:
                        result.add(rhs[i].intersection(x))
                # Those refs can meet elements anywhere in the other list: meet them one by one
                for x in lhs.versions[lhs_tail:]:
                    for y in rhs.versions:
                        result.add(x.intersection(y))
            return result
        else:
            return self.intersection(VersionList(other))

    def intersect(self, other: VersionType) -> bool:
        """Intersect this spec's list with other.

        Return True if the spec changed as a result; False otherwise
        """
        isection = self.intersection(other)
        changed = isection.versions != self.versions
        self.versions = isection.versions
        return changed

    def __getitem__(self, index):
        return self.versions[index]

    def __iter__(self) -> Iterator:
        return iter(self.versions)

    def __reversed__(self) -> Iterator:
        return reversed(self.versions)

    def __len__(self) -> int:
        return len(self.versions)

    def __bool__(self) -> bool:
        return bool(self.versions)

    def __eq__(self, other) -> bool:
        if isinstance(other, VersionList):
            return self.versions == other.versions
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, VersionList):
            return self.versions != other.versions
        return False

    def __lt__(self, other) -> bool:
        if isinstance(other, VersionList):
            return self.versions < other.versions
        return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, VersionList):
            return self.versions <= other.versions
        return NotImplemented

    def __ge__(self, other) -> bool:
        if isinstance(other, VersionList):
            return self.versions >= other.versions
        return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, VersionList):
            return self.versions > other.versions
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self.versions))

    def __str__(self) -> str:
        if not self.versions:
            return ""

        return ",".join(_element_str(v) for v in self.versions)

    def __repr__(self) -> str:
        return str(self.versions)


def _next_str(s: str) -> str:
    """Produce the next string of A-Z and a-z characters"""
    return (
        (s + "A")
        if (len(s) == 0 or s[-1] == "z")
        else s[:-1] + ("a" if s[-1] == "Z" else chr(ord(s[-1]) + 1))
    )


def _prev_str(s: str) -> str:
    """Produce the previous string of A-Z and a-z characters"""
    return (
        s[:-1]
        if (len(s) == 0 or s[-1] == "A")
        else s[:-1] + ("Z" if s[-1] == "a" else chr(ord(s[-1]) - 1))
    )


def _next_version_str_component(v: VersionStrComponent) -> VersionStrComponent:
    """
    Produce the next VersionStrComponent, where
    masteq -> mastes
    master -> main
    """
    # First deal with the infinity case.
    data = v.data
    if isinstance(data, int):
        return VersionStrComponent(data + 1)

    # Find the next non-infinity string.
    while True:
        data = _next_str(data)
        if data not in infinity_versions:
            break

    return VersionStrComponent(data)


def _prev_version_str_component(v: VersionStrComponent) -> VersionStrComponent:
    """
    Produce the previous VersionStrComponent, where
    mastes -> masteq
    master -> head
    """
    # First deal with the infinity case. Allow underflows
    data = v.data
    if isinstance(data, int):
        return VersionStrComponent(data - 1)

    # Find the next string.
    while True:
        data = _prev_str(data)
        if data not in infinity_versions:
            break

    return VersionStrComponent(data)


def _next_version(v: StandardVersion) -> StandardVersion:
    release, prerelease = v.version
    separators = v.separators
    prerelease_type = prerelease[0]
    if prerelease_type != FINAL:
        prerelease = (prerelease_type, prerelease[1] + 1 if len(prerelease) > 1 else 0)
    elif len(release) == 0:
        release = (VersionStrComponent("A"),)
        separators = ("",)
    elif isinstance(release[-1], VersionStrComponent):
        release = release[:-1] + (_next_version_str_component(release[-1]),)
    else:
        release = release[:-1] + (release[-1] + 1,)

    # Avoid constructing a string here for performance. Instead, pass "" to
    # StandardVersion to lazily stringify.
    return StandardVersion("", (release, prerelease), separators)


def _prev_version(v: StandardVersion) -> StandardVersion:
    # this function does not deal with underflow, because it's always called as
    # _prev_version(_next_version(v)).
    release, prerelease = v.version
    separators = v.separators
    prerelease_type = prerelease[0]
    if prerelease_type != FINAL:
        prerelease = (
            (prerelease_type,) if prerelease[1] == 0 else (prerelease_type, prerelease[1] - 1)
        )
    elif len(release) == 0:
        return v
    elif isinstance(release[-1], VersionStrComponent):
        release = release[:-1] + (_prev_version_str_component(release[-1]),)
    else:
        release = release[:-1] + (release[-1] - 1,)

    # Avoid constructing a string here for performance. Instead, pass "" to
    # StandardVersion to lazily stringify.
    return StandardVersion("", (release, prerelease), separators)


def Version(string: Union[str, int]) -> Union[StandardVersion, GitVersion]:
    if not isinstance(string, (str, int)):
        raise TypeError(f"Cannot construct a version from {type(string)}")
    string = str(string)
    if is_git_version(string):
        return GitVersion(string)
    return StandardVersion.from_string(str(string))


def VersionRange(lo: Union[str, StandardVersion], hi: Union[str, StandardVersion]):
    lo = lo if isinstance(lo, StandardVersion) else StandardVersion.from_string(lo)
    hi = hi if isinstance(hi, StandardVersion) else StandardVersion.from_string(hi)
    return ClosedOpenRange.from_version_range(lo, hi)


def _parse_range(string: str) -> ClosedOpenRange:
    """Parse ``lo:hi``, ``lo:``, ``:hi`` or ``:`` into a range."""
    s, e = string.split(":")
    lo = _STANDARD_VERSION_TYPEMIN if s == "" else StandardVersion.from_string(s)
    hi = _STANDARD_VERSION_TYPEMAX if e == "" else StandardVersion.from_string(e)
    return VersionRange(lo, hi)


def from_string(string: str) -> VersionType:
    """Converts a string to a version object. This is private. Client code should use ver()."""
    string = string.replace(" ", "")

    # VersionList
    if "," in string:
        return VersionList([from_string(x) for x in string.split(",")])

    # StandardVersion
    elif string.startswith("="):
        # @=1.2.3 is an exact version
        return Version(string[1:])

    # GitVersion, possibly constrained to a range
    elif is_git_version(string):
        return GitVersion(string)

    # ClosedOpenRange
    elif ":" in string:
        return _parse_range(string)

    else:
        # @1.2.3 is short for 1.2.3:1.2.3
        v = StandardVersion.from_string(string)
        return VersionRange(v, v)


def ver(obj: Union[VersionType, str, list, tuple, int, float]) -> VersionType:
    """Returns a :class:`~spack.version.ClosedOpenRange`, :class:`~spack.version.StandardVersion`,
    :class:`~spack.version.GitVersion`, or :class:`~spack.version.VersionList` from the argument.
    """
    if isinstance(obj, VersionType):
        return obj
    elif isinstance(obj, str):
        return from_string(obj)
    elif isinstance(obj, (list, tuple)):
        return VersionList(obj)
    elif isinstance(obj, (int, float)):
        return from_string(str(obj))
    else:
        raise TypeError("ver() can't convert %s to version!" % type(obj))


_STANDARD_VERSION_TYPEMIN = StandardVersion("", ((), (ALPHA,)), ("",))

_STANDARD_VERSION_TYPEMAX = StandardVersion(
    "infinity", ((VersionStrComponent(len(infinity_versions)),), (FINAL,)), ("",)
)

_UNBOUNDED_RANGE = ClosedOpenRange.from_version_range(
    _STANDARD_VERSION_TYPEMIN, _STANDARD_VERSION_TYPEMAX
)
