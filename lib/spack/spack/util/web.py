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
import re
import sys
import subprocess
import urllib2, cookielib
import urlparse
from multiprocessing import Pool
from HTMLParser import HTMLParser, HTMLParseError

import llnl.util.tty as tty

import spack
import spack.error
from spack.util.compression import ALLOWED_ARCHIVE_TYPES

# Timeout in seconds for web requests
TIMEOUT = 10


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


def _spider(args):
    """_spider(url, depth, max_depth)

       Fetches URL and any pages it links to up to max_depth.  depth should
       initially be 1, and max_depth includes the root.  This function will
       print out a warning only if the root can't be fetched; it ignores
       errors with pages that the root links to.

       This will return a list of the pages fetched, in no particular order.

       Takes args as a tuple b/c it's intended to be used by a multiprocessing
       pool.  Firing off all the child links at once makes the fetch MUCH
       faster for pages with lots of children.
    """
    url, visited, root, opener, depth, max_depth, raise_on_error = args

    pages = {}
    try:
        # Make a HEAD request first to check the content type.  This lets
        # us ignore tarballs and gigantic files.
        # It would be nice to do this with the HTTP Accept header to avoid
        # one round-trip.  However, most servers seem to ignore the header
        # if you ask for a tarball with Accept: text/html.
        req = urllib2.Request(url)
        req.get_method = lambda: "HEAD"
        resp = urllib2.urlopen(req, timeout=TIMEOUT)

        if not "Content-type" in resp.headers:
            tty.debug("ignoring page " + url)
            return pages

        if not resp.headers["Content-type"].startswith('text/html'):
            tty.debug("ignoring page " + url + " with content type " +
                      resp.headers["Content-type"])
            return pages

        # Do the real GET request when we know it's just HTML.
        req.get_method = lambda: "GET"
        response = urllib2.urlopen(req, timeout=TIMEOUT)
        response_url = response.geturl()

        # Read the page and and stick it in the map we'll return
        page = response.read()
        pages[response_url] = page

        # If we're not at max depth, parse out the links in the page
        if depth < max_depth:
            link_parser = LinkParser()
            subcalls = []
            link_parser.feed(page)

            while link_parser.links:
                raw_link = link_parser.links.pop()

                # Skip stuff that looks like an archive
                if any(raw_link.endswith(suf) for suf in ALLOWED_ARCHIVE_TYPES):
                    continue

                # Evaluate the link relative to the page it came from.
                abs_link = urlparse.urljoin(response_url, raw_link)

                # Skip things outside the root directory
                if not abs_link.startswith(root):
                    continue

                # Skip already-visited links
                if abs_link in visited:
                    continue

                subcalls.append((abs_link, visited, root, None, depth+1, max_depth, raise_on_error))
                visited.add(abs_link)

            if subcalls:
                try:
                    pool = Pool(processes=len(subcalls))
                    dicts = pool.map(_spider, subcalls)
                    for d in dicts:
                        pages.update(d)
                finally:
                    pool.terminate()
                    pool.join()

    except urllib2.URLError, e:
        tty.debug(e)
        if raise_on_error:
            raise spack.error.NoNetworkConnectionError(str(e), url)

    except HTMLParseError, e:
        # This error indicates that Python's HTML parser sucks.
        msg = "Got an error parsing HTML."

        # Pre-2.7.3 Pythons in particular have rather prickly HTML parsing.
        if sys.version_info[:3] < (2,7,3):
            msg += " Use Python 2.7.3 or newer for better HTML parsing."

        tty.warn(msg, url, "HTMLParseError: " + str(e))

    except Exception, e:
        # Other types of errors are completely ignored, except in debug mode.
        tty.debug("Error in _spider: %s" % e)

    return pages


def get_pages(root_url, **kwargs):
    """Gets web pages from a root URL.
       If depth is specified (e.g., depth=2), then this will also fetches pages
       linked from the root and its children up to depth.

       This will spawn processes to fetch the children, for much improved
       performance over a sequential fetch.
    """
    max_depth = kwargs.setdefault('depth', 1)
    pages =  _spider((root_url, set(), root_url, None, 1, max_depth, False))
    return pages
