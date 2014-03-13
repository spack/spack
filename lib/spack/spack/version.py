##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
import os
import sys
import re
from bisect import bisect_left
from functools import total_ordering, wraps

import llnl.util.compare.none_high as none_high
import llnl.util.compare.none_low as none_low
import spack.error

# Valid version characters
VALID_VERSION = r'[A-Za-z0-9_.-]'

def int_if_int(string):
    """Convert a string to int if possible.  Otherwise, return a string."""
    try:
        return int(string)
    except ValueError:
        return string


def coerce_versions(a, b):
    """Convert both a and b to the 'greatest' type between them, in this order:
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
    def coercing_method(a, b):
        if type(a) == type(b) or a is None or b is None:
            return method(a, b)
        else:
            ca, cb = coerce_versions(a, b)
            return getattr(ca, method.__name__)(cb)
    return coercing_method


@total_ordering
class Version(object):
    """Class to represent versions"""
    def __init__(self, string):
        string = str(string)

        if not re.match(VALID_VERSION, string):
            raise ValueError("Bad characters in version string: %s" % string)

        # preserve the original string, but trimmed.
        string = string.strip()
        self.string = string

        # Split version into alphabetical and numeric segments
        segment_regex = r'[a-zA-Z]+|[0-9]+'
        segments = re.findall(segment_regex, string)
        self.version = tuple(int_if_int(seg) for seg in segments)

        # Store the separators from the original version string as well.
        # last element of separators is ''
        self.separators = tuple(re.split(segment_regex, string)[1:-1])


    def up_to(self, index):
        """Return a version string up to the specified component, exclusive.
           e.g., if this is 10.8.2, self.up_to(2) will return '10.8'.
        """
        return '.'.join(str(x) for x in self[:index])


    def lowest(self):
        return self


    def highest(self):
        return self


    def wildcard(self):
        """Create a regex that will match variants of this version string."""
        def a_or_n(seg):
            if type(seg) == int:
                return r'[0-9]+'
            else:
                return r'[a-zA-Z]+'

        version = self.version
        separators = ('',) + self.separators

        version += (version[-1],) * 2
        separators += (separators[-1],) * 2

        sep_res = [re.escape(sep) for sep in separators]
        seg_res = [a_or_n(seg) for seg in version]

        wc = seg_res[0]
        for i in xrange(1, len(sep_res)):
            wc += '(?:' + sep_res[i] + seg_res[i]

        # Add possible alpha or beta indicator at the end of each segemnt
        # We treat these specially b/c they're so common.
        wc += '[ab]?)?' * (len(seg_res) - 1)
        return wc


    def __iter__(self):
        return iter(self.version)


    def __getitem__(self, idx):
        return tuple(self.version[idx])


    def __repr__(self):
        return self.string


    def __str__(self):
        return self.string


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

        # Coerce if other is not a Version
        # simple equality test first.
        if self.version == other.version:
            return False

        for a, b in zip(self.version, other.version):
            if a == b:
                continue
            else:
                # Numbers are always "newer" than letters.  This is for
                # consistency with RPM.  See patch #60884 (and details)
                # from bugzilla #50977 in the RPM project at rpm.org.
                # Or look at rpmvercmp.c if you want to see how this is
                # implemented there.
                if type(a) != type(b):
                    return type(b) == int
                else:
                    return a < b

        # If the common prefix is equal, the one with more segments is bigger.
        return len(self.version) < len(other.version)


    @coerced
    def __eq__(self, other):
        return (other is not None and
                type(other) == Version and self.version == other.version)


    def __ne__(self, other):
        return not (self == other)


    def __hash__(self):
        return hash(self.version)


    @coerced
    def __contains__(self, other):
        return self == other


    @coerced
    def overlaps(self, other):
        return self == other


    @coerced
    def union(self, other):
        if self == other:
            return self
        else:
            return VersionList([self, other])


    @coerced
    def intersection(self, other):
        if self == other:
            return self
        else:
            return VersionList()


@total_ordering
class VersionRange(object):
    def __init__(self, start, end):
        if isinstance(start, basestring):
            start = Version(start)
        if isinstance(end, basestring):
            end = Version(end)

        self.start = start
        self.end = end
        if start and end and  end < start:
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

        return (none_low.lt(self.start, other.start) or
                (self.start == other.start and
                 none_high.lt(self.end, other.end)))


    @coerced
    def __eq__(self, other):
        return (other is not None and
                type(other) == VersionRange and
                self.start == other.start and self.end == other.end)


    def __ne__(self, other):
        return not (self == other)


    @property
    def concrete(self):
        return self.start if self.start == self.end else None


    @coerced
    def __contains__(self, other):
        return (none_low.ge(other.start, self.start) and
                none_high.le(other.end, self.end))


    @coerced
    def overlaps(self, other):
        return (other in self or self in other or
                ((self.start == None or other.end is None or
                  self.start <= other.end) and
                 (other.start is None or self.end == None or
                  other.start <= self.end)))


    @coerced
    def union(self, other):
        if self.overlaps(other):
            return VersionRange(none_low.min(self.start, other.start),
                                none_high.max(self.end, other.end))
        else:
            return VersionList([self, other])


    @coerced
    def intersection(self, other):
        if self.overlaps(other):
            return VersionRange(none_low.max(self.start, other.start),
                                none_high.min(self.end, other.end))
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


@total_ordering
class VersionList(object):
    """Sorted, non-redundant list of Versions and VersionRanges."""
    def __init__(self, vlist=None):
        self.versions = []
        if vlist is not None:
            if isinstance(vlist, basestring):
                vlist = _string_to_version(vlist)
                if type(vlist) == VersionList:
                    self.versions = vlist.versions
                else:
                    self.versions = [vlist]
            else:
                vlist = list(vlist)
                for v in vlist:
                    self.add(ver(v))


    def add(self, version):
        if type(version) in (Version, VersionRange):
            # This normalizes single-value version ranges.
            if version.concrete:
                version = version.concrete

            i = bisect_left(self, version)

            while i-1 >= 0 and version.overlaps(self[i-1]):
                version = version.union(self[i-1])
                del self.versions[i-1]
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


    def satisfies(self, other):
        """Synonym for overlaps."""
        return self.overlaps(other)


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
        isection = self.intersection(other)
        self.versions = isection.versions


    @coerced
    def __contains__(self, other):
        if len(self) == 0:
            return False

        for version in other:
            i = bisect_left(self, other)
            if i == 0:
                if version not in self[0]:
                    return False
            elif all(version not in v for v in self[i-1:]):
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


    @coerced
    def __eq__(self, other):
        return other is not None and self.versions == other.versions


    def __ne__(self, other):
        return not (self == other)


    @coerced
    def __lt__(self, other):
        return other is not None and self.versions < other.versions


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
    string = string.replace(' ','')

    if ',' in string:
        return VersionList(string.split(','))

    elif ':' in string:
        s, e = string.split(':')
        start = Version(s) if s else None
        end   = Version(e) if e else None
        return VersionRange(start, end)

    else:
        return Version(string)


def ver(obj):
    """Parses a Version, VersionRange, or VersionList from a string
       or list of strings.
    """
    if isinstance(obj, (list, tuple)):
        return VersionList(obj)
    elif isinstance(obj, basestring):
        return _string_to_version(obj)
    elif isinstance(obj, (int, float)):
        return _string_to_version(str(obj))
    elif type(obj) in (Version, VersionRange, VersionList):
        return obj
    else:
        raise TypeError("ver() can't convert %s to version!" % type(obj))
