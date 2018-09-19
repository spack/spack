##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from __future__ import print_function

import re
import os
import ssl
import sys
import traceback
import hashlib

from six.moves.urllib.request import urlopen, Request
from six.moves.urllib.error import URLError
from six.moves.urllib.parse import urljoin
import multiprocessing.pool

try:
    # Python 2 had these in the HTMLParser package.
    from HTMLParser import HTMLParser, HTMLParseError
except ImportError:
    # In Python 3, things moved to html.parser
    from html.parser import HTMLParser

    # Also, HTMLParseError is deprecated and never raised.
    class HTMLParseError(Exception):
        pass

import llnl.util.tty as tty

import spack.config
import spack.cmd
import spack.url
import spack.stage
import spack.error
import spack.util.crypto
from spack.util.compression import ALLOWED_ARCHIVE_TYPES


# Timeout in seconds for web requests
_timeout = 10


class LinkParser(HTMLParser):
    """This parser just takes an HTML page and strips out the hrefs on the
       links.  Good enough for a really simple spider. """

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, val in attrs:
                if attr == 'href':
                    self.links.append(val)


class NonDaemonProcess(multiprocessing.Process):
    """Process tha allows sub-processes, so pools can have sub-pools."""
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NonDaemonPool(multiprocessing.pool.Pool):
    """Pool that uses non-daemon processes"""
    Process = NonDaemonProcess


def _spider(url, visited, root, depth, max_depth, raise_on_error):
    """Fetches URL and any pages it links to up to max_depth.

       depth should initially be zero, and max_depth is the max depth of
       links to follow from the root.

       Prints out a warning only if the root can't be fetched; it ignores
       errors with pages that the root links to.

       Returns a tuple of:
       - pages: dict of pages visited (URL) mapped to their full text.
       - links: set of links encountered while visiting the pages.
    """
    pages = {}     # dict from page URL -> text content.
    links = set()  # set of all links seen on visited pages.

    # root may end with index.html -- chop that off.
    if root.endswith('/index.html'):
        root = re.sub('/index.html$', '', root)

    try:
        context = None
        verify_ssl = spack.config.get('config:verify_ssl')
        pyver = sys.version_info
        if (pyver < (2, 7, 9) or (3,) < pyver < (3, 4, 3)):
            if verify_ssl:
                tty.warn("Spack will not check SSL certificates. You need to "
                         "update your Python to enable certificate "
                         "verification.")
        elif verify_ssl:
            # We explicitly create default context to avoid error described in
            # https://blog.sucuri.net/2016/03/beware-unverified-tls-certificates-php-python.html
            context = ssl.create_default_context()
        else:
            context = ssl._create_unverified_context()

        # Make a HEAD request first to check the content type.  This lets
        # us ignore tarballs and gigantic files.
        # It would be nice to do this with the HTTP Accept header to avoid
        # one round-trip.  However, most servers seem to ignore the header
        # if you ask for a tarball with Accept: text/html.
        req = Request(url)
        req.get_method = lambda: "HEAD"
        resp = _urlopen(req, timeout=_timeout, context=context)

        if "Content-type" not in resp.headers:
            tty.debug("ignoring page " + url)
            return pages, links

        if not resp.headers["Content-type"].startswith('text/html'):
            tty.debug("ignoring page " + url + " with content type " +
                      resp.headers["Content-type"])
            return pages, links

        # Do the real GET request when we know it's just HTML.
        req.get_method = lambda: "GET"
        response = _urlopen(req, timeout=_timeout, context=context)
        response_url = response.geturl()

        # Read the page and and stick it in the map we'll return
        page = response.read().decode('utf-8')
        pages[response_url] = page

        # Parse out the links in the page
        link_parser = LinkParser()
        subcalls = []
        link_parser.feed(page)

        while link_parser.links:
            raw_link = link_parser.links.pop()
            abs_link = urljoin(response_url, raw_link.strip())

            links.add(abs_link)

            # Skip stuff that looks like an archive
            if any(raw_link.endswith(suf) for suf in ALLOWED_ARCHIVE_TYPES):
                continue

            # Skip things outside the root directory
            if not abs_link.startswith(root):
                continue

            # Skip already-visited links
            if abs_link in visited:
                continue

            # If we're not at max depth, follow links.
            if depth < max_depth:
                subcalls.append((abs_link, visited, root,
                                 depth + 1, max_depth, raise_on_error))
                visited.add(abs_link)

        if subcalls:
            pool = NonDaemonPool(processes=len(subcalls))
            try:
                results = pool.map(_spider_wrapper, subcalls)

                for sub_pages, sub_links in results:
                    pages.update(sub_pages)
                    links.update(sub_links)

            finally:
                pool.terminate()
                pool.join()

    except URLError as e:
        tty.debug(e)

        if hasattr(e, 'reason') and isinstance(e.reason, ssl.SSLError):
            tty.warn("Spack was unable to fetch url list due to a certificate "
                     "verification problem. You can try running spack -k, "
                     "which will not check SSL certificates. Use this at your "
                     "own risk.")

        if raise_on_error:
            raise NoNetworkConnectionError(str(e), url)

    except HTMLParseError as e:
        # This error indicates that Python's HTML parser sucks.
        msg = "Got an error parsing HTML."

        # Pre-2.7.3 Pythons in particular have rather prickly HTML parsing.
        if sys.version_info[:3] < (2, 7, 3):
            msg += " Use Python 2.7.3 or newer for better HTML parsing."

        tty.warn(msg, url, "HTMLParseError: " + str(e))

    except Exception as e:
        # Other types of errors are completely ignored, except in debug mode.
        tty.debug("Error in _spider: %s:%s" % (type(e), e),
                  traceback.format_exc())

    return pages, links


def _spider_wrapper(args):
    """Wrapper for using spider with multiprocessing."""
    return _spider(*args)


def _urlopen(*args, **kwargs):
    """Wrapper for compatibility with old versions of Python."""
    # We don't pass 'context' parameter to urlopen because it
    # was introduces only starting versions 2.7.9 and 3.4.3 of Python.
    if 'context' in kwargs and kwargs['context'] is None:
        del kwargs['context']
    return urlopen(*args, **kwargs)


def spider(root_url, depth=0):
    """Gets web pages from a root URL.

       If depth is specified (e.g., depth=2), then this will also follow
       up to <depth> levels of links from the root.

       This will spawn processes to fetch the children, for much improved
       performance over a sequential fetch.

    """
    pages, links = _spider(root_url, set(), root_url, 0, depth, False)
    return pages, links


def find_versions_of_archive(archive_urls, list_url=None, list_depth=0):
    """Scrape web pages for new versions of a tarball.

    Arguments:
      archive_urls:
          URL or sequence of URLs for different versions of a
          package. Typically these are just the tarballs from the package
          file itself.  By default, this searches the parent directories
          of archives.

    Keyword Arguments:
      list_url:
          URL for a listing of archives.  Spack wills scrape these
          pages for download links that look like the archive URL.

      list_depth:
          Max depth to follow links on list_url pages. Default 0.

    """
    if not isinstance(archive_urls, (list, tuple)):
        archive_urls = [archive_urls]

    # Generate a list of list_urls based on archive urls and any
    # explicitly listed list_url in the package
    list_urls = set()
    if list_url:
        list_urls.add(list_url)
    for aurl in archive_urls:
        list_urls.add(spack.url.find_list_url(aurl))

    # Add '/' to the end of the URL. Some web servers require this.
    additional_list_urls = set()
    for lurl in list_urls:
        if not lurl.endswith('/'):
            additional_list_urls.add(lurl + '/')
    list_urls.update(additional_list_urls)

    # Grab some web pages to scrape.
    pages = {}
    links = set()
    for lurl in list_urls:
        pg, lnk = spider(lurl, depth=list_depth)
        pages.update(pg)
        links.update(lnk)

    # Scrape them for archive URLs
    regexes = []
    for aurl in archive_urls:
        # This creates a regex from the URL with a capture group for
        # the version part of the URL.  The capture group is converted
        # to a generic wildcard, so we can use this to extract things
        # on a page that look like archive URLs.
        url_regex = spack.url.wildcard_version(aurl)

        # We'll be a bit more liberal and just look for the archive
        # part, not the full path.
        url_regex = os.path.basename(url_regex)

        # We need to add a / to the beginning of the regex to prevent
        # Spack from picking up similarly named packages like:
        #   https://cran.r-project.org/src/contrib/pls_2.6-0.tar.gz
        #   https://cran.r-project.org/src/contrib/enpls_5.7.tar.gz
        #   https://cran.r-project.org/src/contrib/autopls_1.3.tar.gz
        #   https://cran.r-project.org/src/contrib/matrixpls_1.0.4.tar.gz
        url_regex = '/' + url_regex

        # We need to add a $ anchor to the end of the regex to prevent
        # Spack from picking up signature files like:
        #   .asc
        #   .md5
        #   .sha256
        #   .sig
        # However, SourceForge downloads still need to end in '/download'.
        url_regex += '(\/download)?$'

        regexes.append(url_regex)

    # Build a dict version -> URL from any links that match the wildcards.
    versions = {}
    for url in links:
        if any(re.search(r, url) for r in regexes):
            try:
                ver = spack.url.parse_version(url)
                versions[ver] = url
            except spack.url.UndetectableVersionError:
                continue

    return versions


def get_checksums_for_versions(
        url_dict, name, first_stage_function=None, keep_stage=False):
    """Fetches and checksums archives from URLs.

    This function is called by both ``spack checksum`` and ``spack
    create``.  The ``first_stage_function`` argument allows the caller to
    inspect the first downloaded archive, e.g., to determine the build
    system.

    Args:
        url_dict (dict): A dictionary of the form: version -> URL
        name (str): The name of the package
        first_stage_function (callable): function that takes a Stage and a URL;
            this is run on the stage of the first URL downloaded
        keep_stage (bool): whether to keep staging area when command completes

    Returns:
        (str): A multi-line string containing versions and corresponding hashes

    """
    sorted_versions = sorted(url_dict.keys(), reverse=True)

    # Find length of longest string in the list for padding
    max_len = max(len(str(v)) for v in sorted_versions)
    num_ver = len(sorted_versions)

    tty.msg("Found {0} version{1} of {2}:".format(
            num_ver, '' if num_ver == 1 else 's', name),
            "",
            *spack.cmd.elide_list(
                ["{0:{1}}  {2}".format(str(v), max_len, url_dict[v])
                 for v in sorted_versions]))
    print()

    archives_to_fetch = tty.get_number(
        "How many would you like to checksum?", default=1, abort='q')

    if not archives_to_fetch:
        tty.die("Aborted.")

    versions = sorted_versions[:archives_to_fetch]
    urls = [url_dict[v] for v in versions]

    tty.msg("Downloading...")
    version_hashes = []
    i = 0
    for url, version in zip(urls, versions):
        try:
            with spack.stage.Stage(url, keep=keep_stage) as stage:
                # Fetch the archive
                stage.fetch()
                if i == 0 and first_stage_function:
                    # Only run first_stage_function the first time,
                    # no need to run it every time
                    first_stage_function(stage, url)

                # Checksum the archive and add it to the list
                version_hashes.append((version, spack.util.crypto.checksum(
                    hashlib.sha256, stage.archive_file)))
                i += 1
        except spack.stage.FailedDownloadError:
            tty.msg("Failed to fetch {0}".format(url))
        except Exception as e:
            tty.msg("Something failed on {0}, skipping.".format(url),
                    "  ({0})".format(e))

    if not version_hashes:
        tty.die("Could not fetch any versions for {0}".format(name))

    # Find length of longest string in the list for padding
    max_len = max(len(str(v)) for v, h in version_hashes)

    # Generate the version directives to put in a package.py
    version_lines = "\n".join([
        "    version('{0}', {1}sha256='{2}')".format(
            v, ' ' * (max_len - len(str(v))), h) for v, h in version_hashes
    ])

    num_hash = len(version_hashes)
    tty.msg("Checksummed {0} version{1} of {2}".format(
        num_hash, '' if num_hash == 1 else 's', name))

    return version_lines


class SpackWebError(spack.error.SpackError):
    """Superclass for Spack web spidering errors."""


class VersionFetchError(SpackWebError):
    """Raised when we can't determine a URL to fetch a package."""


class NoNetworkConnectionError(SpackWebError):
    """Raised when an operation can't get an internet connection."""
    def __init__(self, message, url):
        super(NoNetworkConnectionError, self).__init__(
            "No network connection: " + str(message),
            "URL was: " + str(url))
        self.url = url
