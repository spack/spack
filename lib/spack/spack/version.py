import os
import re
from functools import total_ordering

import utils
import spack.error as serr


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
    def __init__(self, version_string):
        # preserve the original string
        self.version_string = version_string

        # Split version into alphabetical and numeric segments
        segments = re.findall(r'[a-zA-Z]+|[0-9]+', version_string)
        self.version = tuple(int_if_int(seg) for seg in segments)

    def up_to(self, index):
        """Return a version string up to the specified component, exclusive.
           e.g., if this is 10.8.2, self.up_to(2) will return '10.8'.
        """
        return '.'.join(str(x) for x in self[:index])

    def __getitem__(self, idx):
        return tuple(self.version[idx])

    def __repr__(self):
        return self.version_string

    def __str__(self):
        return self.version_string

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


    def __str__(self):
        out = ""
        if self.start:
            out += str(self.start)
        out += ":"
        if self.end:
            out += str(self.end)
        return out


class VersionParseError(serr.SpackError):
    """Raised when the version module can't parse something."""
    def __init__(self, msg, spec):
        super(VersionParseError, self).__init__(msg)
        self.spec = spec


class UndetectableVersionError(VersionParseError):
    """Raised when we can't parse a version from a string."""
    def __init__(self, spec):
        super(UndetectableVersionError, self).__init__(
            "Couldn't detect version in: " + spec, spec)


class UndetectableNameError(VersionParseError):
    """Raised when we can't parse a package name from a string."""
    def __init__(self, spec):
        super(UndetectableNameError, self).__init__(
            "Couldn't parse package name in: " + spec)


def parse_version_string_with_indices(spec):
    """Try to extract a version string from a filename or URL.  This is taken
       largely from Homebrew's Version class."""

    if os.path.isdir(spec):
        stem = os.path.basename(spec)
    elif re.search(r'((?:sourceforge.net|sf.net)/.*)/download$', spec):
        stem = utils.stem(os.path.dirname(spec))
    else:
        stem = utils.stem(spec)

    version_types = [
        # GitHub tarballs, e.g. v1.2.3
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+)$', spec),

        # e.g. https://github.com/sam-github/libnet/tarball/libnet-1.1.4
        (r'github.com/.+/(?:zip|tar)ball/.*-((\d+\.)+\d+)$', spec),

        # e.g. https://github.com/isaacs/npm/tarball/v0.2.5-1
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+-(\d+))$', spec),

        # e.g. https://github.com/petdance/ack/tarball/1.93_02
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+_(\d+))$', spec),

        # e.g. https://github.com/erlang/otp/tarball/OTP_R15B01 (erlang style)
        (r'[-_](R\d+[AB]\d*(-\d+)?)', spec),

        # e.g. boost_1_39_0
        (r'((\d+_)+\d+)$', stem),

        # e.g. foobar-4.5.1-1
        # e.g. ruby-1.9.1-p243
        (r'-((\d+\.)*\d\.\d+-(p|rc|RC)?\d+)(?:[-._](?:bin|dist|stable|src|sources))?$', stem),

        # e.g. lame-398-1
        (r'-((\d)+-\d)', stem),

        # e.g. foobar-4.5.1
        (r'-((\d+\.)*\d+)$', stem),

        # e.g. foobar-4.5.1b
        (r'-((\d+\.)*\d+([a-z]|rc|RC)\d*)$', stem),

        # e.g. foobar-4.5.0-beta1, or foobar-4.50-beta
        (r'-((\d+\.)*\d+-beta(\d+)?)$', stem),

        # e.g. foobar4.5.1
        (r'((\d+\.)*\d+)$', stem),

        # e.g. foobar-4.5.0-bin
        (r'-((\d+\.)+\d+[a-z]?)[-._](bin|dist|stable|src|sources?)$', stem),

        # e.g. dash_0.5.5.1.orig.tar.gz (Debian style)
        (r'_((\d+\.)+\d+[a-z]?)[.]orig$', stem),

        # e.g. http://www.openssl.org/source/openssl-0.9.8s.tar.gz
        (r'-([^-]+)', stem),

        # e.g. astyle_1.23_macosx.tar.gz
        (r'_([^_]+)', stem),

        # e.g. http://mirrors.jenkins-ci.org/war/1.486/jenkins.war
        (r'\/(\d\.\d+)\/', spec),

        # e.g. http://www.ijg.org/files/jpegsrc.v8d.tar.gz
        (r'\.v(\d+[a-z]?)', stem)]

    for vtype in version_types:
        regex, match_string = vtype[:2]
        match = re.search(regex, match_string)
        if match and match.group(1) is not None:
            return match.group(1), match.start(1), match.end(1)

    raise UndetectableVersionError(spec)


def parse_version(spec):
    """Given a URL or archive name, extract a version from it and return
       a version object.
    """
    ver, start, end = parse_version_string_with_indices(spec)
    return Version(ver)


def create_version_format(spec):
    """Given a URL or archive name, find the version and create a format string
       that will allow another version to be substituted.
    """
    ver, start, end = parse_version_string_with_indices(spec)
    return spec[:start] + '%s' + spec[end:]


def replace_version(spec, new_version):
    version = create_version_format(spec)
    # TODO: finish this function.

def parse_name(spec, ver=None):
    if ver is None:
        ver = parse_version(spec)

    ntypes = (r'/sourceforge/([^/]+)/',
              r'/([^/]+)/(tarball|zipball)/',
              r'/([^/]+)[_.-](bin|dist|stable|src|sources)[_.-]%s' % ver,
              r'/([^/]+)[_.-]v?%s' % ver,
              r'/([^/]+)%s' % ver,
              r'^([^/]+)[_.-]v?%s' % ver,
              r'^([^/]+)%s' % ver)

    for nt in ntypes:
        match = re.search(nt, spec)
        if match:
            return match.group(1)
    raise UndetectableNameError(spec)

def parse(spec):
    ver = parse_version(spec)
    name = parse_name(spec, ver)
    return (name, ver)
