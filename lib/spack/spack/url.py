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
import spack.util.compression as comp
from spack.version import Version

#
# Note: We call the input to most of these functions a "path" but the functions
# work on paths and URLs.  There's not a good word for both of these, but
# "path" seemed like the most generic term.
#

def find_list_url(url):
    """Finds a good list URL for the supplied URL.  This depends on
       the site.  By default, just assumes that a good list URL is the
       dirname of an archive path.  For github URLs, this returns the
       URL of the project's releases page.
    """

    url_types = [
        # e.g. https://github.com/scalability-llnl/callpath/archive/v1.0.1.tar.gz
        (r'^(https://github.com/[^/]+/[^/]+)/archive/', lambda m: m.group(1) + '/releases')
        ]

    for pattern, fun in url_types:
        match = re.search(pattern, url)
        if match:
            return fun(match)
    else:
        return os.path.dirname(url)


def parse_version_offset(path):
    """Try to extract a version string from a filename or URL.  This is taken
       largely from Homebrew's Version class."""

    # Strip off sourceforge download stuffix.
    if re.search(r'((?:sourceforge.net|sf.net)/.*)/download$', path):
        path = os.path.dirname(path)

    # Strip archive extension
    path = comp.strip_extension(path)

    # Take basename to avoid including parent dirs in version name
    # Remember the offset of the stem in the full path.
    stem = os.path.basename(path)
    offset = len(path) - len(stem)

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
        (r'-([^-]+(-alpha|-beta)?)', stem),

        # e.g. astyle_1.23_macosx.tar.gz
        (r'_([^_]+(_alpha|_beta)?)', stem),

        # e.g. http://mirrors.jenkins-ci.org/war/1.486/jenkins.war
        (r'\/(\d\.\d+)\/', path),

        # e.g. http://www.ijg.org/files/jpegsrc.v8d.tar.gz
        (r'\.v(\d+[a-z]?)', stem)]

    for i, vtype in enumerate(version_types):
        regex, match_string = vtype[:2]
        match = re.search(regex, match_string)
        if match and match.group(1) is not None:
            version = match.group(1)
            start = offset + match.start(1)
            return version, start, len(version)

    raise UndetectableVersionError(path)


def parse_version(path):
    """Given a URL or archive name, extract a version from it and return
       a version object.
    """
    ver, start, l = parse_version_offset(path)
    return Version(ver)


def parse_name_offset(path, ver=None):
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
            name = match.group(1)
            return name, match.start(1), len(name)
    raise UndetectableNameError(path)


def parse_name(path, ver=None):
    name, start, l = parse_name_offset(path, ver)
    return name


def parse_name_and_version(path):
    ver = parse_version(path)
    name = parse_name(path, ver)
    return (name, ver)


def insensitize(string):
    """Chagne upper and lowercase letters to be case insensitive in
       the provided string.  e.g., 'a' because '[Aa]', 'B' becomes
       '[bB]', etc.  Use for building regexes."""
    def to_ins(match):
        char = match.group(1)
        return '[%s%s]' % (char.lower(), char.upper())
    return re.sub(r'([a-zA-Z])', to_ins, string)


def substitute_version(path, new_version):
    """Given a URL or archive name, find the version in the path and substitute
       the new version for it.
    """
    ver, start, l = parse_version_offset(path)
    return path[:start] + str(new_version) + path[(start+l):]


def wildcard_version(path):
    """Find the version in the supplied path, and return a regular expression
       that will match this path with any version in its place.
    """
    # Get name and version, so we can treat them specially
    name, v = parse_name_and_version(path)

    # Construct a case-insensitive regular expression for the package name.
    name_re = '(%s)' % insensitize(name)

    # protect extensions like bz2 from wildcarding.
    ext = comp.extension(path)
    path = comp.strip_extension(path)

    # Split the string apart by things that match the name so that if the
    # name contains numbers or things that look like versions, we don't
    # catch them with the version wildcard.
    name_parts = re.split(name_re, path)

    # Even elements in the array did *not* match the name
    for i in xrange(0, len(name_parts), 2):
        # Split each part by things that look like versions.
        vparts = re.split(v.wildcard(), name_parts[i])

        # Replace each version with a generic capture group to find versions.
        # And escape everything else so it's not interpreted as a regex
        vgroup = '(%s)' % v.wildcard()
        name_parts[i] = vgroup.join(re.escape(vp) for vp in vparts)

    # Put it all back together with original name matches intact.
    return ''.join(name_parts) + '.' + ext


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
