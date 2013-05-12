import os
import re
from functools import total_ordering

import utils
import spack.error

# Valid version characters
VALID_VERSION = r'[A-Za-z0-9_.-]'


def int_if_int(string):
    """Convert a string to int if possible.  Otherwise, return a string."""
    try:
        return int(string)
    except:
        return string


def ver(string):
    """Parses either a version or version range from a string."""
    if ':' in string:
        start, end = string.split(':')
        return VersionRange(Version(start), Version(end))
    else:
        return Version(string)


@total_ordering
class Version(object):
    """Class to represent versions"""
    def __init__(self, string):
        if not re.match(VALID_VERSION, string):
            raise ValueError("Bad characters in version string: %s" % string)

        # preserve the original string
        self.string = string

        # Split version into alphabetical and numeric segments
        segment_regex = r'[a-zA-Z]+|[0-9]+'
        segments = re.findall(segment_regex, string)
        self.version = tuple(int_if_int(seg) for seg in segments)


    def up_to(self, index):
        """Return a version string up to the specified component, exclusive.
           e.g., if this is 10.8.2, self.up_to(2) will return '10.8'.
        """
        return '.'.join(str(x) for x in self[:index])

    def __iter__(self):
        for v in self.version:
            yield v

    def __getitem__(self, idx):
        return tuple(self.version[idx])

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __lt__(self, other):
        """Version comparison is designed for consistency with the way RPM
           does things.  If you need more complicated versions in installed
           packages, you should override your package's version string to
           express it more sensibly.
        """
        assert(other is not None)

        # Let VersionRange do all the range-based comparison
        if type(other) == VersionRange:
            return not other < self

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

    def __eq__(self, other):
        """Implemented to match __lt__.  See __lt__."""
        if type(other) == VersionRange:
            return False
        return self.version == other.version

    def __ne__(self, other):
        return not (self == other)


@total_ordering
class VersionRange(object):
    def __init__(self, start, end=None):
        if type(start) == str:
            start = Version(start)
        if type(end) == str:
            end = Version(end)

        self.start = start
        self.end = end
        if start and end and  end < start:
            raise ValueError("Invalid Version range: %s" % self)


    def __lt__(self, other):
        if type(other) == Version:
            return self.end and self.end < other
        elif type(other) == VersionRange:
            return self.end and other.start and self.end < other.start
        else:
            raise TypeError("Can't compare VersionRange to %s" % type(other))


    def __gt__(self, other):
        if type(other) == Version:
            return self.start and self.start > other
        elif type(other) == VersionRange:
            return self.start and other.end and self.start > other.end
        else:
            raise TypeError("Can't compare VersionRange to %s" % type(other))


    def __eq__(self, other):
        return (type(other) == VersionRange
                and self.start == other.start
                and self.end == other.end)


    def __ne__(self, other):
        return not (self == other)


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
