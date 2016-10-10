##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
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
from StringIO import StringIO
from urlparse import urlsplit, urlunsplit

import llnl.util.tty as tty
from llnl.util.tty.color import *

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
        # e.g. https://github.com/llnl/callpath/archive/v1.0.1.tar.gz
        (r'^(https://github.com/[^/]+/[^/]+)/archive/',
         lambda m: m.group(1) + '/releases')]

    for pattern, fun in url_types:
        match = re.search(pattern, url)
        if match:
            return fun(match)
    else:
        return os.path.dirname(url)


def strip_query_and_fragment(path):
    try:
        components = urlsplit(path)
        stripped = components[:3] + (None, None)

        query, frag = components[3:5]
        suffix = ''
        if query:
            suffix += '?' + query
        if frag:
            suffix += '#' + frag

        return (urlunsplit(stripped), suffix)

    except ValueError:
        tty.debug("Got error parsing path %s" % path)
        return (path, '')  # Ignore URL parse errors here


def split_url_extension(path):
    """Some URLs have a query string, e.g.:

          1. https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true
          2. http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin.tar.gz

       In (1), the query string needs to be stripped to get at the
       extension, but in (2), the filename is IN a single final query
       argument.

       This strips the URL into three pieces: prefix, ext, and suffix.
       The suffix contains anything that was stripped off the URL to
       get at the file extension.  In (1), it will be '?raw=true', but
       in (2), it will be empty. e.g.:

           1. ('https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7', '.tgz', '?raw=true')
           2. ('http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin',
               '.tar.gz', None)
    """
    prefix, ext, suffix = path, '', ''

    # Strip off sourceforge download suffix.
    match = re.search(r'((?:sourceforge.net|sf.net)/.*)(/download)$', path)
    if match:
        prefix, suffix = match.groups()

    ext = comp.extension(prefix)
    if ext is not None:
        prefix = comp.strip_extension(prefix)

    else:
        prefix, suf = strip_query_and_fragment(prefix)
        ext = comp.extension(prefix)
        prefix = comp.strip_extension(prefix)
        suffix = suf + suffix
        if ext is None:
            ext = ''

    return prefix, ext, suffix


def determine_url_file_extension(path):
    """This returns the type of archive a URL refers to.  This is
       sometimes confusing because of URLs like:

           (1) https://github.com/petdance/ack/tarball/1.93_02

       Where the URL doesn't actually contain the filename.  We need
       to know what type it is so that we can appropriately name files
       in mirrors.
    """
    match = re.search(r'github.com/.+/(zip|tar)ball/', path)
    if match:
        if match.group(1) == 'zip':
            return 'zip'
        elif match.group(1) == 'tar':
            return 'tar.gz'

    prefix, ext, suffix = split_url_extension(path)
    return ext


def parse_version_offset(path):
    """Try to extract a version string from a filename or URL.  This is taken
       largely from Homebrew's Version class."""
    original_path = path

    path, ext, suffix = split_url_extension(path)

    # Allow matches against the basename, to avoid including parent
    # dirs in version name Remember the offset of the stem in the path
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
        (r'github.com/[^/]+/[^/]+/archive/v?(\d+(?:\.\d+)*)$', path),

        # e.g. https://github.com/erlang/otp/tarball/OTP_R15B01 (erlang style)
        (r'[-_](R\d+[AB]\d*(-\d+)?)', path),

        # e.g., https://github.com/hpc/libcircle/releases/download/0.2.1-rc.1/libcircle-0.2.1-rc.1.tar.gz
        # e.g.,
        # https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz
        (r'github.com/[^/]+/[^/]+/releases/download/v?([^/]+)/.*$', path),

        # e.g. boost_1_39_0
        (r'((\d+_)+\d+)$', stem),

        # e.g. foobar-4.5.1-1
        # e.g. ruby-1.9.1-p243
        (r'-((\d+\.)*\d\.\d+-(p|rc|RC)?\d+)(?:[-._](?:bin|dist|stable|src|sources))?$', stem),  # noqa

        # e.g. lame-398-1
        (r'-((\d)+-\d)', stem),

        # e.g. foobar_1.2-3
        (r'_((\d+\.)+\d+(-\d+)?[a-z]?)', stem),

        # e.g. foobar-4.5.1
        (r'-((\d+\.)*\d+)$', stem),

        # e.g. foobar-4.5.1b, foobar4.5RC, foobar.v4.5.1b
        (r'[-._]?v?((\d+\.)*\d+[-._]?([a-z]|rc|RC|tp|TP?)\d*)$', stem),

        # e.g. foobar-4.5.0-beta1, or foobar-4.50-beta
        (r'-((\d+\.)*\d+-beta(\d+)?)$', stem),

        # e.g. foobar4.5.1
        (r'((\d+\.)*\d+)$', stem),

        # e.g. foobar-4.5.0-bin
        (r'-((\d+\.)+\d+[a-z]?)[-._](bin|dist|stable|src|sources?)$', stem),

        # e.g. dash_0.5.5.1.orig.tar.gz (Debian style)
        (r'_((\d+\.)+\d+[a-z]?)[.]orig$', stem),

        # e.g. http://www.openssl.org/source/openssl-0.9.8s.tar.gz
        (r'-v?([^-]+(-alpha|-beta)?)', stem),

        # e.g. astyle_1.23_macosx.tar.gz
        (r'_([^_]+(_alpha|_beta)?)', stem),

        # e.g. http://mirrors.jenkins-ci.org/war/1.486/jenkins.war
        (r'\/(\d\.\d+)\/', path),

        # e.g. http://www.ijg.org/files/jpegsrc.v8d.tar.gz
        (r'\.v(\d+[a-z]?)', stem)]

    for i, vtype in enumerate(version_types):
        regex, match_string = vtype
        match = re.search(regex, match_string)
        if match and match.group(1) is not None:
            version = match.group(1)
            start   = match.start(1)

            # if we matched from the basename, then add offset in.
            if match_string is stem:
                start += offset

            return version, start, len(version)

    raise UndetectableVersionError(original_path)


def parse_version(path):
    """Given a URL or archive name, extract a version from it and return
       a version object.
    """
    ver, start, l = parse_version_offset(path)
    return Version(ver)


def parse_name_offset(path, v=None):
    if v is None:
        v = parse_version(path)

    path, ext, suffix = split_url_extension(path)

    # Allow matching with either path or stem, as with the version.
    stem = os.path.basename(path)
    offset = len(path) - len(stem)

    name_types = [
        (r'/sourceforge/([^/]+)/', path),
        (r'github.com/[^/]+/[^/]+/releases/download/%s/(.*)-%s$' %
         (v, v), path),
        (r'/([^/]+)/(tarball|zipball)/', path),
        (r'/([^/]+)[_.-](bin|dist|stable|src|sources)[_.-]%s' % v, path),
        (r'github.com/[^/]+/([^/]+)/archive', path),

        (r'([^/]+)[_.-]v?%s' % v, stem),   # prefer the stem
        (r'([^/]+)%s' % v, stem),

        # accept the path if name is not in stem.
        (r'/([^/]+)[_.-]v?%s' % v, path),
        (r'/([^/]+)%s' % v, path),

        (r'^([^/]+)[_.-]v?%s' % v, path),
        (r'^([^/]+)%s' % v, path)]

    for i, name_type in enumerate(name_types):
        regex, match_string = name_type
        match = re.search(regex, match_string)
        if match:
            name  = match.group(1)
            start = match.start(1)

            # if we matched from the basename, then add offset in.
            if match_string is stem:
                start += offset

            return name, start, len(name)

    raise UndetectableNameError(path)


def parse_name(path, ver=None):
    name, start, l = parse_name_offset(path, ver)
    return name


def parse_name_and_version(path):
    ver = parse_version(path)
    name = parse_name(path, ver)
    return (name, ver)


def insensitize(string):
    """Change upper and lowercase letters to be case insensitive in
       the provided string.  e.g., 'a' because '[Aa]', 'B' becomes
       '[bB]', etc.  Use for building regexes."""
    def to_ins(match):
        char = match.group(1)
        return '[%s%s]' % (char.lower(), char.upper())
    return re.sub(r'([a-zA-Z])', to_ins, string)


def cumsum(elts, init=0, fn=lambda x: x):
    """Return cumulative sum of result of fn on each element in elts."""
    sums = []
    s = init
    for i, e in enumerate(elts):
        sums.append(s)
        s += fn(e)
    return sums


def substitution_offsets(path):
    """This returns offsets for substituting versions and names in the
       provided path.  It is a helper for substitute_version().
    """
    # Get name and version offsets
    try:
        ver,  vs, vl = parse_version_offset(path)
        name, ns, nl = parse_name_offset(path, ver)
    except UndetectableNameError:
        return (None, -1, -1, (), ver, vs, vl, (vs,))
    except UndetectableVersionError:
        return (None, -1, -1, (), None, -1, -1, ())

    # protect extensions like bz2 from getting inadvertently
    # considered versions.
    path = comp.strip_extension(path)

    # Construct a case-insensitive regular expression for the package name.
    name_re = '(%s)' % insensitize(name)

    # Split the string apart by things that match the name so that if the
    # name contains numbers or things that look like versions, we don't
    # accidentally substitute them with a version.
    name_parts = re.split(name_re, path)

    offsets = cumsum(name_parts, 0, len)
    name_offsets = offsets[1::2]

    ver_offsets = []
    for i in xrange(0, len(name_parts), 2):
        vparts = re.split(ver, name_parts[i])
        voffsets = cumsum(vparts, offsets[i], len)
        ver_offsets.extend(voffsets[1::2])

    return (name, ns, nl, tuple(name_offsets),
            ver,  vs, vl, tuple(ver_offsets))


def wildcard_version(path):
    """Find the version in the supplied path, and return a regular expression
       that will match this path with any version in its place.
    """
    # Get name and version, so we can treat them specially
    name, v = parse_name_and_version(path)

    path, ext, suffix = split_url_extension(path)

    # Construct a case-insensitive regular expression for the package name.
    name_re = '(%s)' % insensitize(name)

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
    result = ''.join(name_parts)
    if ext:
        result += '.' + ext
    result += suffix
    return result


def substitute_version(path, new_version):
    """Given a URL or archive name, find the version in the path and
       substitute the new version for it.  Replace all occurrences of
       the version *if* they don't overlap with the package name.

       Simple example::
         substitute_version('http://www.mr511.de/software/libelf-0.8.13.tar.gz', '2.9.3')
         ->'http://www.mr511.de/software/libelf-2.9.3.tar.gz'

       Complex examples::
         substitute_version('http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.0.tar.gz', 2.1)
         -> 'http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.1.tar.gz'

         # In this string, the "2" in mvapich2 is NOT replaced.
         substitute_version('http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.tar.gz', 2.1)
         -> 'http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.1.tar.gz'

    """
    (name, ns, nl, noffs,
     ver,  vs, vl, voffs) = substitution_offsets(path)

    new_path = ''
    last = 0
    for vo in voffs:
        new_path += path[last:vo]
        new_path += str(new_version)
        last = vo + vl

    new_path += path[last:]
    return new_path


def color_url(path, **kwargs):
    """Color the parts of the url according to Spack's parsing.

       Colors are:
          Cyan: The version found by parse_version_offset().
          Red:  The name found by parse_name_offset().

          Green:   Instances of version string from substitute_version().
          Magenta: Instances of the name (protected from substitution).

       Optional args:
          errors=True    Append parse errors at end of string.
          subs=True      Color substitutions as well as parsed name/version.

    """
    errors = kwargs.get('errors', False)
    subs   = kwargs.get('subs', False)

    (name, ns, nl, noffs,
     ver,  vs, vl, voffs) = substitution_offsets(path)

    nends = [no + nl - 1 for no in noffs]
    vends = [vo + vl - 1 for vo in voffs]

    nerr = verr = 0
    out = StringIO()
    for i in range(len(path)):
        if i == vs:
            out.write('@c')
            verr += 1
        elif i == ns:
            out.write('@r')
            nerr += 1
        elif subs:
            if i in voffs:
                out.write('@g')
            elif i in noffs:
                out.write('@m')

        out.write(path[i])

        if i == vs + vl - 1:
            out.write('@.')
            verr += 1
        elif i == ns + nl - 1:
            out.write('@.')
            nerr += 1
        elif subs:
            if i in vends or i in nends:
                out.write('@.')

    if errors:
        if nerr == 0:
            out.write(" @r{[no name]}")
        if verr == 0:
            out.write(" @r{[no version]}")
        if nerr == 1:
            out.write(" @r{[incomplete name]}")
        if verr == 1:
            out.write(" @r{[incomplete version]}")

    return colorize(out.getvalue())


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
