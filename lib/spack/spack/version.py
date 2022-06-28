# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple  # novm

from six import string_types

import llnl.util.lang as lang
import llnl.util.tty as tty

import spack.caches
import spack.error
import spack.paths
import spack.util.executable
import spack.util.spack_json as sjson
from spack.util.spack_yaml import syaml_dict

if TYPE_CHECKING:
    from spack.fetch_strategy import GitCommit, GitFetchStrategy
    from spack.package_base import PackageBase

__all__ = ['Version', 'VersionRange', 'VersionList', 'ver']

# Valid version characters
VALID_VERSION = re.compile(r'^[A-Za-z0-9_.-]+$')

# regex for a commit version
COMMIT_VERSION = re.compile(r'^[a-f0-9]{40}$')

# regex for version segments
SEGMENT_REGEX = re.compile(r'(?:(?P<num>[0-9]+)|(?P<str>[a-zA-Z]+))(?P<sep>[_.-]*)')

# regular expression for semantic versioning
SEMVER_REGEX = re.compile(".+(?P<semver>([0-9]+)[.]([0-9]+)[.]([0-9]+)"
                          "(?:-([0-9A-Za-z-]+(?:[.][0-9A-Za-z-]+)*))?"
                          "(?:[+][0-9A-Za-z-]+)?)")

# Infinity-like versions. The order in the list implies the comparison rules
infinity_versions = ['develop', 'main', 'master', 'head', 'trunk', 'stable']

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
    __slots__ = ['inf_ver', 'data']

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

        raise ValueError("VersionStrComponent can only be compared with itself, "
                         "int and str")

    def __gt__(self, other):
        return not self.__lt__(other)


def is_git_version(string):
    if string.startswith('git.'):
        return True
    elif len(string) == 40 and COMMIT_VERSION.match(string):
        return True
    return False


def Version(string):  # capitalized for backwards compatibility
    if not isinstance(string, str):
        string = str(string)  # to handle VersionBase and GitVersion types

    if is_git_version(string):
        return GitVersion(string)
    return VersionBase(string)


class VersionBase(object):
    """Class to represent versions"""
    __slots__ = [
        "version",
        "separators",
        "string",
    ]

    def __init__(self, string):
        # type: (str) -> None
        if not isinstance(string, str):
            string = str(string)

        # preserve the original string, but trimmed.
        string = string.strip()
        self.string = string

        if string and not VALID_VERSION.match(string):
            raise ValueError("Bad characters in version string: %s" % string)

        segments = SEGMENT_REGEX.findall(string)
        self.version = tuple(
            int(m[0]) if m[0] else VersionStrComponent(m[1]) for m in segments
        )
        self.separators = tuple(m[2] for m in segments)

        self.is_commit = COMMIT_VERSION.match(self.string)

    _v_prefix = re.compile(r'^v')

    def matches_regardless_of_v_prefix(self, other):
        # type: (Version) -> bool
        return (
            self._v_prefix.sub('', self.string) == self._v_prefix.sub('', other.string))

    def parse_semver(self):
        # type: () -> Optional[Version]
        match = SEMVER_REGEX.match(self.string)
        if match:
            return Version(match.groupdict()['semver'])
        return None

    def _cmp(self, other_lookups=None):
        commit_lookup = self.commit_lookup or other_lookups

        if self.is_commit and commit_lookup:
            if self.commit_version is not None:
                return self.commit_version
            commit_info = commit_lookup.get(self.string)
            if commit_info:
                prev_version, distance = commit_info

                # Extend previous version by empty component and distance
                # If commit is exactly a known version, no distance suffix
                prev_tuple = Version(prev_version).version if prev_version else ()
                dist_suffix = (VersionStrComponent(''), distance) if distance else ()
                self.commit_version = prev_tuple + dist_suffix
                return self.commit_version

        return self.version

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
        return type(self)(self.string.replace('-', '.').replace('_', '.'))

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
        return type(self)(self.string.replace('.', '_').replace('-', '_'))

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
        return type(self)(self.string.replace('.', '-').replace('_', '-'))

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
        return type(self)(
            self.string.replace('.', '').replace('-', '').replace('_', ''))

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
    def satisfies(self, other):
        """A Version 'satisfies' another if it is at least as specific and has
        a common prefix.  e.g., we want gcc@4.7.3 to satisfy a request for
        gcc@4.7 so that when a user asks to build with gcc@4.7, we can find
        a suitable compiler.
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
                string_arg = ''.join(string_arg)
                return cls(string_arg)
            else:
                return VersionBase('')

        message = '{cls.__name__} indices must be integers'
        raise TypeError(message.format(cls=cls))

    def __repr__(self):
        return 'VersionBase(' + repr(self.string) + ')'

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

        return other.version[:len(self.version)] == self.version

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

    @coerced
    def overlaps(self, other):
        return self in other or other in self

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

    Non-git versions may be coerced to GitVersion for comparison, but no Spec will ever
    have a GitVersion that is not actually referencing a version from git."""
    def __init__(self, string):
        if not isinstance(string, str):
            string = str(string)  # In case we got a VersionBase or GitVersion object

        git_prefix = string.startswith('git.')
        self.ref = string[4:] if git_prefix else string

        self.is_commit = len(self.ref) == 40 and COMMIT_VERSION.match(self.ref)
        self.is_ref = git_prefix  # is_ref False only for comparing to VersionBase
        self.is_ref |= bool(self.is_commit)

        # ensure git.<hash> and <hash> are treated the same by dropping 'git.'
        canonical_string = self.ref if self.is_commit else string
        super(GitVersion, self).__init__(canonical_string)

        # An object that can lookup git refs to compare them to versions
        self._ref_lookup = None
        self.ref_version = None

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

                # Extend previous version by empty component and distance
                # If commit is exactly a known version, no distance suffix
                prev_tuple = VersionBase(prev_version).version if prev_version else ()
                dist_suffix = (VersionStrComponent(''), distance) if distance else ()
                self.ref_version = prev_tuple + dist_suffix
                return self.ref_version

        return self.version

    @coerced
    def satisfies(self, other):
        """A Version 'satisfies' another if it is at least as specific and has
        a common prefix.  e.g., we want gcc@4.7.3 to satisfy a request for
        gcc@4.7 so that when a user asks to build with gcc@4.7, we can find
        a suitable compiler.
        """
        self_cmp = self._cmp(other.ref_lookup)
        other_cmp = other._cmp(self.ref_lookup)

        # Do the final comparison
        nself = len(self_cmp)
        nother = len(other_cmp)
        return nother <= nself and self_cmp[:nother] == other_cmp

    def __repr__(self):
        return 'GitVersion(' + repr(self.string) + ')'

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
        return other._cmp(self.ref_lookup)[:len(self_cmp)] == self_cmp

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

        # Generate a commit looker-upper
        self._ref_lookup = CommitLookup(pkg_name)


class VersionRange(object):

    def __init__(self, start, end):
        if isinstance(start, string_types):
            start = Version(start)
        if isinstance(end, string_types):
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
            raise ValueError("Invalid Version range: %s" % self)

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
            return s.start is None or (
                o.start is not None and s.start < o.start)
        return (s.end != o.end and
                o.end is None or (s.end is not None and s.end < o.end))

    @coerced
    def __eq__(self, other):
        return (other is not None and
                type(other) == VersionRange and
                self.start == other.start and self.end == other.end)

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

        in_lower = (self.start == other.start or
                    self.start is None or
                    (other.start is not None and (
                        self.start < other.start or
                        other.start in self.start)))
        if not in_lower:
            return False

        in_upper = (self.end == other.end or
                    self.end is None or
                    (other.end is not None and (
                        self.end > other.end or
                        other.end in self.end)))
        return in_upper

    @coerced
    def satisfies(self, other):
        """
        x.satisfies(y) in general means that x and y have a
        non-zero intersection. For VersionRange this means they overlap.

        `satisfies` is a commutative binary operator, meaning that
        x.satisfies(y) if and only if y.satisfies(x).

        Note: in some cases we have the keyword x.satisfies(y, strict=True)
        to mean strict set inclusion, which is not commutative. However, this
        lacks in VersionRange for unknown reasons.

        Examples
        - 1:3 satisfies 2:4, as their intersection is 2:3.
        - 1:2 does not satisfy 3:4, as their intersection is empty.
        - 4.5:4.7 satisfies 4.7.2:4.8, as their intersection is 4.7.2:4.7
        """
        return self.overlaps(other)

    @coerced
    def overlaps(self, other):
        return ((self.start is None or other.end is None or
                 self.start <= other.end or
                 other.end in self.start or self.start in other.end) and
                (other.start is None or self.end is None or
                 other.start <= self.end or
                 other.start in self.end or self.end in other.start))

    @coerced
    def union(self, other):
        if not self.overlaps(other):
            if (self.end is not None and other.start is not None and
                    self.end.is_predecessor(other.start)):
                return VersionRange(self.start, other.end)

            if (other.end is not None and self.start is not None and
                    other.end.is_predecessor(self.start)):
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
        if self.overlaps(other):
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

        else:
            return VersionList()

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
            if isinstance(vlist, string_types):
                vlist = _string_to_version(vlist)
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
        numeric_versions = list(filter(
            lambda v: str(v) not in infinity_versions,
            self.versions))
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

    def to_dict(self):
        """Generate human-readable dict for YAML."""
        if self.concrete:
            return syaml_dict([
                ('version', str(self[0]))
            ])
        else:
            return syaml_dict([
                ('versions', [str(v) for v in self])
            ])

    @staticmethod
    def from_dict(dictionary):
        """Parse dict from to_dict."""
        if 'versions' in dictionary:
            return VersionList(dictionary['versions'])
        elif 'version' in dictionary:
            return VersionList([dictionary['version']])
        else:
            raise ValueError("Dict must have 'version' or 'versions' in it.")

    @coerced
    def satisfies(self, other, strict=False):
        """A VersionList satisfies another if some version in the list
           would satisfy some version in the other list.  This uses
           essentially the same algorithm as overlaps() does for
           VersionList, but it calls satisfies() on member Versions
           and VersionRanges.

           If strict is specified, this version list must lie entirely
           *within* the other in order to satisfy it.
        """
        if not other or not self:
            return False

        if strict:
            return self in other

        s = o = 0
        while s < len(self) and o < len(other):
            if self[s].satisfies(other[o]):
                return True
            elif self[s] < other[o]:
                s += 1
            else:
                o += 1
        return False

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
        changed = (isection.versions != self.versions)
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
            elif all(version not in v for v in self[i - 1:]):
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


def _string_to_version(string):
    """Converts a string to a Version, VersionList, or VersionRange.
       This is private.  Client code should use ver().
    """
    string = string.replace(' ', '')

    if ',' in string:
        return VersionList(string.split(','))

    elif ':' in string:
        s, e = string.split(':')
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
    elif isinstance(obj, string_types):
        return _string_to_version(obj)
    elif isinstance(obj, (int, float)):
        return _string_to_version(str(obj))
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


_CommitLookupResult = Tuple[Optional[str], Optional[int]]


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

    @property
    def git_repo_path(self):
        # type: () -> str
        return self.pkg.git  # type: ignore[attr-defined]

    @property
    def versions(self):
        # type: () -> List[Version]
        return self.pkg.versions  # type: ignore[attr-defined]

    # The following properties are used as part of a lazy reference scheme
    # to avoid querying the package repository until it is necessary (and
    # in particular to wait until after the configuration has been
    # assembled)
    @property                   # type: ignore[misc]
    @lang.memoized
    def cache_key(self):
        # type: () -> str
        key_base = 'git_metadata'
        if not self.repository_uri.startswith('/'):
            key_base += '/'
        cache_key = key_base + self.repository_uri

        # Cache data in misc_cache
        # If this is the first lazy access, initialize the cache as well
        spack.caches.misc_cache.init_entry(cache_key)

        return cache_key

    @property                   # type: ignore[misc]
    @lang.memoized
    def cache_path(self):
        # type: () -> str
        return spack.caches.misc_cache.cache_path(self.cache_key)

    @property                   # type: ignore[misc]
    @lang.memoized
    def pkg(self):
        # type: () -> PackageBase
        return spack.repo.get(self.pkg_name)

    @lang.memoized
    def fetcher(self, commit):
        # type: (str) -> GitFetchStrategy
        import spack.fetch_strategy  # break cycle
        return spack.fetch_strategy.GitFetchStrategy(
            git=self.pkg.git,
            commit=commit,
            # We require the full git repository history.
            get_full_repo=True,
        )

    @property
    def repository_uri(self):
        # type: () -> str
        """
        Identifier for git repos used within the repo and metadata caches.

        """
        try:
            components = [str(c).lstrip('/')
                          for c in spack.util.url.parse_git_url(self.pkg.git)
                          if c]
            return os.path.join(*components)
        except ValueError:
            # If it's not a git url, it's a local path
            return os.path.abspath(self.pkg.git)

    def save(self):
        # type: () -> None
        """
        Save the data to file
        """
        with spack.caches.misc_cache.write_transaction(self.cache_key) as (old, new):
            sjson.dump(self.data, new)

    def load_data(self):
        # type: () -> None
        """
        Load data if the path already exists.
        """
        if os.path.isfile(self.cache_path):
            with spack.caches.misc_cache.read_transaction(self.cache_key) as cache_file:
                self.data = sjson.load(cache_file)

    def get(self, commit):
        # type: (str) -> _CommitLookupResult
        if not self.data:
            self.load_data()

        if commit not in self.data:
            self.data[commit] = self.lookup_commit(commit)
            self.save()

        return self.data[commit]

    def lookup_commit(self, commit):
        # type: (str) -> _CommitLookupResult
        """Lookup the previous version and distance for a given commit.

        We use git to compare the known versions from the package to the git tags,
        as well as any git tags that are SEMVER versions, and find the latest
        known version prior to the commit, as well as the distance from that version
        to the commit in the git repo. Those values are used to compare Version objects.
        """
        fetcher = self.fetcher(commit)
        from spack.stage import Stage
        with Stage(fetcher):
            assert fetcher.fetch()
            git_repo = fetcher.canonical_git_repo

            # Lookup commit info.
            import spack.fetch_strategy as fs  # break cycle
            initial_ref = fs.GitRef.Commit(commit)
            # Ensure commit is an object known to git.
            if git_repo.expand_commit_hash(initial_ref) is None:
                raise spack.fetch_strategy.InvalidGitRef(
                    "initial reference '{0}' was not found in repo {1}"
                    .format(initial_ref, git_repo))

            # Lookup of commits to spack versions.
            commit_to_version = {}  # type: Dict[GitCommit, Version]
            for tag_commit, tag in git_repo.tags_for():
                # For each tag, try to match to a version.
                for v in self.versions:
                    if v.matches_regardless_of_v_prefix(tag.version):
                        commit_to_version[tag_commit] = v
                        break
                else:
                    # Try to parse tag to compare versions spack does not know.
                    maybe_semver = tag.version.parse_semver()
                    if maybe_semver:
                        commit_to_version[tag_commit] = maybe_semver

            ancestor_commits = []  # type: List[Tuple[GitCommit, int]]
            for tag_commit, v in commit_to_version.items():
                distance = git_repo.calculate_ancestry_distance(tag_commit, initial_ref)
                if distance is not None:
                    ancestor_commits.append((tag_commit, distance))

            # Get nearest ancestor that is a known version.
            prev_version = None  # type: Optional[str]
            if ancestor_commits:
                ancestor_commits.sort(key=lambda x: x[1])
                prev_version_commit, distance = ancestor_commits[0]
                prev_version = commit_to_version[prev_version_commit].string
            else:
                # Get list of all commit in reverse order. We then use this to get the
                # first commit.
                commits = git_repo.all_commits_for()

                # No previous version, so calculate distance from the first commit.
                distance = git_repo.calculate_ancestry_distance(
                    commits[-1], initial_ref)

            return prev_version, distance
