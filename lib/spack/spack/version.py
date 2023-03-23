# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module implements Version and version-ish objects.  These are:

Version
  A single version of a package.
VersionRange
  A range of versions of a package.
VersionList
  A list of Versions and VersionRanges.

All of these types support the following operations, which can
be called on any of the types::

  __eq__, __ne__, __lt__, __gt__, __ge__, __le__, __hash__
  __contains__
  satisfies
  overlaps
  union
  intersection
  concrete
"""
import numbers
import os
import re
from bisect import bisect_left
from functools import wraps

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, working_dir

import spack.caches
import spack.error
import spack.paths
import spack.util.executable
import spack.util.spack_json as sjson
from spack.util.spack_yaml import syaml_dict

__all__ = ["Version", "VersionRange", "VersionList", "ver"]

# Valid version characters
VALID_VERSION = re.compile(r"^[A-Za-z0-9_.-][=A-Za-z0-9_.-]*$")

# regex for a commit version
COMMIT_VERSION = re.compile(r"^[a-f0-9]{40}$")

# regex for version segments
SEGMENT_REGEX = re.compile(r"(?:(?P<num>[0-9]+)|(?P<str>[a-zA-Z]+))(?P<sep>[_.-]*)")

# regular expression for semantic versioning
SEMVER_REGEX = re.compile(
    ".+(?P<semver>([0-9]+)[.]([0-9]+)[.]([0-9]+)"
    "(?:-([0-9A-Za-z-]+(?:[.][0-9A-Za-z-]+)*))?"
    "(?:[+][0-9A-Za-z-]+)?)"
)

# Infinity-like versions. The order in the list implies the comparison rules
infinity_versions = ["develop", "main", "master", "head", "trunk", "stable"]

iv_min_len = min(len(s) for s in infinity_versions)


def coerce_versions(a, b):
    """
    Convert both a and b to the 'greatest' type between them, in this order:
           VersionBase < GitVersion < VersionRange < VersionList
    This is used to simplify comparison operations below so that we're always
    comparing things that are of the same type.
    """
    order = (VersionBase, GitVersion, VersionRange, VersionList)
    ta, tb = type(a), type(b)

    def check_type(t):
        if t not in order:
            raise TypeError("coerce_versions cannot be called on %s" % t)

    check_type(ta)
    check_type(tb)

    if ta == tb:
        return (a, b)
    elif order.index(ta) > order.index(tb):
        if ta == GitVersion:
            return (a, GitVersion(b))
        elif ta == VersionRange:
            return (a, VersionRange(b, b))
        else:
            return (a, VersionList([b]))
    else:
        if tb == GitVersion:
            return (GitVersion(a), b)
        elif tb == VersionRange:
            return (VersionRange(a, a), b)
        else:
            return (VersionList([a]), b)


def coerced(method):
    """Decorator that ensures that argument types of a method are coerced."""

    @wraps(method)
    def coercing_method(a, b, *args, **kwargs):
        if type(a) == type(b) or a is None or b is None:
            return method(a, b, *args, **kwargs)
        else:
            ca, cb = coerce_versions(a, b)
            return getattr(ca, method.__name__)(cb, *args, **kwargs)

    return coercing_method


class VersionStrComponent(object):
    # NOTE: this is intentionally not a UserString, the abc instanceof
    #       check is slow enough to eliminate all gains
    __slots__ = ["inf_ver", "data"]

    def __init__(self, string):
        self.inf_ver = None
        self.data = string
        if len(string) >= iv_min_len:
            try:
                self.inf_ver = infinity_versions.index(string)
            except ValueError:
                pass

    def __hash__(self):
        return hash(self.data)

    def __str__(self):
        return self.data

    def __repr__(self):
        return f"VersionStrComponent('{self.data}')"

    def __eq__(self, other):
        if isinstance(other, VersionStrComponent):
            return self.data == other.data
        return self.data == other

    def __lt__(self, other):
        if isinstance(other, VersionStrComponent):
            if self.inf_ver is not None:
                if other.inf_ver is not None:
                    return self.inf_ver > other.inf_ver
                return False
            if other.inf_ver is not None:
                return True

            return self.data < other.data

        if self.inf_ver is not None:
            return False

        # Numbers are always "newer" than letters.
        # This is for consistency with RPM.  See patch
        # #60884 (and details) from bugzilla #50977 in
        # the RPM project at rpm.org.  Or look at
        # rpmvercmp.c if you want to see how this is
        # implemented there.
        if isinstance(other, int):
            return True

        if isinstance(other, str):
            return self < VersionStrComponent(other)
        # If we get here, it's an unsupported comparison

        raise ValueError("VersionStrComponent can only be compared with itself, " "int and str")

    def __gt__(self, other):
        return not self.__lt__(other)


def is_git_version(string):
    if string.startswith("git."):
        return True
    elif len(string) == 40 and COMMIT_VERSION.match(string):
        return True
    elif "=" in string:
        return True
    return False


def Version(string):  # capitalized for backwards compatibility
    if not isinstance(string, str):
        string = str(string)  # to handle VersionBase and GitVersion types

    if is_git_version(string):
        return GitVersion(string)
    return VersionBase(string)


class VersionBase(object):
    """Class to represent versions

    Versions are compared by converting to a tuple and comparing
    lexicographically.

    The most common Versions are alpha-numeric, and are parsed from strings
    such as ``2.3.0`` or ``1.2-5``. These Versions are represented by
    the tuples ``(2, 3, 0)`` and ``(1, 2, 5)`` respectively.

    Versions are split on ``.``, ``-``, and
    ``_`` characters, as well as any point at which they switch from
    numeric to alphabetical or vice-versa. For example, the version
    ``0.1.3a`` is represented by the tuple ``(0, 1, 3, 'a') and the
    version ``a-5b`` is represented by the tuple ``('a', 5, 'b')``.

    Spack versions may also be arbitrary non-numeric strings or git
    commit SHAs. The following are the full rules for comparing
    versions.

    1. If the version represents a git reference (i.e. commit, tag, branch), see GitVersions.

    2. The version is split into fields based on the delimiters ``.``,
    ``-``, and ``_``, as well as alphabetic-numeric boundaries.

    3. The following develop-like strings are greater (newer) than all
    numbers and are ordered as ``develop > main > master > head >
    trunk``.

    4. All other non-numeric versions are less than numeric versions,
    and are sorted alphabetically.

    These rules can be summarized as follows:

    ``develop > main > master > head > trunk > 999 > 0 > 'zzz' > 'a' >
    ''``

    """

    __slots__ = ["version", "separators", "string"]

    def __init__(self, string: str) -> None:
        if not isinstance(string, str):
            string = str(string)

        # preserve the original string, but trimmed.
        string = string.strip()
        self.string = string

        if string and not VALID_VERSION.match(string):
            raise ValueError("Bad characters in version string: %s" % string)

        self.separators, self.version = self._generate_separators_and_components(string)

    def _generate_separators_and_components(self, string):
        segments = SEGMENT_REGEX.findall(string)
        components = tuple(int(m[0]) if m[0] else VersionStrComponent(m[1]) for m in segments)
        separators = tuple(m[2] for m in segments)
        return separators, components

    @property
    def dotted(self):
        """The dotted representation of the version.

        Example:
        >>> version = Version('1-2-3b')
        >>> version.dotted
        Version('1.2.3b')

        Returns:
            Version: The version with separator characters replaced by dots
        """
        return type(self)(self.string.replace("-", ".").replace("_", "."))

    @property
    def underscored(self):
        """The underscored representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.underscored
        Version('1_2_3b')

        Returns:
            Version: The version with separator characters replaced by
                underscores
        """
        return type(self)(self.string.replace(".", "_").replace("-", "_"))

    @property
    def dashed(self):
        """The dashed representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.dashed
        Version('1-2-3b')

        Returns:
            Version: The version with separator characters replaced by dashes
        """
        return type(self)(self.string.replace(".", "-").replace("_", "-"))

    @property
    def joined(self):
        """The joined representation of the version.

        Example:
        >>> version = Version('1.2.3b')
        >>> version.joined
        Version('123b')

        Returns:
            Version: The version with separator characters removed
        """
        return type(self)(self.string.replace(".", "").replace("-", "").replace("_", ""))

    def up_to(self, index):
        """The version up to the specified component.

        Examples:
        >>> version = Version('1.23-4b')
        >>> version.up_to(1)
        Version('1')
        >>> version.up_to(2)
        Version('1.23')
        >>> version.up_to(3)
        Version('1.23-4')
        >>> version.up_to(4)
        Version('1.23-4b')
        >>> version.up_to(-1)
        Version('1.23-4')
        >>> version.up_to(-2)
        Version('1.23')
        >>> version.up_to(-3)
        Version('1')

        Returns:
            Version: The first index components of the version
        """
        return self[:index]

    def lowest(self):
        return self

    def highest(self):
        return self

    def isdevelop(self):
        """Triggers on the special case of the `@develop-like` version."""
        for inf in infinity_versions:
            for v in self.version:
                if v == inf:
                    return True

        return False

    @coerced
    def intersects(self, other: "VersionBase") -> bool:
        """Return True if self intersects with other, False otherwise.

        Two versions intersect if one can be constrained by the other. For instance
        @4.7 and @4.7.3 intersect (the intersection being @4.7.3).

        Arg:
            other: version to be checked for intersection
        """
        n = min(len(self.version), len(other.version))
        return self.version[:n] == other.version[:n]

    @coerced
    def satisfies(self, other: "VersionBase") -> bool:
        """Return True if self is at least as specific and share a common prefix with other.

        For instance, @4.7.3 satisfies @4.7 but not vice-versa.

        Arg:
            other: version to be checked for intersection
        """
        nself = len(self.version)
        nother = len(other.version)
        return nother <= nself and self.version[:nother] == other.version

    def __iter__(self):
        return iter(self.version)

    def __len__(self):
        return len(self.version)

    def __getitem__(self, idx):
        cls = type(self)

        if isinstance(idx, numbers.Integral):
            return self.version[idx]

        elif isinstance(idx, slice):
            string_arg = []

            pairs = zip(self.version[idx], self.separators[idx])
            for token, sep in pairs:
                string_arg.append(str(token))
                string_arg.append(str(sep))

            if string_arg:
                string_arg.pop()  # We don't need the last separator
                string_arg = "".join(string_arg)
                return cls(string_arg)
            else:
                return VersionBase("")

        message = "{cls.__name__} indices must be integers"
        raise TypeError(message.format(cls=cls))

    def __repr__(self):
        return "VersionBase(" + repr(self.string) + ")"

    def __str__(self):
        return self.string

    def __format__(self, format_spec):
        return str(self).format(format_spec)

    @property
    def concrete(self):
        return self

    @coerced
    def __lt__(self, other):
        """Version comparison is designed for consistency with the way RPM
        does things.  If you need more complicated versions in installed
        packages, you should override your package's version string to
        express it more sensibly.
        """
        if other is None:
            return False

        # Use tuple comparison assisted by VersionStrComponent for performance
        return self.version < other.version

    @coerced
    def __eq__(self, other):
        # Cut out early if we don't have a version
        if other is None or type(other) != VersionBase:
            return False

        return self.version == other.version

    @coerced
    def __ne__(self, other):
        return not (self == other)

    @coerced
    def __le__(self, other):
        return self == other or self < other

    @coerced
    def __ge__(self, other):
        return not (self < other)

    @coerced
    def __gt__(self, other):
        return not (self == other) and not (self < other)

    def __hash__(self):
        return hash(self.version)

    @coerced
    def __contains__(self, other):
        if other is None:
            return False

        return other.version[: len(self.version)] == self.version

    @coerced
    def is_predecessor(self, other):
        """True if the other version is the immediate predecessor of this one.
        That is, NO non-git versions v exist such that:
        (self < v < other and v not in self).
        """
        if self.version[:-1] != other.version[:-1]:
            return False

        sl = self.version[-1]
        ol = other.version[-1]
        # TODO: extend this to consecutive letters, z/0, and infinity versions
        return type(sl) == int and type(ol) == int and (ol - sl == 1)

    @coerced
    def is_successor(self, other):
        return other.is_predecessor(self)

    def overlaps(self, other):
        return self.intersects(other)

    @coerced
    def union(self, other):
        if self == other or other in self:
            return self
        elif self in other:
            return other
        else:
            return VersionList([self, other])

    @coerced
    def intersection(self, other):
        if self in other:  # also covers `self == other`
            return self
        elif other in self:
            return other
        else:
            return VersionList()


class GitVersion(VersionBase):
    """Class to represent versions interpreted from git refs.

    There are two distinct categories of git versions:

    1) GitVersions instantiated with an associated reference version (e.g. 'git.foo=1.2')
    2) GitVersions requiring commit lookups

    Git ref versions that are not paired with a known version
    are handled separately from all other version comparisons.
    When Spack identifies a git ref version, it associates a
    ``CommitLookup`` object with the version. This object
    handles caching of information from the git repo. When executing
    comparisons with a git ref version, Spack queries the
    ``CommitLookup`` for the most recent version previous to this
    git ref, as well as the distance between them expressed as a number
    of commits. If the previous version is ``X.Y.Z`` and the distance
    is ``D``, the git commit version is represented by the tuple ``(X,
    Y, Z, '', D)``. The component ``''`` cannot be parsed as part of
    any valid version, but is a valid component. This allows a git
    ref version to be less than (older than) every Version newer
    than its previous version, but still newer than its previous
    version.

    To find the previous version from a git ref version, Spack
    queries the git repo for its tags. Any tag that matches a version
    known to Spack is associated with that version, as is any tag that
    is a known version prepended with the character ``v`` (i.e., a tag
    ``v1.0`` is associated with the known version
    ``1.0``). Additionally, any tag that represents a semver version
    (X.Y.Z with X, Y, Z all integers) is associated with the version
    it represents, even if that version is not known to Spack. Each
    tag is then queried in git to see whether it is an ancestor of the
    git ref in question, and if so the distance between the two. The
    previous version is the version that is an ancestor with the least
    distance from the git ref in question.

    This procedure can be circumvented if the user supplies a known version
    to associate with the GitVersion (e.g. ``[hash]=develop``).  If the user
    prescribes the version then there is no need to do a lookup
    and the standard version comparison operations are sufficient.

    Non-git versions may be coerced to GitVersion for comparison, but no Spec will ever
    have a GitVersion that is not actually referencing a version from git."""

    def __init__(self, string):
        if not isinstance(string, str):
            string = str(string)  # In case we got a VersionBase or GitVersion object

        # An object that can lookup git refs to compare them to versions
        self.user_supplied_reference = False
        self._ref_lookup = None
        self.ref_version = None

        git_prefix = string.startswith("git.")
        pruned_string = string[4:] if git_prefix else string

        if "=" in pruned_string:
            self.ref, self.ref_version_str = pruned_string.split("=")
            _, self.ref_version = self._generate_separators_and_components(self.ref_version_str)
            self.user_supplied_reference = True
        else:
            self.ref = pruned_string

        self.is_commit = bool(len(self.ref) == 40 and COMMIT_VERSION.match(self.ref))
        self.is_ref = git_prefix  # is_ref False only for comparing to VersionBase
        self.is_ref |= bool(self.is_commit)

        # ensure git.<hash> and <hash> are treated the same by dropping 'git.'
        # unless we are assigning a version with =
        canonical_string = self.ref if (self.is_commit and not self.ref_version) else string
        super(GitVersion, self).__init__(canonical_string)

    def _cmp(self, other_lookups=None):
        # No need to rely on git comparisons for develop-like refs
        if len(self.version) == 2 and self.isdevelop():
            return self.version

        # If we've already looked this version up, return cached value
        if self.ref_version is not None:
            return self.ref_version

        ref_lookup = self.ref_lookup or other_lookups

        if self.is_ref and ref_lookup:
            ref_info = ref_lookup.get(self.ref)
            if ref_info:
                prev_version, distance = ref_info

                if prev_version is None:
                    prev_version = "0"

                # Extend previous version by empty component and distance
                # If commit is exactly a known version, no distance suffix
                prev_tuple = VersionBase(prev_version).version if prev_version else ()
                dist_suffix = (VersionStrComponent(""), distance) if distance else ()
                self.ref_version = prev_tuple + dist_suffix
                return self.ref_version

        return self.version

    @coerced
    def intersects(self, other):
        # If they are both references, they must match exactly
        if self.is_ref and other.is_ref:
            return self.version == other.version

        # Otherwise the ref_version of the reference must intersect with the version of the other
        v1 = self.ref_version if self.is_ref else self.version
        v2 = other.ref_version if other.is_ref else other.version
        n = min(len(v1), len(v2))
        return v1[:n] == v2[:n]

    @coerced
    def satisfies(self, other):
        # In the case of two GitVersions we require the ref_versions
        # to satisfy one another and the versions to be an exact match.

        self_cmp = self._cmp(other.ref_lookup)
        other_cmp = other._cmp(self.ref_lookup)

        if other.is_ref:
            # if other is a ref then satisfaction requires an exact version match
            # i.e. the GitRef must match this.version for satisfaction
            # this creates an asymmetric comparison:
            #  - 'foo@main'.satisfies('foo@git.hash=main') == False
            #  - 'foo@git.hash=main'.satisfies('foo@main') == True
            version_match = self.version == other.version
        elif self.is_ref:
            # other is not a ref then it is a version base and we need to compare
            # this.ref
            version_match = self.ref_version == other.version
        else:
            # neither is a git ref.  We shouldn't ever be here, but if we are this variable
            # is not meaningful and defaults to true
            version_match = True

        # Do the final comparison
        nself = len(self_cmp)
        nother = len(other_cmp)
        return nother <= nself and self_cmp[:nother] == other_cmp and version_match

    def __repr__(self):
        return "GitVersion(" + repr(self.string) + ")"

    @coerced
    def __lt__(self, other):
        """Version comparison is designed for consistency with the way RPM
        does things.  If you need more complicated versions in installed
        packages, you should override your package's version string to
        express it more sensibly.
        """
        if other is None:
            return False

        # If we haven't indexed yet, can't compare
        # If we called this, we know at least one is a git ref
        if not (self.ref_lookup or other.ref_lookup):
            return False

        # Use tuple comparison assisted by VersionStrComponent for performance
        return self._cmp(other.ref_lookup) < other._cmp(self.ref_lookup)

    @coerced
    def __eq__(self, other):
        # Cut out early if we don't have a git version
        if other is None or type(other) != GitVersion:
            return False

        return self._cmp(other.ref_lookup) == other._cmp(self.ref_lookup)

    def __hash__(self):
        return hash(str(self))

    @coerced
    def __contains__(self, other):
        if other is None:
            return False

        self_cmp = self._cmp(other.ref_lookup)
        return other._cmp(self.ref_lookup)[: len(self_cmp)] == self_cmp

    @coerced
    def is_predecessor(self, other):
        """True if the other version is the immediate predecessor of this one.
        That is, NO non-commit versions v exist such that:
        (self < v < other and v not in self).
        """
        self_cmp = self._cmp(self.ref_lookup)
        other_cmp = other._cmp(other.ref_lookup)

        if self_cmp[:-1] != other_cmp[:-1]:
            return False

        sl = self_cmp[-1]
        ol = other_cmp[-1]
        return type(sl) == int and type(ol) == int and (ol - sl == 1)

    @property
    def ref_lookup(self):
        if self._ref_lookup:
            # Get operation ensures dict is populated
            self._ref_lookup.get(self.ref)
            return self._ref_lookup

    def generate_git_lookup(self, pkg_name):
        """
        Use the git fetcher to look up a version for a commit.

        Since we want to optimize the clone and lookup, we do the clone once
        and store it in the user specified git repository cache. We also need
        context of the package to get known versions, which could be tags if
        they are linked to Git Releases. If we are unable to determine the
        context of the version, we cannot continue. This implementation is
        alongside the GitFetcher because eventually the git repos cache will
        be one and the same with the source cache.

        Args:
            fetcher: the fetcher to use.
            versions: the known versions of the package
        """

        # Sanity check we have a commit
        if not self.is_ref:
            tty.die("%s is not a git version." % self)

        # don't need a lookup if we already have a version assigned
        if self.ref_version:
            return

        # Generate a commit looker-upper
        self._ref_lookup = CommitLookup(pkg_name)


class VersionRange(object):
    def __init__(self, start, end):
        if isinstance(start, str):
            start = Version(start)
        if isinstance(end, str):
            end = Version(end)

        self.start = start
        self.end = end

        # Unbounded ranges are not empty
        if not start or not end:
            return

        # Do not allow empty ranges. We have to be careful about lexicographical
        # ordering of versions here: 1.2 < 1.2.3 lexicographically, but 1.2.3:1.2
        # means the range [1.2.3, 1.3), which is non-empty.
        min_len = min(len(start), len(end))
        if end.up_to(min_len) < start.up_to(min_len):
            raise ValueError(f"Invalid Version range: {self}")

    def lowest(self):
        return self.start

    def highest(self):
        return self.end

    @coerced
    def __lt__(self, other):
        """Sort VersionRanges lexicographically so that they are ordered first
        by start and then by end.  None denotes an open range, so None in
        the start position is less than everything except None, and None in
        the end position is greater than everything but None.
        """
        if other is None:
            return False

        s, o = self, other
        if s.start != o.start:
            return s.start is None or (o.start is not None and s.start < o.start)
        return s.end != o.end and o.end is None or (s.end is not None and s.end < o.end)

    @coerced
    def __eq__(self, other):
        return (
            other is not None
            and type(other) == VersionRange
            and self.start == other.start
            and self.end == other.end
        )

    @coerced
    def __ne__(self, other):
        return not (self == other)

    @coerced
    def __le__(self, other):
        return self == other or self < other

    @coerced
    def __ge__(self, other):
        return not (self < other)

    @coerced
    def __gt__(self, other):
        return not (self == other) and not (self < other)

    @property
    def concrete(self):
        return self.start if self.start == self.end else None

    @coerced
    def __contains__(self, other):
        if other is None:
            return False

        in_lower = (
            self.start == other.start
            or self.start is None
            or (
                other.start is not None and (self.start < other.start or other.start in self.start)
            )
        )
        if not in_lower:
            return False

        in_upper = (
            self.end == other.end
            or self.end is None
            or (other.end is not None and (self.end > other.end or other.end in self.end))
        )
        return in_upper

    def intersects(self, other) -> bool:
        """Return two if two version ranges overlap with each other, False otherwise.

        This is a commutative operation.

        Examples:
        - 1:3 satisfies 2:4, as their intersection is 2:3.
        - 1:2 does not satisfy 3:4, as their intersection is empty.
        - 4.5:4.7 satisfies 4.7.2:4.8, as their intersection is 4.7.2:4.7

        Args:
            other: version range to be checked for intersection
        """
        return self.overlaps(other)

    @coerced
    def satisfies(self, other):
        """A version range satisfies another if it is a subset of the other.

        Examples:
        - 1:2 does not satisfy 3:4, as their intersection is empty.
        - 1:3 does not satisfy 2:4, as they overlap but neither is a subset of the other
        - 1:3 satisfies 1:4.
        """
        return self.intersection(other) == self

    @coerced
    def overlaps(self, other):
        return (
            self.start is None
            or other.end is None
            or self.start <= other.end
            or other.end in self.start
            or self.start in other.end
        ) and (
            other.start is None
            or self.end is None
            or other.start <= self.end
            or other.start in self.end
            or self.end in other.start
        )

    @coerced
    def union(self, other):
        if not self.overlaps(other):
            if (
                self.end is not None
                and other.start is not None
                and self.end.is_predecessor(other.start)
            ):
                return VersionRange(self.start, other.end)

            if (
                other.end is not None
                and self.start is not None
                and other.end.is_predecessor(self.start)
            ):
                return VersionRange(other.start, self.end)

            return VersionList([self, other])

        # if we're here, then we know the ranges overlap.
        if self.start is None or other.start is None:
            start = None
        else:
            start = self.start
            # TODO: See note in intersection() about < and in discrepancy.
            if self.start in other.start or other.start < self.start:
                start = other.start

        if self.end is None or other.end is None:
            end = None
        else:
            end = self.end
            # TODO: See note in intersection() about < and in discrepancy.
            if other.end not in self.end:
                if end in other.end or other.end > self.end:
                    end = other.end

        return VersionRange(start, end)

    @coerced
    def intersection(self, other):
        if not self.overlaps(other):
            return VersionList()

        if self.start is None:
            start = other.start
        else:
            start = self.start
            if other.start is not None:
                if other.start > start or other.start in start:
                    start = other.start

        if self.end is None:
            end = other.end
        else:
            end = self.end
            # TODO: does this make sense?
            # This is tricky:
            #     1.6.5 in 1.6 = True  (1.6.5 is more specific)
            #     1.6 < 1.6.5  = True  (lexicographic)
            # Should 1.6 NOT be less than 1.6.5?  Hmm.
            # Here we test (not end in other.end) first to avoid paradox.
            if other.end is not None and end not in other.end:
                if other.end < end or other.end in end:
                    end = other.end

        return VersionRange(start, end)

    def __hash__(self):
        return hash((self.start, self.end))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = ""
        if self.start:
            out += str(self.start)
        out += ":"
        if self.end:
            out += str(self.end)
        return out


class VersionList(object):
    """Sorted, non-redundant list of Versions and VersionRanges."""

    def __init__(self, vlist=None):
        self.versions = []
        if vlist is not None:
            if isinstance(vlist, str):
                vlist = from_string(vlist)
                if type(vlist) == VersionList:
                    self.versions = vlist.versions
                else:
                    self.versions = [vlist]
            else:
                for v in vlist:
                    self.add(ver(v))

    def add(self, version):
        if type(version) in (VersionBase, GitVersion, VersionRange):
            # This normalizes single-value version ranges.
            if version.concrete:
                version = version.concrete

            i = bisect_left(self, version)

            while i - 1 >= 0 and version.overlaps(self[i - 1]):
                version = version.union(self[i - 1])
                del self.versions[i - 1]
                i -= 1

            while i < len(self) and version.overlaps(self[i]):
                version = version.union(self[i])
                del self.versions[i]

            self.versions.insert(i, version)

        elif type(version) == VersionList:
            for v in version:
                self.add(v)

        else:
            raise TypeError("Can't add %s to VersionList" % type(version))

    @property
    def concrete(self):
        if len(self) == 1:
            return self[0].concrete
        else:
            return None

    def copy(self):
        return VersionList(self)

    def lowest(self):
        """Get the lowest version in the list."""
        if not self:
            return None
        else:
            return self[0].lowest()

    def highest(self):
        """Get the highest version in the list."""
        if not self:
            return None
        else:
            return self[-1].highest()

    def highest_numeric(self):
        """Get the highest numeric version in the list."""
        numeric_versions = list(filter(lambda v: str(v) not in infinity_versions, self.versions))
        if not any(numeric_versions):
            return None
        else:
            return numeric_versions[-1].highest()

    def preferred(self):
        """Get the preferred (latest) version in the list."""
        latest = self.highest_numeric()
        if latest is None:
            latest = self.highest()
        return latest

    @coerced
    def overlaps(self, other):
        if not other or not self:
            return False

        s = o = 0
        while s < len(self) and o < len(other):
            if self[s].overlaps(other[o]):
                return True
            elif self[s] < other[o]:
                s += 1
            else:
                o += 1
        return False

    def intersects(self, other):
        return self.overlaps(other)

    def to_dict(self):
        """Generate human-readable dict for YAML."""
        if self.concrete:
            return syaml_dict([("version", str(self[0]))])
        else:
            return syaml_dict([("versions", [str(v) for v in self])])

    @staticmethod
    def from_dict(dictionary):
        """Parse dict from to_dict."""
        if "versions" in dictionary:
            return VersionList(dictionary["versions"])
        elif "version" in dictionary:
            return VersionList([dictionary["version"]])
        else:
            raise ValueError("Dict must have 'version' or 'versions' in it.")

    @coerced
    def satisfies(self, other) -> bool:
        # This exploits the fact that version lists are "reduced" and normalized, so we can
        # never have a list like [1:3, 2:4] since that would be normalized to [1:4]
        return all(any(lhs.satisfies(rhs) for rhs in other) for lhs in self)

    @coerced
    def update(self, other):
        for v in other.versions:
            self.add(v)

    @coerced
    def union(self, other):
        result = self.copy()
        result.update(other)
        return result

    @coerced
    def intersection(self, other):
        # TODO: make this faster.  This is O(n^2).
        result = VersionList()
        for s in self:
            for o in other:
                result.add(s.intersection(o))
        return result

    @coerced
    def intersect(self, other):
        """Intersect this spec's list with other.

        Return True if the spec changed as a result; False otherwise
        """
        isection = self.intersection(other)
        changed = isection.versions != self.versions
        self.versions = isection.versions
        return changed

    @coerced
    def __contains__(self, other):
        if len(self) == 0:
            return False

        for version in other:
            i = bisect_left(self, other)
            if i == 0:
                if version not in self[0]:
                    return False
            elif all(version not in v for v in self[i - 1 :]):
                return False

        return True

    def __getitem__(self, index):
        return self.versions[index]

    def __iter__(self):
        return iter(self.versions)

    def __reversed__(self):
        return reversed(self.versions)

    def __len__(self):
        return len(self.versions)

    def __bool__(self):
        return bool(self.versions)

    @coerced
    def __eq__(self, other):
        return other is not None and self.versions == other.versions

    @coerced
    def __ne__(self, other):
        return not (self == other)

    @coerced
    def __lt__(self, other):
        return other is not None and self.versions < other.versions

    @coerced
    def __le__(self, other):
        return self == other or self < other

    @coerced
    def __ge__(self, other):
        return not (self < other)

    @coerced
    def __gt__(self, other):
        return not (self == other) and not (self < other)

    def __hash__(self):
        return hash(tuple(self.versions))

    def __str__(self):
        return ",".join(str(v) for v in self.versions)

    def __repr__(self):
        return str(self.versions)


def from_string(string):
    """Converts a string to a Version, VersionList, or VersionRange.
    This is private.  Client code should use ver().
    """
    string = string.replace(" ", "")

    if "," in string:
        return VersionList(string.split(","))

    elif ":" in string:
        s, e = string.split(":")
        start = Version(s) if s else None
        end = Version(e) if e else None
        return VersionRange(start, end)

    else:
        return Version(string)


def ver(obj):
    """Parses a Version, VersionRange, or VersionList from a string
    or list of strings.
    """
    if isinstance(obj, (list, tuple)):
        return VersionList(obj)
    elif isinstance(obj, str):
        return from_string(obj)
    elif isinstance(obj, (int, float)):
        return from_string(str(obj))
    elif type(obj) in (VersionBase, GitVersion, VersionRange, VersionList):
        return obj
    else:
        raise TypeError("ver() can't convert %s to version!" % type(obj))


class VersionError(spack.error.SpackError):
    """This is raised when something is wrong with a version."""


class VersionChecksumError(VersionError):
    """Raised for version checksum errors."""


class VersionLookupError(VersionError):
    """Raised for errors looking up git commits as versions."""


class CommitLookup(object):
    """An object for cached lookups of git commits

    CommitLookup objects delegate to the misc_cache for locking.
    CommitLookup objects may be attached to a GitVersion object for which
    Version.is_ref returns True to allow for comparisons between git refs
    and versions as represented by tags in the git repository.
    """

    def __init__(self, pkg_name):
        self.pkg_name = pkg_name

        self.data = {}

        self._pkg = None
        self._fetcher = None
        self._cache_key = None
        self._cache_path = None

    # The following properties are used as part of a lazy reference scheme
    # to avoid querying the package repository until it is necessary (and
    # in particular to wait until after the configuration has been
    # assembled)
    @property
    def cache_key(self):
        if not self._cache_key:
            key_base = "git_metadata"
            if not self.repository_uri.startswith("/"):
                key_base += "/"
            self._cache_key = key_base + self.repository_uri

            # Cache data in misc_cache
            # If this is the first lazy access, initialize the cache as well
            spack.caches.misc_cache.init_entry(self.cache_key)
        return self._cache_key

    @property
    def cache_path(self):
        if not self._cache_path:
            self._cache_path = spack.caches.misc_cache.cache_path(self.cache_key)
        return self._cache_path

    @property
    def pkg(self):
        if not self._pkg:
            self._pkg = spack.repo.path.get_pkg_class(self.pkg_name)
        return self._pkg

    @property
    def fetcher(self):
        if not self._fetcher:
            # We require the full git repository history
            import spack.fetch_strategy  # break cycle

            fetcher = spack.fetch_strategy.GitFetchStrategy(git=self.pkg.git)
            fetcher.get_full_repo = True
            self._fetcher = fetcher
        return self._fetcher

    @property
    def repository_uri(self):
        """
        Identifier for git repos used within the repo and metadata caches.

        """
        try:
            components = [
                str(c).lstrip("/") for c in spack.util.url.parse_git_url(self.pkg.git) if c
            ]
            return os.path.join(*components)
        except ValueError:
            # If it's not a git url, it's a local path
            return os.path.abspath(self.pkg.git)

    def save(self):
        """
        Save the data to file
        """
        with spack.caches.misc_cache.write_transaction(self.cache_key) as (old, new):
            sjson.dump(self.data, new)

    def load_data(self):
        """
        Load data if the path already exists.
        """
        if os.path.isfile(self.cache_path):
            with spack.caches.misc_cache.read_transaction(self.cache_key) as cache_file:
                self.data = sjson.load(cache_file)

    def get(self, ref):
        if not self.data:
            self.load_data()

        if ref not in self.data:
            self.data[ref] = self.lookup_ref(ref)
            self.save()

        return self.data[ref]

    def lookup_ref(self, ref):
        """Lookup the previous version and distance for a given commit.

        We use git to compare the known versions from package to the git tags,
        as well as any git tags that are SEMVER versions, and find the latest
        known version prior to the commit, as well as the distance from that version
        to the commit in the git repo. Those values are used to compare Version objects.
        """
        dest = os.path.join(spack.paths.user_repos_cache_path, self.repository_uri)
        if dest.endswith(".git"):
            dest = dest[:-4]

        # prepare a cache for the repository
        dest_parent = os.path.dirname(dest)
        if not os.path.exists(dest_parent):
            mkdirp(dest_parent)

        # Only clone if we don't have it!
        if not os.path.exists(dest):
            self.fetcher.clone(dest, bare=True)

        # Lookup commit info
        with working_dir(dest):
            # TODO: we need to update the local tags if they changed on the
            # remote instance, simply adding '-f' may not be sufficient
            # (if commits are deleted on the remote, this command alone
            # won't properly update the local rev-list)
            self.fetcher.git("fetch", "--tags", output=os.devnull, error=os.devnull)

            # Ensure ref is a commit object known to git
            # Note the brackets are literals, the ref replaces the format string
            try:
                self.fetcher.git(
                    "cat-file", "-e", "%s^{commit}" % ref, output=os.devnull, error=os.devnull
                )
            except spack.util.executable.ProcessError:
                raise VersionLookupError("%s is not a valid git ref for %s" % (ref, self.pkg_name))

            # List tags (refs) by date, so last reference of a tag is newest
            tag_info = self.fetcher.git(
                "for-each-ref",
                "--sort=creatordate",
                "--format",
                "%(objectname) %(refname)",
                "refs/tags",
                output=str,
            ).split("\n")

            # Lookup of commits to spack versions
            commit_to_version = {}

            for entry in tag_info:
                if not entry:
                    continue
                tag_commit, tag = entry.split()
                tag = tag.replace("refs/tags/", "", 1)

                # For each tag, try to match to a version
                for v in [v.string for v in self.pkg.versions]:
                    if v == tag or "v" + v == tag:
                        commit_to_version[tag_commit] = v
                        break
                else:
                    # try to parse tag to copare versions spack does not know
                    match = SEMVER_REGEX.match(tag)
                    if match:
                        semver = match.groupdict()["semver"]
                        commit_to_version[tag_commit] = semver

            ancestor_commits = []
            for tag_commit in commit_to_version:
                self.fetcher.git("merge-base", "--is-ancestor", tag_commit, ref, ignore_errors=[1])
                if self.fetcher.git.returncode == 0:
                    distance = self.fetcher.git(
                        "rev-list", "%s..%s" % (tag_commit, ref), "--count", output=str, error=str
                    ).strip()
                    ancestor_commits.append((tag_commit, int(distance)))

            # Get nearest ancestor that is a known version
            ancestor_commits.sort(key=lambda x: x[1])
            if ancestor_commits:
                prev_version_commit, distance = ancestor_commits[0]
                prev_version = commit_to_version[prev_version_commit]
            else:
                # Get list of all commits, this is in reverse order
                # We use this to get the first commit below
                ref_info = self.fetcher.git("log", "--all", "--pretty=format:%H", output=str)
                commits = [c for c in ref_info.split("\n") if c]

                # No previous version and distance from first commit
                prev_version = None
                distance = int(
                    self.fetcher.git(
                        "rev-list", "%s..%s" % (commits[-1], ref), "--count", output=str, error=str
                    ).strip()
                )

        return prev_version, distance
