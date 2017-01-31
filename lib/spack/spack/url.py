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

**Example:** when spack is given the following URL:

    https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.12/src/hdf-4.2.12.tar.gz

It can figure out that the package name is ``hdf``, and that it is at version
``4.2.12``. This is useful for making the creation of packages simple: a user
just supplies a URL and skeleton code is generated automatically.

Spack can also figure out that it can most likely download 4.2.6 at this URL:

    https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.6/src/hdf-4.2.6.tar.gz

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
    3. https://gitlab.kitware.com/vtk/vtk/repository/archive.tar.bz2?ref=v7.0.0

    In (1), the query string needs to be stripped to get at the
    extension, but in (2) & (3), the filename is IN a single final query
    argument.

    This strips the URL into three pieces: ``prefix``, ``ext``, and ``suffix``.
    The suffix contains anything that was stripped off the URL to
    get at the file extension.  In (1), it will be ``'?raw=true'``, but
    in (2), it will be empty. In (3) the suffix is a parameter that follows
    after the file extension, e.g.:

    1. ``('https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7', '.tgz', '?raw=true')``
    2. ``('http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin', '.tar.gz', None)``
    3. ``('https://gitlab.kitware.com/vtk/vtk/repository/archive', '.tar.bz2', '?ref=v7.0.0')``
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
    """Try to extract a version string from a filename or URL.

    :param str path: The filename or URL for the package

    :return: A tuple containing:
        version of the package,
        first index of version,
        length of version string,
        the index of the matching regex
        the matching regex

    :rtype: tuple

    :raises UndetectableVersionError: If the URL does not match any regexes
    """
    original_path = path

    # path:   The prefix of the URL, everything before the ext and suffix
    # ext:    The file extension
    # suffix: Any kind of query string that begins with a '?'
    path, ext, suffix = split_url_extension(path)

    # stem:   Everything from path after the final '/'
    stem = os.path.basename(path)
    offset = len(path) - len(stem)

    # List of the following format:
    #
    # [
    #     (regex, string),
    #     ...
    # ]
    #
    # The first regex that matches string will be used to determine
    # the version of the package. Thefore, hyperspecific regexes should
    # come first while generic, catch-all regexes should come last.
    version_regexes = [
        # GitHub tarballs, e.g. v1.2.3
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+)$', path),

        # e.g. https://github.com/sam-github/libnet/tarball/libnet-1.1.4
        (r'github.com/.+/(?:zip|tar)ball/.*-((\d+\.)+\d+)$', path),

        # e.g. https://github.com/isaacs/npm/tarball/v0.2.5-1
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+-(\d+))$', path),

        # e.g. https://github.com/petdance/ack/tarball/1.93_02
        (r'github.com/.+/(?:zip|tar)ball/v?((\d+\.)+\d+_(\d+))$', path),

        # Yorick is very special.
        # e.g. https://github.com/dhmunro/yorick/archive/y_2_2_04.tar.gz
        (r'github.com/[^/]+/yorick/archive/y_(\d+(?:_\d+)*)$', path),

        # e.g. https://github.com/hpc/lwgrp/archive/v1.0.1.tar.gz
        (r'github.com/[^/]+/[^/]+/archive/(?:release-)?v?(\w+(?:[.-]\w+)*)$', path),  # noqa

        # e.g. https://github.com/erlang/otp/tarball/OTP_R15B01 (erlang style)
        (r'[-_](R\d+[AB]\d*(-\d+)?)', path),

        # e.g., https://github.com/hpc/libcircle/releases/download/0.2.1-rc.1/libcircle-0.2.1-rc.1.tar.gz
        # e.g.,
        # https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz
        (r'github.com/[^/]+/[^/]+/releases/download/v?([^/]+)/.*$', path),

        # GitLab syntax:
        #   {baseUrl}{/organization}{/projectName}/repository/archive.{fileEnding}?ref={gitTag}
        #   as with github releases, we hope a version can be found in the
        #   git tag
        # Search dotted versions:
        #   e.g., https://gitlab.kitware.com/vtk/vtk/repository/archive.tar.bz2?ref=v7.0.0
        #   e.g., https://example.com/org/repo/repository/archive.tar.bz2?ref=SomePrefix-2.1.1
        #   e.g., http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1
        (r'\?ref=(?:.*-|v)*((\d+\.)+\d+).*$', suffix),
        (r'\?version=((\d+\.)+\d+)', suffix),

        # e.g. boost_1_39_0
        (r'((\d+_)+\d+)$', stem),

        # e.g. foobar-4.5.1-1
        # e.g. ruby-1.9.1-p243
        (r'-((\d+\.)*\d\.\d+-(p|rc|RC)?\d+)(?:[-._](?:bin|dist|stable|src|sources))?$', stem),  # noqa

        # e.g. lame-398-1
        (r'-((\d)+-\d)', stem),

        # e.g. foobar_1.2-3 or 3.98-1.4
        (r'_((\d+\.)+\d+(-(\d+(\.\d+)?))?[a-z]?)', stem),

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
        (r'\.v(\d+[a-z]?)', stem)
    ]

    for i, version_regex in enumerate(version_regexes):
        regex, match_string = version_regex
        match = re.search(regex, match_string)
        if match and match.group(1) is not None:
            version = match.group(1)
            start   = match.start(1)

            # if we matched from the basename, then add offset in.
            if match_string is stem:
                start += offset

            return version, start, len(version), i, regex

    raise UndetectableVersionError(original_path)


def parse_version(path):
    """Try to extract a version string from a filename or URL.

    :param str path: The filename or URL for the package

    :return: The version of the package
    :rtype: spack.version.Version

    :raises UndetectableVersionError: If the URL does not match any regexes
    """
    version, start, length, i, regex = parse_version_offset(path)
    return Version(version)


def parse_name_offset(path, v=None):
    """Try to determine the name of a package from its filename or URL.

    :param str path: The filename or URL for the package
    :param str v: The version of the package

    :return: A tuple containing:
        name of the package,
        first index of name,
        length of name,
        the index of the matching regex
        the matching regex

    :rtype: tuple

    :raises UndetectableNameError: If the URL does not match any regexes
    """
    original_path = path

    # We really need to know the version of the package
    # This helps us prevent collisions between the name and version
    if v is None:
        try:
            v = parse_version(path)
        except UndetectableVersionError:
            # Not all URLs contain a version. We still want to be able
            # to determine a name if possible.
            v = ''

    # path:   The prefix of the URL, everything before the ext and suffix
    # ext:    The file extension
    # suffix: Any kind of query string that begins with a '?'
    path, ext, suffix = split_url_extension(path)

    # stem:   Everything from path after the final '/'
    stem = os.path.basename(path)
    offset = len(path) - len(stem)

    # List of the following format:
    #
    # [
    #     (regex, string),
    #     ...
    # ]
    #
    # The first regex that matches string will be used to determine
    # the name of the package. Thefore, hyperspecific regexes should
    # come first while generic, catch-all regexes should come last.
    name_regexes = [
        (r'/sourceforge/([^/]+)/', path),
        (r'github.com/[^/]+/[^/]+/releases/download/%s/(.*)-%s$' %
         (v, v), path),
        (r'/([^/]+)/(tarball|zipball)/', path),
        (r'/([^/]+)[_.-](bin|dist|stable|src|sources)[_.-]%s' % v, path),
        (r'github.com/[^/]+/([^/]+)/archive', path),
        (r'[^/]+/([^/]+)/repository/archive', path),  # gitlab
        (r'([^/]+)/download.php', path),

        (r'([^/]+)[_.-]v?%s' % v, stem),   # prefer the stem
        (r'([^/]+)%s' % v, stem),

        # accept the path if name is not in stem.
        (r'/([^/]+)[_.-]v?%s' % v, path),
        (r'/([^/]+)%s' % v, path),

        (r'^([^/]+)[_.-]v?%s' % v, path),
        (r'^([^/]+)%s' % v, path)
    ]

    for i, name_regex in enumerate(name_regexes):
        regex, match_string = name_regex
        match = re.search(regex, match_string)
        if match:
            name  = match.group(1)
            start = match.start(1)

            # if we matched from the basename, then add offset in.
            if match_string is stem:
                start += offset

            # package names should be lowercase and separated by dashes.
            name = name.lower()
            name = re.sub('[_.]', '-', name)

            return name, start, len(name), i, regex

    raise UndetectableNameError(original_path)


def parse_name(path, ver=None):
    """Try to determine the name of a package from its filename or URL.

    :param str path: The filename or URL for the package
    :param str ver: The version of the package

    :return: The name of the package
    :rtype: str

    :raises UndetectableNameError: If the URL does not match any regexes
    """
    name, start, length, i, regex = parse_name_offset(path, ver)
    return name


def parse_name_and_version(path):
    """Try to determine the name of a package and extract its version
    from its filename or URL.

    :param str path: The filename or URL for the package

    :return: A tuple containing:
        The name of the package
        The version of the package

    :rtype: tuple
    """
    ver = parse_version(path)
    name = parse_name(path, ver)
    return (name, ver)


def insensitize(string):
    """Change upper and lowercase letters to be case insensitive in
       the provided string.  e.g., 'a' becomes '[Aa]', 'B' becomes
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
       provided path.  It is a helper for :func:`substitute_version`.
    """
    # Get name and version offsets
    try:
        ver,  vs, vl, vi, vregex = parse_version_offset(path)
        name, ns, nl, ni, nregex = parse_name_offset(path, ver)
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

    Simple example:

    .. code-block:: python

       substitute_version('http://www.mr511.de/software/libelf-0.8.13.tar.gz', '2.9.3')
       >>> 'http://www.mr511.de/software/libelf-2.9.3.tar.gz'

    Complex example:

    .. code-block:: python

       substitute_version('https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.12/src/hdf-4.2.12.tar.gz', '2.3')
       >>> 'https://www.hdfgroup.org/ftp/HDF/releases/HDF2.3/src/hdf-2.3.tar.gz'
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
       | Cyan: The version found by :func:`parse_version_offset`.
       | Red:  The name found by :func:`parse_name_offset`.

       | Green:   Instances of version string from :func:`substitute_version`.
       | Magenta: Instances of the name (protected from substitution).

    :param str path: The filename or URL for the package
    :keyword bool errors: Append parse errors at end of string.
    :keyword bool subs: Color substitutions as well as parsed name/version.
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
