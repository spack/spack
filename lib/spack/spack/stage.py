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
import os
import sys
import errno
import hashlib
import shutil
import tempfile
import getpass
from urlparse import urljoin

import llnl.util.tty as tty
import llnl.util.lock
from llnl.util.filesystem import *

import spack.util.pattern as pattern

import spack
import spack.config
import spack.fetch_strategy as fs
import spack.error
from spack.version import *
from spack.util.path import canonicalize_path
from spack.util.crypto import prefix_bits, bit_length

_stage_prefix = 'spack-stage-'


def _first_accessible_path(paths):
    """Find a tmp dir that exists that we can access."""
    for path in paths:
        try:
            # try to create the path if it doesn't exist.
            path = canonicalize_path(path)
            mkdirp(path)

            # ensure accessible
            if not can_access(path):
                continue

            # return it if successful.
            return path

        except OSError:
            tty.debug('OSError while checking temporary path: %s' % path)
            continue

    return None


# cached temporary root
_tmp_root = None
_use_tmp_stage = True


def get_tmp_root():
    global _tmp_root, _use_tmp_stage

    if not _use_tmp_stage:
        return None

    if _tmp_root is None:
        config = spack.config.get_config('config')
        candidates = config['build_stage']
        if isinstance(candidates, basestring):
            candidates = [candidates]

        path = _first_accessible_path(candidates)
        if not path:
            raise StageError("No accessible stage paths in %s", candidates)

        # Return None to indicate we're using a local staging area.
        if path == canonicalize_path(spack.stage_path):
            _use_tmp_stage = False
            return None

        # ensure that any temp path is unique per user, so users don't
        # fight over shared temporary space.
        user = getpass.getuser()
        if user not in path:
            path = os.path.join(path, user, 'spack-stage')
        else:
            path = os.path.join(path, 'spack-stage')

        mkdirp(path)
        _tmp_root = path

    return _tmp_root


class Stage(object):
    """Manages a temporary stage directory for building.

    A Stage object is a context manager that handles a directory where
    some source code is downloaded and built before being installed.
    It handles fetching the source code, either as an archive to be
    expanded or by checking it out of a repository.  A stage's
    lifecycle looks like this::

        with Stage() as stage:      # Context manager creates and destroys the
                                    # stage directory
            stage.fetch()           # Fetch a source archive into the stage.
            stage.expand_archive()  # Expand the source archive.
            <install>               # Build and install the archive.
                                    # (handled by user of Stage)

    When used as a context manager, the stage is automatically
    destroyed if no exception is raised by the context. If an
    excpetion is raised, the stage is left in the filesystem and NOT
    destroyed, for potential reuse later.

    You can also use the stage's create/destroy functions manually,
    like this::

        stage = Stage()
        try:
            stage.create()          # Explicitly create the stage directory.
            stage.fetch()           # Fetch a source archive into the stage.
            stage.expand_archive()  # Expand the source archive.
            <install>               # Build and install the archive.
                                    # (handled by user of Stage)
        finally:
            stage.destroy()         # Explicitly destroy the stage directory.

    If spack.use_tmp_stage is True, spack will attempt to create
    stages in a tmp directory.  Otherwise, stages are created directly
    in spack.stage_path.

    There are two kinds of stages: named and unnamed.  Named stages
    can persist between runs of spack, e.g. if you fetched a tarball
    but didn't finish building it, you won't have to fetch it again.

    Unnamed stages are created using standard mkdtemp mechanisms or
    similar, and are intended to persist for only one run of spack.
    """

    """Shared dict of all stage locks."""
    stage_locks = {}

    def __init__(
            self, url_or_fetch_strategy,
            name=None, mirror_path=None, keep=False, path=None, lock=True,
            alternate_fetchers=None):
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

             mirror_path
                 If provided, Stage will search Spack's mirrors for
                 this archive at the mirror_path, before using the
                 default fetch strategy.

             keep
                 By default, when used as a context manager, the Stage
                 is deleted on exit when no exceptions are raised.
                 Pass True to keep the stage intact even if no
                 exceptions are raised.
        """
        # TODO: fetch/stage coupling needs to be reworked -- the logic
        # TODO: here is convoluted and not modular enough.
        if isinstance(url_or_fetch_strategy, basestring):
            self.fetcher = fs.from_url(url_or_fetch_strategy)
        elif isinstance(url_or_fetch_strategy, fs.FetchStrategy):
            self.fetcher = url_or_fetch_strategy
        else:
            raise ValueError(
                "Can't construct Stage without url or fetch strategy")
        self.fetcher.set_stage(self)
        # self.fetcher can change with mirrors.
        self.default_fetcher = self.fetcher
        self.alternate_fetchers = alternate_fetchers
        # used for mirrored archives of repositories.
        self.skip_checksum_for_mirror = True

        # TODO : this uses a protected member of tempfile, but seemed the only
        # TODO : way to get a temporary name besides, the temporary link name
        # TODO : won't be the same as the temporary stage area in tmp_root
        self.name = name
        if name is None:
            self.name = _stage_prefix + next(tempfile._get_candidate_names())
        self.mirror_path = mirror_path

        # Try to construct here a temporary name for the stage directory
        # If this is a named stage, then construct a named path.
        if path is not None:
            self.path = path
        else:
            self.path = join_path(spack.stage_path, self.name)

        # Flag to decide whether to delete the stage folder on exit or not
        self.keep = keep

        # File lock for the stage directory.  We use one file for all
        # stage locks. See Spec.prefix_lock for details on this approach.
        self._lock = None
        if lock:
            if self.name not in Stage.stage_locks:
                sha1 = hashlib.sha1(self.name).digest()
                lock_id = prefix_bits(sha1, bit_length(sys.maxsize))
                stage_lock_path = join_path(spack.stage_path, '.lock')

                Stage.stage_locks[self.name] = llnl.util.lock.Lock(
                    stage_lock_path, lock_id, 1)

            self._lock = Stage.stage_locks[self.name]

    def __enter__(self):
        """
        Entering a stage context will create the stage directory

        Returns:
            self
        """
        if self._lock is not None:
            self._lock.acquire_write(timeout=60)
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exiting from a stage context will delete the stage directory unless:
        - it was explicitly requested not to do so
        - an exception has been raised

        Args:
            exc_type: exception type
            exc_val: exception value
            exc_tb: exception traceback

        Returns:
            Boolean
        """
        # Delete when there are no exceptions, unless asked to keep.
        if exc_type is None and not self.keep:
            self.destroy()

        if self._lock is not None:
            self._lock.release_write()

    def _need_to_create_path(self):
        """Makes sure nothing weird has happened since the last time we
           looked at path.  Returns True if path already exists and is ok.
           Returns False if path needs to be created."""
        # Path doesn't exist yet.  Will need to create it.
        if not os.path.exists(self.path):
            return True

        # Path exists but points at something else.  Blow it away.
        if not os.path.isdir(self.path):
            os.unlink(self.path)
            return True

        # Path looks ok, but need to check the target of the link.
        if os.path.islink(self.path):
            tmp_root = get_tmp_root()
            if tmp_root is not None:
                real_path = os.path.realpath(self.path)
                real_tmp = os.path.realpath(tmp_root)

                # If we're using a tmp dir, it's a link, and it points at the
                # right spot, then keep it.
                if (real_path.startswith(real_tmp) and
                        os.path.exists(real_path)):
                    return False
                else:
                    # otherwise, just unlink it and start over.
                    os.unlink(self.path)
                    return True

            else:
                # If we're not tmp mode, then it's a link and we want a
                # directory.
                os.unlink(self.path)
                return True

        return False

    @property
    def expected_archive_files(self):
        """Possible archive file paths."""
        paths = []
        if isinstance(self.default_fetcher, fs.URLFetchStrategy):
            paths.append(os.path.join(
                self.path, os.path.basename(self.default_fetcher.url)))

        if self.mirror_path:
            paths.append(os.path.join(
                self.path, os.path.basename(self.mirror_path)))

        return paths

    @property
    def save_filename(self):
        possible_filenames = self.expected_archive_files
        if possible_filenames:
            # This prefers using the URL associated with the default fetcher if
            # available, so that the fetched resource name matches the remote
            # name
            return possible_filenames[0]

    @property
    def archive_file(self):
        """Path to the source archive within this stage directory."""
        for path in self.expected_archive_files:
            if os.path.exists(path):
                return path
        else:
            return None

    @property
    def source_path(self):
        """Returns the path to the expanded/checked out source code.

        To find the source code, this method searches for the first
        subdirectory of the stage that it can find, and returns it.
        This assumes nothing besides the archive file will be in the
        stage path, but it has the advantage that we don't need to
        know the name of the archive or its contents.

        If the fetch strategy is not supposed to expand the downloaded
        file, it will just return the stage path. If the archive needs
        to be expanded, it will return None when no archive is found.
        """
        if isinstance(self.fetcher, fs.URLFetchStrategy):
            if not self.fetcher.expand_archive:
                return self.path

        for p in [os.path.join(self.path, f) for f in os.listdir(self.path)]:
            if os.path.isdir(p):
                return p
        return None

    def chdir(self):
        """Changes directory to the stage path. Or dies if it is not set
        up."""
        if os.path.isdir(self.path):
            os.chdir(self.path)
        else:
            raise ChdirError("Setup failed: no such directory: " + self.path)

    def fetch(self, mirror_only=False):
        """Downloads an archive or checks out code from a repository."""
        self.chdir()

        fetchers = []
        if not mirror_only:
            fetchers.append(self.default_fetcher)

        # TODO: move mirror logic out of here and clean it up!
        # TODO: Or @alalazo may have some ideas about how to use a
        # TODO: CompositeFetchStrategy here.
        self.skip_checksum_for_mirror = True
        if self.mirror_path:
            mirrors = spack.config.get_config('mirrors')

            # Join URLs of mirror roots with mirror paths. Because
            # urljoin() will strip everything past the final '/' in
            # the root, so we add a '/' if it is not present.
            mirror_roots = [root if root.endswith('/') else root + '/'
                            for root in mirrors.values()]
            urls = [urljoin(root, self.mirror_path) for root in mirror_roots]

            # If this archive is normally fetched from a tarball URL,
            # then use the same digest.  `spack mirror` ensures that
            # the checksum will be the same.
            digest = None
            expand = True
            extension = None
            if isinstance(self.default_fetcher, fs.URLFetchStrategy):
                digest = self.default_fetcher.digest
                expand = self.default_fetcher.expand_archive
                extension = self.default_fetcher.extension

            # Have to skip the checksum for things archived from
            # repositories.  How can this be made safer?
            self.skip_checksum_for_mirror = not bool(digest)

            # Add URL strategies for all the mirrors with the digest
            for url in urls:
                fetchers.insert(
                    0, fs.URLFetchStrategy(
                        url, digest, expand=expand, extension=extension))
            if self.default_fetcher.cachable:
                fetchers.insert(
                    0, spack.fetch_cache.fetcher(
                        self.mirror_path, digest, expand=expand,
                        extension=extension))

        if self.alternate_fetchers:
            fetchers.extend(self.alternate_fetchers)

        for fetcher in fetchers:
            try:
                fetcher.set_stage(self)
                self.fetcher = fetcher
                self.fetcher.fetch()
                break
            except spack.error.SpackError as e:
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
        if self.fetcher is not self.default_fetcher and \
           self.skip_checksum_for_mirror:
            tty.warn("Fetching from mirror without a checksum!",
                     "This package is normally checked out from a version "
                     "control system, but it has been archived on a spack "
                     "mirror.  This means we cannot know a checksum for the "
                     "tarball in advance. Be sure that your connection to "
                     "this mirror is secure!.")
        else:
            self.fetcher.check()

    def cache_local(self):
        spack.fetch_cache.store(self.fetcher, self.mirror_path)

    def expand_archive(self):
        """Changes to the stage directory and attempt to expand the downloaded
        archive.  Fail if the stage is not set up or if the archive is not yet
        downloaded."""
        archive_dir = self.source_path
        if not archive_dir:
            self.fetcher.expand()
            tty.msg("Created stage in %s" % self.path)
        else:
            tty.msg("Already staged %s in %s" % (self.name, self.path))

    def chdir_to_source(self):
        """Changes directory to the expanded archive directory.
           Dies with an error if there was no expanded archive.
        """
        path = self.source_path
        if not path:
            raise StageError("Attempt to chdir before expanding archive.")
        else:
            os.chdir(path)
            if not os.listdir(path):
                raise StageError("Archive was empty for %s" % self.name)

    def restage(self):
        """Removes the expanded archive path if it exists, then re-expands
           the archive.
        """
        self.fetcher.reset()

    def create(self):
        """Creates the stage directory.

        If get_tmp_root() is None, the stage directory is created
        directly under spack.stage_path, otherwise this will attempt to
        create a stage in a temporary directory and link it into
        spack.stage_path.

        Spack will use the first writable location in spack.tmp_dirs
        to create a stage. If there is no valid location in tmp_dirs,
        fall back to making the stage inside spack.stage_path.

        """
        # Create the top-level stage directory
        mkdirp(spack.stage_path)
        remove_if_dead_link(self.path)

        # If a tmp_root exists then create a directory there and then link it
        # in the stage area, otherwise create the stage directory in self.path
        if self._need_to_create_path():
            tmp_root = get_tmp_root()
            if tmp_root is not None:
                tmp_dir = tempfile.mkdtemp('', _stage_prefix, tmp_root)
                tty.debug('link %s -> %s' % (self.path, tmp_dir))
                os.symlink(tmp_dir, self.path)
            else:
                mkdirp(self.path)
        # Make sure we can actually do something with the stage we made.
        ensure_access(self.path)

    def destroy(self):
        """Removes this stage directory."""
        remove_linked_tree(self.path)

        # Make sure we don't end up in a removed directory
        try:
            os.getcwd()
        except OSError:
            os.chdir(os.path.dirname(self.path))


class ResourceStage(Stage):

    def __init__(self, url_or_fetch_strategy, root, resource, **kwargs):
        super(ResourceStage, self).__init__(url_or_fetch_strategy, **kwargs)
        self.root_stage = root
        self.resource = resource

    def expand_archive(self):
        super(ResourceStage, self).expand_archive()
        root_stage = self.root_stage
        resource = self.resource
        placement = os.path.basename(self.source_path) \
            if resource.placement is None \
            else resource.placement
        if not isinstance(placement, dict):
            placement = {'': placement}
        # Make the paths in the dictionary absolute and link
        for key, value in placement.iteritems():
            target_path = join_path(
                root_stage.source_path, resource.destination)
            destination_path = join_path(target_path, value)
            source_path = join_path(self.source_path, key)

            try:
                os.makedirs(target_path)
            except OSError as err:
                if err.errno == errno.EEXIST and os.path.isdir(target_path):
                    pass
                else:
                    raise

            if not os.path.exists(destination_path):
                # Create a symlink
                tty.info('Moving resource stage\n\tsource : '
                         '{stage}\n\tdestination : {destination}'.format(
                             stage=source_path, destination=destination_path
                         ))
                shutil.move(source_path, destination_path)


@pattern.composite(method_list=['fetch', 'create', 'check', 'expand_archive',
                                'restage', 'destroy', 'cache_local'])
class StageComposite:
    """Composite for Stage type objects. The first item in this composite is
    considered to be the root package, and operations that return a value are
    forwarded to it."""
    #
    # __enter__ and __exit__ delegate to all stages in the composite.
    #

    def __enter__(self):
        for item in self:
            item.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for item in reversed(self):
            item.keep = getattr(self, 'keep', False)
            item.__exit__(exc_type, exc_val, exc_tb)

    #
    # Below functions act only on the *first* stage in the composite.
    #
    @property
    def source_path(self):
        return self[0].source_path

    @property
    def path(self):
        return self[0].path

    def chdir_to_source(self):
        return self[0].chdir_to_source()

    @property
    def archive_file(self):
        return self[0].archive_file

    @property
    def mirror_path(self):
        return self[0].mirror_path


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
            raise ChdirError("Setup failed: no such directory: " + self.path)

    # DIY stages do nothing as context managers.
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def chdir_to_source(self):
        self.chdir()

    def fetch(self, *args, **kwargs):
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

    def cache_local(self):
        tty.msg("Sources for DIY stages are not cached")


def _get_mirrors():
    """Get mirrors from spack configuration."""
    config = spack.config.get_config('mirrors')
    return [val for name, val in config.iteritems()]


def ensure_access(file=spack.stage_path):
    """Ensure we can access a directory and die with an error if we can't."""
    if not can_access(file):
        tty.die("Insufficient permissions for %s" % file)


def purge():
    """Remove all build directories in the top-level stage path."""
    if os.path.isdir(spack.stage_path):
        for stage_dir in os.listdir(spack.stage_path):
            stage_path = join_path(spack.stage_path, stage_dir)
            remove_linked_tree(stage_path)


class StageError(spack.error.SpackError):
    """"Superclass for all errors encountered during staging."""


class RestageError(StageError):
    """"Error encountered during restaging."""


class ChdirError(StageError):
    """Raised when Spack can't change directories."""

# Keep this in namespace for convenience
FailedDownloadError = fs.FailedDownloadError
