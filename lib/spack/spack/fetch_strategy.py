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
Fetch strategies are used to download source code into a staging area
in order to build it.  They need to define the following methods:

    * fetch()
        This should attempt to download/check out source from somewhere.
    * check()
        Apply a checksum to the downloaded source code, e.g. for an archive.
        May not do anything if the fetch method was safe to begin with.
    * expand()
        Expand (e.g., an archive) downloaded file to source.
    * reset()
        Restore original state of downloaded code.  Used by clean commands.
        This may just remove the expanded source and re-expand an archive,
        or it may run something like git reset --hard.
"""
import os
import re
import shutil

import llnl.util.tty as tty

import spack
import spack.error
import spack.util.crypto as crypto
from spack.util.compression import decompressor_for


class FetchStrategy(object):
    def __init__(self):
        # The stage is initialized late, so that fetch strategies can be constructed
        # at package construction time.  This is where things will be fetched.
        self.stage = None


    def set_stage(self, stage):
        """This is called by Stage before any of the fetching
           methods are called on the stage."""
        self.stage = stage


    # Subclasses need to implement tehse methods
    def fetch(self): pass    # Return True on success, False on fail
    def check(self): pass
    def expand(self): pass
    def reset(self): pass
    def __str__(self): pass



class URLFetchStrategy(FetchStrategy):

    def __init__(self, url, digest=None):
        super(URLFetchStrategy, self).__init__()
        self.url = url
        self.digest = digest


    def fetch(self):
        assert(self.stage)

        self.stage.chdir()

        if self.archive_file:
            tty.msg("Already downloaded %s." % self.archive_file)
            return

        tty.msg("Trying to fetch from %s" % self.url)

        # Run curl but grab the mime type from the http headers
        headers = spack.curl('-#',        # status bar
                             '-O',        # save file to disk
                             '-D', '-',   # print out HTML headers
                             '-L', self.url,
                             return_output=True, fail_on_error=False)

        if spack.curl.returncode != 0:
            # clean up archive on failure.
            if self.archive_file:
                os.remove(self.archive_file)

            if spack.curl.returncode == 60:
                # This is a certificate error.  Suggest spack -k
                raise FailedDownloadError(
                    self.url,
                    "Curl was unable to fetch due to invalid certificate. "
                    "This is either an attack, or your cluster's SSL configuration "
                    "is bad.  If you believe your SSL configuration is bad, you "
                    "can try running spack -k, which will not check SSL certificates."
                    "Use this at your own risk.")

        # Check if we somehow got an HTML file rather than the archive we
        # asked for.  We only look at the last content type, to handle
        # redirects properly.
        content_types = re.findall(r'Content-Type:[^\r\n]+', headers)
        if content_types and 'text/html' in content_types[-1]:
            tty.warn("The contents of " + self.archive_file + " look like HTML.",
                     "The checksum will likely be bad.  If it is, you can use",
                     "'spack clean --dist' to remove the bad archive, then fix",
                     "your internet gateway issue and install again.")

        if not self.archive_file:
            raise FailedDownloadError(self.url)


    @property
    def archive_file(self):
        """Path to the source archive within this stage directory."""
        assert(self.stage)
        path = os.path.join(self.stage.path, os.path.basename(self.url))
        return path if os.path.exists(path) else None


    def expand(self):
        assert(self.stage)
        tty.msg("Staging archive: %s" % self.archive_file)

        self.stage.chdir()
        if not self.archive_file:
            raise NoArchiveFileError("URLFetchStrategy couldn't find archive file",
                                     "Failed on expand() for URL %s" % self.url)

        print self.archive_file

        decompress = decompressor_for(self.archive_file)
        decompress(self.archive_file)


    def check(self):
        """Check the downloaded archive against a checksum digest.
           No-op if this stage checks code out of a repository."""
        assert(self.stage)
        if not self.digest:
            raise NoDigestError("Attempt to check URLFetchStrategy with no digest.")
        checker = crypto.Checker(digest)
        if not checker.check(self.archive_file):
            raise ChecksumError(
                "%s checksum failed for %s." % (checker.hash_name, self.archive_file),
                "Expected %s but got %s." % (digest, checker.sum))


    def reset(self):
        """Removes the source path if it exists, then re-expands the archive."""
        assert(self.stage)
        if not self.archive_file:
            raise NoArchiveFileError("Tried to reset URLFetchStrategy before fetching",
                                     "Failed on reset() for URL %s" % self.url)
        if self.stage.source_path:
            shutil.rmtree(self.stage.source_path, ignore_errors=True)
        self.expand()


    def __str__(self):
        return self.url



class GitFetchStrategy(FetchStrategy):
    pass


class SvnFetchStrategy(FetchStrategy):
    pass


def strategy_for_url(url):
    """Given a URL, find an appropriate fetch strategy for it.
       Currently just gives you a URLFetchStrategy that uses curl.

       TODO: make this return appropriate fetch strategies for other
             types of URLs.
    """
    return URLFetchStrategy(url)


class FetchStrategyError(spack.error.SpackError):
    def __init__(self, msg, long_msg):
        super(FetchStrategyError, self).__init__(msg, long_msg)


class FailedDownloadError(FetchStrategyError):
    """Raised wen a download fails."""
    def __init__(self, url, msg=""):
        super(FailedDownloadError, self).__init__(
            "Failed to fetch file from URL: %s" % url, msg)
        self.url = url


class NoArchiveFileError(FetchStrategyError):
    def __init__(self, msg, long_msg):
        super(NoArchiveFileError, self).__init__(msg, long_msg)


class NoDigestError(FetchStrategyError):
    def __init__(self, msg, long_msg):
        super(NoDigestError, self).__init__(msg, long_msg)


