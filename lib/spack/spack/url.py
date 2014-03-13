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
This module has methods for parsing names and versions of packages from URLs.
The idea is to allow package creators to supply nothing more than the
download location of the package, and figure out version and name information
from there.

Example: when spack is given the following URL:

    ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.1-p243.tar.gz

It can figure out that the package name is ruby, and that it is at version
1.9.1-p243.  This is useful for making the creation of packages simple: a user
just supplies a URL and skeleton code is generated automatically.

Spack can also figure out that it can most likely download 1.8.1 at this URL:

    ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.8.1.tar.gz

This is useful if a user asks for a package at a particular version number;
spack doesn't need anyone to tell it where to get the tarball even though
it's never been told about that version before.
"""
import os
import re

import spack.error
import spack.util.filesystem as fs
from spack.version import Version

#
# Note: We call the input to most of these functions a "path" but the functions
# work on paths and URLs.  There's not a good word for both of these, but
# "path" seemed like the most generic term.
#

class UrlParseError(spack.error.SpackError):
    """Raised when the URL module can't parse something correctly."""
    def __init__(self, msg, path):
        super(UrlParseError, self).__init__(msg)
        self.path = path


class UndetectableVersionError(UrlParseError):
    """Raised when we can't parse a version from a string."""
    def __init__(self, path):
        super(UndetectableVersionError, self).__init__(
            "Couldn't detect version in: " + path, path)


class UndetectableNameError(UrlParseError):
    """Raised when we can't parse a package name from a string."""
    def __init__(self, path):
        super(UndetectableNameError, self).__init__(
            "Couldn't parse package name in: " + path, path)


def parse_version_string_with_indices(path):
    """Try to extract a version string from a filename or URL.  This is taken
       largely from Homebrew's Version class."""

    if os.path.isdir(path):
        stem = os.path.basename(path)
    elif re.search(r'((?:sourceforge.net|sf.net)/.*)/download$', path):
        stem = fs.stem(os.path.dirname(path))
    else:
        stem = fs.stem(path)

    version_types = [
        # GitHub tarballs, e.g. v1.2.3
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+)$', path),

        # e.g. https://github.com/sam-github/libnet/tarball/libnet-1.1.4
        (r'github.com/.+/(?:zip|tar)ball/.*-((\d+\.)+\d+)$', path),

        # e.g. https://github.com/isaacs/npm/tarball/v0.2.5-1
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+-(\d+))$', path),

        # e.g. https://github.com/petdance/ack/tarball/1.93_02
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+_(\d+))$', path),

        # e.g. https://github.com/hpc/lwgrp/archive/v1.0.1.tar.gz
        (r'github.com/[^/]+/[^/]+/archive/v?(\d+(?:\.\d+)*)\.tar\.gz$', path),

        # e.g. https://github.com/erlang/otp/tarball/OTP_R15B01 (erlang style)
        (r'[-_](R\d+[AB]\d*(-\d+)?)', path),

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
        (r'\/(\d\.\d+)\/', path),

        # e.g. http://www.ijg.org/files/jpegsrc.v8d.tar.gz
        (r'\.v(\d+[a-z]?)', stem)]

    for vtype in version_types:
        regex, match_string = vtype[:2]
        match = re.search(regex, match_string)
        if match and match.group(1) is not None:
            return match.group(1), match.start(1), match.end(1)

    raise UndetectableVersionError(path)


def parse_version(path):
    """Given a URL or archive name, extract a version from it and return
       a version object.
    """
    ver, start, end = parse_version_string_with_indices(path)
    return Version(ver)


def parse_name(path, ver=None):
    if ver is None:
        ver = parse_version(path)

    ntypes = (r'/sourceforge/([^/]+)/',
              r'/([^/]+)/(tarball|zipball)/',
              r'/([^/]+)[_.-](bin|dist|stable|src|sources)[_.-]%s' % ver,
              r'github.com/[^/]+/([^/]+)/archive',
              r'/([^/]+)[_.-]v?%s' % ver,
              r'/([^/]+)%s' % ver,
              r'^([^/]+)[_.-]v?%s' % ver,
              r'^([^/]+)%s' % ver)

    for nt in ntypes:
        match = re.search(nt, path)
        if match:
            return match.group(1)
    raise UndetectableNameError(path)


def parse_name_and_version(path):
    ver = parse_version(path)
    name = parse_name(path, ver)
    return (name, ver)


def substitute_version(path, new_version):
    """Given a URL or archive name, find the version in the path and substitute
       the new version for it.
    """
    ver, start, end = parse_version_string_with_indices(path)
    return path[:start] + str(new_version) + path[end:]


def wildcard_version(path):
    """Find the version in the supplied path, and return a regular expression
       that will match this path with any version in its place.
    """
    ver, start, end = parse_version_string_with_indices(path)

    v = Version(ver)
    parts = list(re.escape(p) for p in path.split(str(v)))

    # Make a group for the wildcard, so it will be captured by the regex.
    version_group = '(%s)' % v.wildcard()
    return version_group.join(parts)
