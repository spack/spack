##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import os
import re
import shutil
import tempfile

import llnl.util.tty as tty
from llnl.util.filesystem import *

import spack
import spack.config
import spack.fetch_strategy as fs
import spack.error


STAGE_PREFIX = 'spack-stage-'


class Stage(object):
    """A Stage object manaages a directory where some source code is
       downloaded and built before being installed.  It handles
       fetching the source code, either as an archive to be expanded
       or by checking it out of a repository.  A stage's lifecycle
       looks like this:

       Stage()
         Constructor creates the stage directory.
       fetch()
         Fetch a source archive into the stage.
       expand_archive()
         Expand the source archive.
       <install>
         Build and install the archive.  This is handled by the Package class.
       destroy()
         Remove the stage once the package has been installed.

       If spack.use_tmp_stage is True, spack will attempt to create stages
       in a tmp directory.  Otherwise, stages are created directly in
       spack.stage_path.

       There are two kinds of stages: named and unnamed.  Named stages can
       persist between runs of spack, e.g. if you fetched a tarball but
       didn't finish building it, you won't have to fetch it again.

       Unnamed stages are created using standard mkdtemp mechanisms or
       similar, and are intended to persist for only one run of spack.
    """

    def __init__(self, url_or_fetch_strategy, **kwargs):
        """Create a stage object.
           Parameters:
             url_or_fetch_strategy
                 URL of the archive to be downloaded into this stage, OR
                 a valid FetchStrategy.

             name
                 If a name is provided, then this stage is a named stage
                 and will persist between runs (or if you construct another
                 stage object later).  If name is not provided, then this
                 stage will be given a unique name automatically.
        """
        # TODO: fetch/stage coupling needs to be reworked -- the logic
        # TODO: here is convoluted and not modular enough.
        if isinstance(url_or_fetch_strategy, basestring):
            self.fetcher = fs.from_url(url_or_fetch_strategy)
        elif isinstance(url_or_fetch_strategy, fs.FetchStrategy):
            self.fetcher = url_or_fetch_strategy
        else:
            raise ValueError("Can't construct Stage without url or fetch strategy")
        self.fetcher.set_stage(self)
        self.default_fetcher = self.fetcher  # self.fetcher can change with mirrors.
        self.skip_checksum_for_mirror = True # used for mirrored archives of repositories.

        self.name = kwargs.get('name')
        self.mirror_path = kwargs.get('mirror_path')

        self.tmp_root = find_tmp_root()

        self.path = None
        self._setup()


    def _cleanup_dead_links(self):
        """Remove any dead links in the stage directory."""
        for file in os.listdir(spack.stage_path):
            path = join_path(spack.stage_path, file)
            if os.path.islink(path):
                real_path = os.path.realpath(path)
                if not os.path.exists(path):
                    os.unlink(path)


    def _need_to_create_path(self):
        """Makes sure nothing weird has happened since the last time we
           looked at path.  Returns True if path already exists and is ok.
           Returns False if path needs to be created.
        """
        # Path doesn't exist yet.  Will need to create it.
        if not os.path.exists(self.path):
            return True

        # Path exists but points at something else.  Blow it away.
        if not os.path.isdir(self.path):
            os.unlink(self.path)
            return True

        # Path looks ok, but need to check the target of the link.
        if os.path.islink(self.path):
            real_path = os.path.realpath(self.path)
            real_tmp  = os.path.realpath(self.tmp_root)

            if spack.use_tmp_stage:
                # If we're using a tmp dir, it's a link, and it points at the right spot,
                # then keep it.
                if (real_path.startswith(real_tmp) and os.path.exists(real_path)):
                    return False
                else:
                    # otherwise, just unlink it and start over.
                    os.unlink(self.path)
                    return True

            else:
                # If we're not tmp mode, then it's a link and we want a directory.
                os.unlink(self.path)
                return True

        return False


    def _setup(self):
        """Creates the stage directory.
           If spack.use_tmp_stage is False, the stage directory is created
           directly under spack.stage_path.

           If spack.use_tmp_stage is True, this will attempt to create a
           stage in a temporary directory and link it into spack.stage_path.
           Spack will use the first writable location in spack.tmp_dirs to
           create a stage.  If there is no valid location in tmp_dirs, fall
           back to making the stage inside spack.stage_path.
        """
        # Create the top-level stage directory
        mkdirp(spack.stage_path)
        self._cleanup_dead_links()

        # If this is a named stage, then construct a named path.
        if self.name is not None:
            self.path = join_path(spack.stage_path, self.name)

        # If this is a temporary stage, them make the temp directory
        tmp_dir = None
        if self.tmp_root:
            if self.name is None:
                # Unnamed tmp root.  Link the path in
                tmp_dir = tempfile.mkdtemp('', STAGE_PREFIX, self.tmp_root)
                self.name = os.path.basename(tmp_dir)
                self.path = join_path(spack.stage_path, self.name)
                if self._need_to_create_path():
                    os.symlink(tmp_dir, self.path)

            else:
                if self._need_to_create_path():
                    tmp_dir = tempfile.mkdtemp('', STAGE_PREFIX, self.tmp_root)
                    os.symlink(tmp_dir, self.path)

        # if we're not using a tmp dir, create the stage directly in the
        # stage dir, rather than linking to it.
        else:
            if self.name is None:
                self.path = tempfile.mkdtemp('', STAGE_PREFIX, spack.stage_path)
                self.name = os.path.basename(self.path)
            else:
                if self._need_to_create_path():
                    mkdirp(self.path)

        # Make sure we can actually do something with the stage we made.
        ensure_access(self.path)


    @property
    def archive_file(self):
        """Path to the source archive within this stage directory."""
        paths = []
        if isinstance(self.fetcher, fs.URLFetchStrategy):
            paths.append(os.path.join(self.path, os.path.basename(self.fetcher.url)))

        if self.mirror_path:
            paths.append(os.path.join(self.path, os.path.basename(self.mirror_path)))

        for path in paths:
            if os.path.exists(path):
                return path
        else:
            return None


    @property
    def source_path(self):
        """Returns the path to the expanded/checked out source code
           within this fetch strategy's path.

           This assumes nothing else is going ot be put in the
           FetchStrategy's path.  It searches for the first
           subdirectory of the path it can find, then returns that.
        """
        for p in [os.path.join(self.path, f) for f in os.listdir(self.path)]:
            if os.path.isdir(p):
                return p
        return None


    def chdir(self):
        """Changes directory to the stage path.  Or dies if it is not set up."""
        if os.path.isdir(self.path):
            os.chdir(self.path)
        else:
            tty.die("Setup failed: no such directory: " + self.path)


    def fetch(self):
        """Downloads an archive or checks out code from a repository."""
        self.chdir()

        fetchers = [self.default_fetcher]

        # TODO: move mirror logic out of here and clean it up!
        # TODO: Or @alalazo may have some ideas about how to use a
        # TODO: CompositeFetchStrategy here.
        self.skip_checksum_for_mirror = True
        if self.mirror_path:
            urls = ["%s/%s" % (m, self.mirror_path) for m in _get_mirrors()]

            # If this archive is normally fetched from a tarball URL,
            # then use the same digest.  `spack mirror` ensures that
            # the checksum will be the same.
            digest = None
            if isinstance(self.default_fetcher, fs.URLFetchStrategy):
                digest = self.default_fetcher.digest

            # Have to skip the checkesum for things archived from
            # repositories.  How can this be made safer?
            self.skip_checksum_for_mirror = not bool(digest)

            for url in urls:
                fetchers.insert(0, fs.URLFetchStrategy(url, digest))

        for fetcher in fetchers:
            try:
                fetcher.set_stage(self)
                self.fetcher = fetcher
                self.fetcher.fetch()
                break
            except spack.error.SpackError, e:
                tty.msg("Fetching from %s failed." % fetcher)
                tty.debug(e)
                continue
        else:
            errMessage = "All fetchers failed for %s" % self.name
            self.fetcher = self.default_fetcher
            raise fs.FetchError(errMessage, None)


    def check(self):
        """Check the downloaded archive against a checksum digest.
           No-op if this stage checks code out of a repository."""
        if self.fetcher is not self.default_fetcher and self.skip_checksum_for_mirror:
            tty.warn("Fetching from mirror without a checksum!",
                     "This package is normally checked out from a version "
                     "control system, but it has been archived on a spack "
                     "mirror.  This means we cannot know a checksum for the "
                     "tarball in advance. Be sure that your connection to "
                     "this mirror is secure!.")
        else:
            self.fetcher.check()


    def expand_archive(self):
        """Changes to the stage directory and attempt to expand the downloaded
           archive.  Fail if the stage is not set up or if the archive is not yet
           downloaded.
        """
        self.fetcher.expand()


    def chdir_to_source(self):
        """Changes directory to the expanded archive directory.
           Dies with an error if there was no expanded archive.
        """
        path = self.source_path
        if not path:
            tty.die("Attempt to chdir before expanding archive.")
        else:
            os.chdir(path)
            if not os.listdir(path):
                tty.die("Archive was empty for %s" % self.name)


    def restage(self):
        """Removes the expanded archive path if it exists, then re-expands
           the archive.
        """
        self.fetcher.reset()


    def destroy(self):
        """Remove this stage directory."""
        remove_linked_tree(self.path)

        # Make sure we don't end up in a removed directory
        try:
            os.getcwd()
        except OSError:
            os.chdir(os.path.dirname(self.path))


class DIYStage(object):
    """Simple class that allows any directory to be a spack stage."""
    def __init__(self, path):
        self.archive_file = None
        self.path = path
        self.source_path = path

    def chdir(self):
        if os.path.isdir(self.path):
            os.chdir(self.path)
        else:
            tty.die("Setup failed: no such directory: " + self.path)

    def chdir_to_source(self):
        self.chdir()

    def fetch(self):
        tty.msg("No need to fetch for DIY.")

    def check(self):
        tty.msg("No checksum needed for DIY.")

    def expand_archive(self):
        tty.msg("Using source directory: %s" % self.source_path)

    def restage(self):
        tty.die("Cannot restage DIY stage.")

    def destroy(self):
        # No need to destroy DIY stage.
        pass


def _get_mirrors():
    """Get mirrors from spack configuration."""
    config = spack.config.get_mirror_config()
    return [val for name, val in config.iteritems()]



def ensure_access(file=spack.stage_path):
    """Ensure we can access a directory and die with an error if we can't."""
    if not can_access(file):
        tty.die("Insufficient permissions for %s" % file)


def remove_linked_tree(path):
    """Removes a directory and its contents.  If the directory is a symlink,
       follows the link and reamoves the real directory before removing the
       link.
    """
    if os.path.exists(path):
        if os.path.islink(path):
            shutil.rmtree(os.path.realpath(path), True)
            os.unlink(path)
        else:
            shutil.rmtree(path, True)


def purge():
    """Remove all build directories in the top-level stage path."""
    if os.path.isdir(spack.stage_path):
        for stage_dir in os.listdir(spack.stage_path):
            stage_path = join_path(spack.stage_path, stage_dir)
            remove_linked_tree(stage_path)


def find_tmp_root():
    if spack.use_tmp_stage:
        for tmp in spack.tmp_dirs:
            try:
                # Replace %u with username
                expanded = expand_user(tmp)

                # try to create a directory for spack stuff
                mkdirp(expanded)

                # return it if successful.
                return expanded

            except OSError:
                continue

    return None


class StageError(spack.error.SpackError):
    def __init__(self, message, long_message=None):
        super(self, StageError).__init__(message, long_message)


class RestageError(StageError):
    def __init__(self, message, long_msg=None):
        super(RestageError, self).__init__(message, long_msg)


class ChdirError(StageError):
    def __init__(self, message, long_msg=None):
        super(ChdirError, self).__init__(message, long_msg)


# Keep this in namespace for convenience
FailedDownloadError = fs.FailedDownloadError
