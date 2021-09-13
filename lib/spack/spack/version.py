# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

from six import string_types

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

import spack.error
import spack.paths
import spack.util.executable
import spack.util.spack_json as sjson
from spack.util.spack_yaml import syaml_dict

__all__ = ['Version', 'VersionRange', 'VersionList', 'ver']

# Valid version characters
VALID_VERSION = re.compile(r'^[A-Za-z0-9_.-]+$')

# regex for a commit version
COMMIT_VERSION = re.compile(r'^[a-z0-9]{40}$')

# regex for version segments
SEGMENT_REGEX = re.compile(r'(?:(?P<num>[0-9]+)|(?P<str>[a-zA-Z]+))(?P<sep>[_.-]*)')

# regular expression for semantic versioning
SEMVER_REGEX = re.compile(".+(?P<semver>([0-9]+)[.]([0-9]+)[.]([0-9]+)"
                          "(?:-([0-9A-Za-z-]+(?:[.][0-9A-Za-z-]+)*))?"
                          "(?:[+][0-9A-Za-z-]+)?)")

# Infinity-like versions. The order in the list implies the comparison rules
infinity_versions = ['develop', 'main', 'master', 'head', 'trunk']

iv_min_len = min(len(s) for s in infinity_versions)


def coerce_versions(a, b):
    """
    Convert both a and b to the 'greatest' type between them, in this order:
           Version < VersionRange < VersionList
    This is used to simplify comparison operations below so that we're always
    comparing things that are of the same type.
    """
    order = (Version, VersionRange, VersionList)
    ta, tb = type(a), type(b)

    def check_type(t):
        if t not in order:
            raise TypeError("coerce_versions cannot be called on %s" % t)
    check_type(ta)
    check_type(tb)

    if ta == tb:
        return (a, b)
    elif order.index(ta) > order.index(tb):
        if ta == VersionRange:
            return (a, VersionRange(b, b))
        else:
            return (a, VersionList([b]))
    else:
        if tb == VersionRange:
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


class Version(object):
    """Class to represent versions"""
    __slots__ = ['version', 'separators', 'string', 'commits']

    def __init__(self, string):
        if not isinstance(string, str):
            string = str(string)

        # preserve the original string, but trimmed.
        string = string.strip()
        self.string = string

        if not VALID_VERSION.match(string):
            raise ValueError("Bad characters in version string: %s" % string)

        # A cache of known commits, if needed
        self.commits = {}

        segments = SEGMENT_REGEX.findall(string)
        self.version = tuple(
            int(m[0]) if m[0] else VersionStrComponent(m[1]) for m in segments
        )
        self.separators = tuple(m[2] for m in segments)

    def _cmp(self, commit_info={}):
        if self.is_commit and self.string in commit_info:
            self_info = commit_info[self.string]
            prev_version = self_info.get('prev_version', None)
            distance = self_info['distance']

            # Extend previous version by empty component and distance
            # If commit is exactly a known version, no distance suffix
            prev_tuple = Version(prev_version).version if prev_version else ()
            distance_suffix = (VersionStrComponent(''), distance) if distance else ()
            return prev_tuple + distance_suffix
        else:
            return self.version

    @property
    def is_commit(self):
        """
        Determine if the original string is referencing a commit.
        """
        if self.string in infinity_versions:
            return False
        return COMMIT_VERSION.match(self.string) is not None

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
        return Version(self.string.replace('-', '.').replace('_', '.'))

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
        return Version(self.string.replace('.', '_').replace('-', '_'))

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
        return Version(self.string.replace('.', '-').replace('_', '-'))

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
        return Version(
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
        commits = self.commits or other.commits
        self_cmp = self._cmp(commit_info=commits)
        other_cmp = other._cmp(commit_info=commits)

        # Do the final comparison
        nself = len(self_cmp)
        nother = len(other_cmp)
        return nother <= nself and self_cmp[:nother] == other_cmp

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

            string_arg.pop()  # We don't need the last separator
            string_arg = ''.join(string_arg)
            return cls(string_arg)

        message = '{cls.__name__} indices must be integers'
        raise TypeError(message.format(cls=cls))

    def __repr__(self):
        return 'Version(' + repr(self.string) + ')'

    def __str__(self):
        return self.string

    def __format__(self, format_spec):
        return self.string.format(format_spec)

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

        commits = self.commits or other.commits
        # If either is a commit and we haven't indexed yet, can't compare
        if other.is_commit or self.is_commit and not commits:
            return False

        # Use tuple comparison assisted by VersionStrComponent for performance
        return self._cmp(commit_info=commits) < other._cmp(commit_info=commits)

    @coerced
    def __eq__(self, other):

        # Cut out early if we don't have a version
        if other is None or type(other) != Version:
            return False

        commits = self.commits or other.commits
        return self._cmp(commit_info=commits) == other._cmp(commit_info=commits)

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

        commits = self.commits or other.commits
        self_cmp = self._cmp(commit_info=commits)
        return other._cmp(commit_info=commits)[:len(self_cmp)] == self_cmp

    def is_predecessor(self, other):
        """True if the other version is the immediate predecessor of this one.
           That is, NO non-commit versions v exist such that:
           (self < v < other and v not in self).
        """
        commits = self.commits or other.commits
        self_cmp = self._cmp(commit_info=commits)
        other_cmp = other._cmp(commit_info=commits)

        if self_cmp[:-1] != other_cmp[:-1]:
            return False

        sl = self_cmp[-1]
        ol = other_cmp[-1]
        return type(sl) == int and type(ol) == int and (ol - sl == 1)

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

    def generate_commit_lookup(self, pkg, repository):
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
        if self.commits and self.string in self.commits:
            return

        # Sanity check we have a commit
        if not self.is_commit:
            tty.die("%s is not a commit." % self)

        # We require the full git repository history
        from spack.fetch_strategy import GitFetchStrategy  # break cycle
        fetcher = GitFetchStrategy(git=repository)
        fetcher.get_full_repo = True

        # Generate a commit looker-upper
        lookup = CommitLookup(fetcher)

        # This shows a previous, and next spack version
        self.commits = lookup.get_commit_lookup(self, pkg.versions)
        lookup.save()


class VersionRange(object):

    def __init__(self, start, end):
        if isinstance(start, string_types):
            start = Version(start)
        if isinstance(end, string_types):
            end = Version(end)

        self.start = start
        self.end = end
        if start and end and end < start:
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
        """A VersionRange satisfies another if some version in this range
        would satisfy some version in the other range.  To do this it must
        either:

        a) Overlap with the other range
        b) The start of this range satisfies the end of the other range.

        This is essentially the same as overlaps(), but overlaps assumes
        that its arguments are specific.  That is, 4.7 is interpreted as
        4.7.0.0.0.0... .  This function assumes that 4.7 would be satisfied
        by 4.7.3.5, etc.

        Rationale:

        If a user asks for gcc@4.5:4.7, and a package is only compatible with
        gcc@4.7.3:4.8, then that package should be able to build under the
        constraints.  Just using overlaps() would not work here.

        Note that we don't need to check whether the end of this range
        would satisfy the start of the other range, because overlaps()
        already covers that case.

        Note further that overlaps() is a symmetric operation, while
        satisfies() is not.
        """
        return (self.overlaps(other) or
                # if either self.start or other.end are None, then this can't
                # satisfy, or overlaps() would've taken care of it.
                self.start and other.end and self.start.satisfies(other.end))

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
        if type(version) in (Version, VersionRange):
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
    elif type(obj) in (Version, VersionRange, VersionList):
        return obj
    else:
        raise TypeError("ver() can't convert %s to version!" % type(obj))


class VersionError(spack.error.SpackError):
    """This is raised when something is wrong with a version."""


class VersionChecksumError(VersionError):
    """Raised for version checksum errors."""


class CommitLookup(object):

    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.data = {}

    @property
    def repository_uri(self):
        # Case 1: It's a path on the filesystem
        if os.path.exists(self.fetcher.url) or self.fetcher.url.startswith("file://"):
            return re.sub("file://", "", self.fetcher.url)
        return re.sub("[.]git$", "", os.sep.join(self.fetcher.url.split(os.sep)[-3:]))

    @property
    def repository_metadata_path(self):
        filename = "%s.json" % self.repository_uri.replace('/', '-')
        return os.path.join(spack.paths.user_repos_metadata_path, filename)

    def save(self):
        """
        Save the data to file
        """
        with open(self.repository_metadata_path, 'w') as fd:
            sjson.dump(self.data, fd)

    def load_data(self):
        """
        Load data if the path already exists.
        """
        if os.path.exists(self.repository_metadata_path):
            with open(self.repository_metadata_path, 'r') as fd:
                self.data = sjson.load(fd.read())

    def get_commit_lookup(self, version, spack_versions):
        """
        Given a git handle, repository, and known spack versions, generate a lookup.

        We do this by listing all the tags for a repository path, in the order of
        release (the assumption being that versioned releases/candidates that are
        later are preferable to earlier) and then we match these versions to known
        spack versions. We can then parse the entire git history, and generate
        a lookup that describes the context of every commit to a known spack
        version. In the case that commit is an exact match, exact_version will
        be true. If a commit does not have a spack version before it, or does
        not have a spack version after it, then the value will be None.
        """
        # lookup cache and return early here
        self.load_data()

        # Cut out early if we already have the version cached
        if str(version) in self.data:
            return self.data

        # Were we given an already cloned path?
        already_cloned = os.path.exists(self.repository_uri)
        if already_cloned:
            dest = self.repository_uri

        # Otherwise honor the namespace for the service and repository
        else:
            dest = os.path.join(spack.paths.user_repos_cache_path, self.repository_uri)

        # prepare a cache for the repository and metadata
        for path in [dest, self.repository_metadata_path]:
            parent = os.path.dirname(path)
            if not os.path.exists(parent):
                os.makedirs(parent)

        # Only clone if we don't have it!
        if not os.path.exists(dest):
            self.fetcher.clone(os.path.dirname(dest))

        # But if we get here and no repostiory, this is a fail
        if not os.path.exists(dest):
            tty.die("There was an issue cloning %s to %s" % (self.fetcher.url, dest))

        # Always pull and fetch
        with working_dir(dest):

            # Don't do anything if already cloned - it might not have remote
            if not already_cloned:
                self.fetcher.git("pull")
                self.fetcher.git("fetch")

            # List tags (refs) by date, so last reference of a tag is newest
            tag_info = self.fetcher.git(
                "for-each-ref", "--sort=creatordate", "--format",
                "%(objectname) %(refname)", "refs/tags", output=str).split('\n')

            # Get list of all commits, this is in reverse order
            commits = self.fetcher.git("log", "--all", "--pretty=format:%H", output=str)

        # Lookup of commits to spack versions
        commit_to_version = {}

        for entry in tag_info:
            if not entry:
                continue
            commit, tag = entry.split()
            tag = tag.replace('refs/tags/', '', 1)

            # For each tag, try to match to a version
            for v in [v.string for v in spack_versions]:
                if v in tag:
                    commit_to_version[commit] = v
                    break
            else:
                # try to parse tag to copare versions spack does not know
                match = SEMVER_REGEX.match(tag)
                if match:
                    semver = match.gropudict()['semver']
                    commit_to_version[commit] = semver

        # commits[0] is most recent, commits[-2] is first
        commits = [c for c in commits.split('\n') if c]

        for commit in commits:
            # Get commits associated with tags that're ancestors of this commit
            # Values are tuples of ancestor and distance in commits
            ancestor_commits = []
            for tag_commit in commit_to_version:
                with working_dir(dest):
                    self.fetcher.git(
                        'merge-base', '--is-ancestor', tag_commit, commit,
                        ignore_errors=[1])
                    if self.fetcher.git.returncode == 0:
                        distance = self.fetcher.git(
                            'rev-list', '%s..%s' % (tag_commit, commit), '--count',
                            output=str, error=str).strip()
                        ancestor_commits.append((tag_commit, int(distance)))

            # Get nearest ancestor that is a known version
            ancestor_commits.sort(key=lambda x: x[1])
            if ancestor_commits:
                prev_version_commit, distance = ancestor_commits[0]
                prev_version = commit_to_version[prev_version_commit]
            else:
                prev_version = None
                with working_dir(dest):
                    distance = self.fetcher.git(
                        'rev-list', '%s..%s' % (commits[-1], commit),
                        output=str, error=str
                    ).strip()

            # Write out data for this commit
            self.data[commit] = {
                'prev_version': prev_version,
                'distance': distance,
            }

        if str(version) not in self.data:
            tty.die("%s is not in the history of %s" % (version, self.fetcher.url))
        return self.data
