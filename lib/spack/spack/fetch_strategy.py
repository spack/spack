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
from spack.version import Version, ver
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


    # Subclasses need to implement these methods
    def fetch(self): pass    # Return True on success, False on fail
    def check(self): pass
    def expand(self): pass
    def reset(self): pass
    def __str__(self):
        return "FetchStrategy.__str___"

    # This method is used to match fetch strategies to version()
    # arguments in packages.
    @classmethod
    def match(kwargs):
        return any(k in kwargs for k in self.attributes)


class URLFetchStrategy(FetchStrategy):
    attributes = ('url', 'md5')

    def __init__(self, url=None, digest=None, **kwargs):
        super(URLFetchStrategy, self).__init__()

        # If URL or digest are provided in the kwargs, then prefer
        # those values.
        self.url = kwargs.get('url', None)
        if not self.url: self.url = url

        self.digest = kwargs.get('md5', None)
        if not self.digest: self.digest = digest

        if not self.url:
            raise ValueError("URLFetchStrategy requires a url for fetching.")


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
        if self.url:
            return self.url
        else:
            return "URLFetchStrategy <no url>"


class VCSFetchStrategy(FetchStrategy):
    def __init__(self, name):
        super(VCSFetchStrategy, self).__init__()
        self.name = name


    def check(self):
        assert(self.stage)
        tty.msg("No check needed when fetching with %s." % self.name)

    def expand(self):
        assert(self.stage)
        tty.debug("Source fetched with %s is already expanded." % self.name)



class GitFetchStrategy(VCSFetchStrategy):
    attributes = ('git', 'ref', 'tag', 'branch')

    def __init__(self, **kwargs):
        super(GitFetchStrategy, self).__init__("git")
        self.url = kwargs.get('git', None)
        if not self.url:
            raise ValueError("GitFetchStrategy requires git argument.")

        if sum((k in kwargs for k in ('ref', 'tag', 'branch'))) > 1:
            raise FetchStrategyError(
                "Git requires exactly one ref, branch, or tag.")

        self._git = None
        self.ref    = kwargs.get('ref', None)
        self.branch = kwargs.get('branch', None)
        if not self.branch:
            self.branch = kwargs.get('tag', None)


    @property
    def git_version(self):
        git = which('git', required=True)
        vstring = git('--version', return_output=True).lstrip('git version ')
        return Version(vstring)


    @property
    def git(self):
        if not self._git:
            self._git = which('git', required=True)
        return self._git


    def fetch(self):
        assert(self.stage)
        self.stage.chdir()

        if self.stage.source_path:
            tty.msg("Already fetched %s." % self.source_path)
            return

        tty.msg("Trying to clone git repository: %s" % self.url)


        if self.ref:
            # Need to do a regular clone and check out everything if
            # they asked for a particular ref.
            git('clone', self.url)
            self.chdir_to_source()
            git('checkout', self.ref)

        else:
            # Can be more efficient if not checking out a specific ref.
            args = ['clone']

            # If we want a particular branch ask for it.
            if self.branch:
                args.extend(['--branch', self.branch])

            # Try to be efficient if we're using a new enough git.
            # This checks out only one branch's history
            if self.git_version > ver('1.7.10'):
                args.append('--single-branch')

            args.append(self.url)
            git(*args)
            self.chdir_to_source()


    def reset(self):
        assert(self.stage)
        git = which('git', required=True)

        self.stage.chdir_to_source()
        git('checkout', '.')
        git('clean', '-f')


    def __str__(self):
        return self.url


class SvnFetchStrategy(FetchStrategy):
    attributes = ('svn', 'rev', 'revision')
    pass


def from_url(url):
    """Given a URL, find an appropriate fetch strategy for it.
       Currently just gives you a URLFetchStrategy that uses curl.

       TODO: make this return appropriate fetch strategies for other
             types of URLs.
    """
    return URLFetchStrategy(url)


def args_are_for(args, fetcher):
    return any(arg in args for arg in fetcher.attributes)


def from_args(args, pkg):
    """Determine a fetch strategy based on the arguments supplied to
       version() in the package description."""
    fetchers = (URLFetchStrategy, GitFetchStrategy)
    for fetcher in fetchers:
        if args_are_for(args, fetcher):
            attrs = {}
            for attr in fetcher.attributes:
                default = getattr(pkg, attr, None)
                if default:
                    attrs[attr] = default

            attrs.update(args)
            return fetcher(**attrs)

    return None

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


class InvalidArgsError(FetchStrategyError):
    def __init__(self, msg, long_msg):
        super(InvalidArgsError, self).__init__(msg, long_msg)

