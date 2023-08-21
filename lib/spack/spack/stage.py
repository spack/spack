# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import getpass
import glob
import hashlib
import os
import shutil
import stat
import sys
import tempfile
from typing import Dict, Iterable

import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import (
    can_access,
    get_owner_uid,
    getuid,
    install,
    install_tree,
    mkdirp,
    partition_path,
    remove_linked_tree,
)

import spack.caches
import spack.config
import spack.error
import spack.fetch_strategy as fs
import spack.mirror
import spack.paths
import spack.spec
import spack.util.lock
import spack.util.path as sup
import spack.util.pattern as pattern
import spack.util.url as url_util
from spack.util.crypto import bit_length, prefix_bits
from spack.util.web import FetchError

# The well-known stage source subdirectory name.
_source_path_subdir = "spack-src"

# The temporary stage name prefix.
stage_prefix = "spack-stage-"


def compute_stage_name(spec):
    """Determine stage name given a spec"""
    default_stage_structure = stage_prefix + "{name}-{version}-{hash}"
    stage_name_structure = spack.config.get("config:stage_name", default=default_stage_structure)
    return spec.format(format_string=stage_name_structure)


def create_stage_root(path: str) -> None:
    """Create the stage root directory and ensure appropriate access perms."""
    assert os.path.isabs(path) and len(path.strip()) > 1

    err_msg = "Cannot create stage root {0}: Access to {1} is denied"

    user_uid = getuid()

    # Obtain lists of ancestor and descendant paths of the $user node, if any.
    group_paths, user_node, user_paths = partition_path(path, getpass.getuser())

    for p in group_paths:
        if not os.path.exists(p):
            # Ensure access controls of subdirs created above `$user` inherit
            # from the parent and share the group.
            par_stat = os.stat(os.path.dirname(p))
            mkdirp(p, group=par_stat.st_gid, mode=par_stat.st_mode)

            p_stat = os.stat(p)
            if par_stat.st_gid != p_stat.st_gid:
                tty.warn(
                    "Expected {0} to have group {1}, but it is {2}".format(
                        p, par_stat.st_gid, p_stat.st_gid
                    )
                )

            if par_stat.st_mode & p_stat.st_mode != par_stat.st_mode:
                tty.warn(
                    "Expected {0} to support mode {1}, but it is {2}".format(
                        p, par_stat.st_mode, p_stat.st_mode
                    )
                )

            if not can_access(p):
                raise OSError(errno.EACCES, err_msg.format(path, p))

    # Add the path ending with the $user node to the user paths to ensure paths
    # from $user (on down) meet the ownership and permission requirements.
    if user_node:
        user_paths.insert(0, user_node)

    for p in user_paths:
        # Ensure access controls of subdirs from `$user` on down are
        # restricted to the user.
        owner_uid = get_owner_uid(p)
        if user_uid != owner_uid:
            tty.warn(
                "Expected user {0} to own {1}, but it is owned by {2}".format(
                    user_uid, p, owner_uid
                )
            )

    spack_src_subdir = os.path.join(path, _source_path_subdir)
    # When staging into a user-specified directory with `spack stage -p <PATH>`, we need
    # to ensure the `spack-src` subdirectory exists, as we can't rely on it being
    # created automatically by spack. It's not clear why this is the case for `spack
    # stage -p`, but since `mkdirp()` is idempotent, this should not change the behavior
    # for any other code paths.
    if not os.path.isdir(spack_src_subdir):
        mkdirp(spack_src_subdir, mode=stat.S_IRWXU)


def _first_accessible_path(paths):
    """Find the first path that is accessible, creating it if necessary."""
    for path in paths:
        try:
            # Ensure the user has access, creating the directory if necessary.
            if os.path.exists(path):
                if can_access(path):
                    return path
            else:
                # Now create the stage root with the proper group/perms.
                create_stage_root(path)
                return path

        except OSError as e:
            tty.debug("OSError while checking stage path %s: %s" % (path, str(e)))

    return None


def _resolve_paths(candidates):
    """
    Resolve candidate paths and make user-related adjustments.

    Adjustments involve removing extra $user from $tempdir if $tempdir includes
    $user and appending $user if it is not present in the path.
    """
    temp_path = sup.canonicalize_path("$tempdir")
    user = getpass.getuser()
    tmp_has_usr = user in temp_path.split(os.path.sep)

    paths = []
    for path in candidates:
        # Remove the extra `$user` node from a `$tempdir/$user` entry for
        # hosts that automatically append `$user` to `$tempdir`.
        if path.startswith(os.path.join("$tempdir", "$user")) and tmp_has_usr:
            path = path.replace("/$user", "", 1)

        # Ensure the path is unique per user.
        can_path = sup.canonicalize_path(path)
        # When multiple users share a stage root, we can avoid conflicts between
        # them by adding a per-user subdirectory.
        # Avoid doing this on Windows to keep stage absolute path as short as possible.
        if user not in can_path and not sys.platform == "win32":
            can_path = os.path.join(can_path, user)

        paths.append(can_path)

    return paths


# Cached stage path root
_stage_root = None


def get_stage_root():
    global _stage_root

    if _stage_root is None:
        candidates = spack.config.get("config:build_stage")
        if isinstance(candidates, str):
            candidates = [candidates]

        resolved_candidates = _resolve_paths(candidates)
        path = _first_accessible_path(resolved_candidates)
        if not path:
            raise StageError("No accessible stage paths in:", " ".join(resolved_candidates))

        _stage_root = path

    return _stage_root


def _mirror_roots():
    mirrors = spack.config.get("mirrors")
    return [
        sup.substitute_path_variables(root)
        if root.endswith(os.sep)
        else sup.substitute_path_variables(root) + os.sep
        for root in mirrors.values()
    ]


class Stage:
    """Manages a temporary stage directory for building.

    A Stage object is a context manager that handles a directory where
    some source code is downloaded and built before being installed.
    It handles fetching the source code, either as an archive to be
    expanded or by checking it out of a repository.  A stage's
    lifecycle looks like this::

        with Stage() as stage:      # Context manager creates and destroys the
                                    # stage directory
            stage.fetch()           # Fetch a source archive into the stage.
            stage.expand_archive()  # Expand the archive into source_path.
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
            stage.expand_archive()  # Expand the archive into source_path.
            <install>               # Build and install the archive.
                                    # (handled by user of Stage)
        finally:
            stage.destroy()         # Explicitly destroy the stage directory.

    There are two kinds of stages: named and unnamed.  Named stages
    can persist between runs of spack, e.g. if you fetched a tarball
    but didn't finish building it, you won't have to fetch it again.

    Unnamed stages are created using standard mkdtemp mechanisms or
    similar, and are intended to persist for only one run of spack.
    """

    """Shared dict of all stage locks."""
    stage_locks: Dict[str, spack.util.lock.Lock] = {}

    """Most staging is managed by Spack.  DIYStage is one exception."""
    managed_by_spack = True

    def __init__(
        self,
        url_or_fetch_strategy,
        name=None,
        mirror_paths=None,
        keep=False,
        path=None,
        lock=True,
        search_fn=None,
    ):
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

          mirror_paths
              If provided, Stage will search Spack's mirrors for
              this archive at each of the provided relative mirror paths
              before using the default fetch strategy.

          keep
              By default, when used as a context manager, the Stage
              is deleted on exit when no exceptions are raised.
              Pass True to keep the stage intact even if no
              exceptions are raised.

         path
              If provided, the stage path to use for associated builds.

         lock
              True if the stage directory file lock is to be used, False
              otherwise.

         search_fn
              The search function that provides the fetch strategy
              instance.
        """
        # TODO: fetch/stage coupling needs to be reworked -- the logic
        # TODO: here is convoluted and not modular enough.
        if isinstance(url_or_fetch_strategy, str):
            self.fetcher = fs.from_url_scheme(url_or_fetch_strategy)
        elif isinstance(url_or_fetch_strategy, fs.FetchStrategy):
            self.fetcher = url_or_fetch_strategy
        else:
            raise ValueError("Can't construct Stage without url or fetch strategy")
        self.fetcher.stage = self
        # self.fetcher can change with mirrors.
        self.default_fetcher = self.fetcher
        self.search_fn = search_fn
        # used for mirrored archives of repositories.
        self.skip_checksum_for_mirror = True

        self.srcdir = None

        # TODO: This uses a protected member of tempfile, but seemed the only
        # TODO: way to get a temporary name.  It won't be the same as the
        # TODO: temporary stage area in _stage_root.
        self.name = name
        if name is None:
            self.name = stage_prefix + next(tempfile._get_candidate_names())
        self.mirror_paths = mirror_paths

        # Use the provided path or construct an optionally named stage path.
        if path is not None:
            self.path = path
        else:
            self.path = os.path.join(get_stage_root(), self.name)

        # Flag to decide whether to delete the stage folder on exit or not
        self.keep = keep

        # File lock for the stage directory.  We use one file for all
        # stage locks. See spack.database.Database.prefix_locker.lock for
        # details on this approach.
        self._lock = None
        if lock:
            if self.name not in Stage.stage_locks:
                sha1 = hashlib.sha1(self.name.encode("utf-8")).digest()
                lock_id = prefix_bits(sha1, bit_length(sys.maxsize))
                stage_lock_path = os.path.join(get_stage_root(), ".lock")

                tty.debug("Creating stage lock {0}".format(self.name))
                Stage.stage_locks[self.name] = spack.util.lock.Lock(
                    stage_lock_path, start=lock_id, length=1, desc=self.name
                )

            self._lock = Stage.stage_locks[self.name]

        # When stages are reused, we need to know whether to re-create
        # it.  This marks whether it has been created/destroyed.
        self.created = False

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

    @property
    def expected_archive_files(self):
        """Possible archive file paths."""
        paths = []
        fnames = []
        expanded = True
        if isinstance(self.default_fetcher, fs.URLFetchStrategy):
            expanded = self.default_fetcher.expand_archive
            fnames.append(url_util.default_download_filename(self.default_fetcher.url))

        if self.mirror_paths:
            fnames.extend(os.path.basename(x) for x in self.mirror_paths)

        paths.extend(os.path.join(self.path, f) for f in fnames)
        if not expanded:
            # If the download file is not compressed, the "archive" is a
            # single file placed in Stage.source_path
            paths.extend(os.path.join(self.source_path, f) for f in fnames)

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
    def expanded(self):
        """Returns True if source path expanded; else False."""
        return os.path.exists(self.source_path)

    @property
    def source_path(self):
        """Returns the well-known source directory path."""
        return os.path.join(self.path, _source_path_subdir)

    def disable_mirrors(self):
        """The Stage will not attempt to look for the associated fetcher
        target in any of Spack's mirrors (including the local download cache).
        """
        self.mirror_paths = []

    def fetch(self, mirror_only=False, err_msg=None):
        """Retrieves the code or archive

        Args:
            mirror_only (bool): only fetch from a mirror
            err_msg (str or None): the error message to display if all fetchers
                fail or ``None`` for the default fetch failure message
        """
        fetchers = []
        if not mirror_only:
            fetchers.append(self.default_fetcher)

        # TODO: move mirror logic out of here and clean it up!
        # TODO: Or @alalazo may have some ideas about how to use a
        # TODO: CompositeFetchStrategy here.
        self.skip_checksum_for_mirror = True
        if self.mirror_paths:
            # Join URLs of mirror roots with mirror paths. Because
            # urljoin() will strip everything past the final '/' in
            # the root, so we add a '/' if it is not present.
            mirror_urls = [
                url_util.join(mirror.fetch_url, rel_path)
                for mirror in spack.mirror.MirrorCollection(source=True).values()
                for rel_path in self.mirror_paths
            ]

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
            # Insert fetchers in the order that the URLs are provided.
            for url in reversed(mirror_urls):
                fetchers.insert(
                    0, fs.from_url_scheme(url, digest, expand=expand, extension=extension)
                )

            if self.default_fetcher.cachable:
                for rel_path in reversed(list(self.mirror_paths)):
                    cache_fetcher = spack.caches.FETCH_CACHE.fetcher(
                        rel_path, digest, expand=expand, extension=extension
                    )
                    fetchers.insert(0, cache_fetcher)

        def generate_fetchers():
            for fetcher in fetchers:
                yield fetcher
            # The search function may be expensive, so wait until now to
            # call it so the user can stop if a prior fetcher succeeded
            if self.search_fn and not mirror_only:
                dynamic_fetchers = self.search_fn()
                for fetcher in dynamic_fetchers:
                    yield fetcher

        def print_errors(errors):
            for msg in errors:
                tty.debug(msg)

        errors = []
        for fetcher in generate_fetchers():
            try:
                fetcher.stage = self
                self.fetcher = fetcher
                self.fetcher.fetch()
                break
            except spack.fetch_strategy.NoCacheError:
                # Don't bother reporting when something is not cached.
                continue
            except spack.error.SpackError as e:
                errors.append("Fetching from {0} failed.".format(fetcher))
                tty.debug(e)
                continue
        else:
            print_errors(errors)

            self.fetcher = self.default_fetcher
            default_msg = "All fetchers failed for {0}".format(self.name)
            raise FetchError(err_msg or default_msg, None)

        print_errors(errors)

    def steal_source(self, dest):
        """Copy the source_path directory in its entirety to directory dest

        This operation creates/fetches/expands the stage if it is not already,
        and destroys the stage when it is done."""
        if not self.created:
            self.create()
        if not self.expanded and not self.archive_file:
            self.fetch()
        if not self.expanded:
            self.expand_archive()

        if not os.path.isdir(dest):
            mkdirp(dest)

        # glob all files and directories in the source path
        hidden_entries = glob.glob(os.path.join(self.source_path, ".*"))
        entries = glob.glob(os.path.join(self.source_path, "*"))

        # Move all files from stage to destination directory
        # Include hidden files for VCS repo history
        for entry in hidden_entries + entries:
            if os.path.isdir(entry):
                d = os.path.join(dest, os.path.basename(entry))
                shutil.copytree(entry, d, symlinks=True)
            else:
                shutil.copy2(entry, dest)

        # copy archive file if we downloaded from url -- replaces for vcs
        if self.archive_file and os.path.exists(self.archive_file):
            shutil.copy2(self.archive_file, dest)

        # remove leftover stage
        self.destroy()

    def check(self):
        """Check the downloaded archive against a checksum digest.
        No-op if this stage checks code out of a repository."""
        if self.fetcher is not self.default_fetcher and self.skip_checksum_for_mirror:
            tty.warn(
                "Fetching from mirror without a checksum!",
                "This package is normally checked out from a version "
                "control system, but it has been archived on a spack "
                "mirror.  This means we cannot know a checksum for the "
                "tarball in advance. Be sure that your connection to "
                "this mirror is secure!",
            )
        elif spack.config.get("config:checksum"):
            self.fetcher.check()

    def cache_local(self):
        spack.caches.FETCH_CACHE.store(self.fetcher, self.mirror_paths.storage_path)

    def cache_mirror(self, mirror, stats):
        """Perform a fetch if the resource is not already cached

        Arguments:
            mirror (spack.caches.MirrorCache): the mirror to cache this Stage's
                resource in
            stats (spack.mirror.MirrorStats): this is updated depending on whether the
                caching operation succeeded or failed
        """
        if isinstance(self.default_fetcher, fs.BundleFetchStrategy):
            # BundleFetchStrategy has no source to fetch. The associated
            # fetcher does nothing but the associated stage may still exist.
            # There is currently no method available on the fetcher to
            # distinguish this ('cachable' refers to whether the fetcher
            # refers to a resource with a fixed ID, which is not the same
            # concept as whether there is anything to fetch at all) so we
            # must examine the type of the fetcher.
            return

        if mirror.skip_unstable_versions and not fs.stable_target(self.default_fetcher):
            return

        absolute_storage_path = os.path.join(mirror.root, self.mirror_paths.storage_path)

        if os.path.exists(absolute_storage_path):
            stats.already_existed(absolute_storage_path)
        else:
            self.fetch()
            self.check()
            mirror.store(self.fetcher, self.mirror_paths.storage_path)
            stats.added(absolute_storage_path)

        mirror.symlink(self.mirror_paths)

    def expand_archive(self):
        """Changes to the stage directory and attempt to expand the downloaded
        archive.  Fail if the stage is not set up or if the archive is not yet
        downloaded."""
        if not self.expanded:
            self.fetcher.expand()
            tty.debug("Created stage in {0}".format(self.path))
        else:
            tty.debug("Already staged {0} in {1}".format(self.name, self.path))

    def restage(self):
        """Removes the expanded archive path if it exists, then re-expands
        the archive.
        """
        self.fetcher.reset()

    def create(self):
        """
        Ensures the top-level (config:build_stage) directory exists.
        """
        # User has full permissions and group has only read permissions
        if not os.path.exists(self.path):
            mkdirp(self.path, mode=stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
        elif not os.path.isdir(self.path):
            os.remove(self.path)
            mkdirp(self.path, mode=stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)

        # Make sure we can actually do something with the stage we made.
        ensure_access(self.path)
        self.created = True

    def destroy(self):
        """Removes this stage directory."""
        remove_linked_tree(self.path)

        # Make sure we don't end up in a removed directory
        try:
            os.getcwd()
        except OSError as e:
            tty.debug(e)
            os.chdir(os.path.dirname(self.path))

        # mark as destroyed
        self.created = False


class ResourceStage(Stage):
    def __init__(self, url_or_fetch_strategy, root, resource, **kwargs):
        super().__init__(url_or_fetch_strategy, **kwargs)
        self.root_stage = root
        self.resource = resource

    def restage(self):
        super().restage()
        self._add_to_root_stage()

    def expand_archive(self):
        super().expand_archive()
        self._add_to_root_stage()

    def _add_to_root_stage(self):
        """
        Move the extracted resource to the root stage (according to placement).
        """
        root_stage = self.root_stage
        resource = self.resource

        if resource.placement:
            placement = resource.placement
        elif self.srcdir:
            placement = self.srcdir
        else:
            placement = self.source_path

        if not isinstance(placement, dict):
            placement = {"": placement}

        target_path = os.path.join(root_stage.source_path, resource.destination)

        try:
            os.makedirs(target_path)
        except OSError as err:
            tty.debug(err)
            if err.errno == errno.EEXIST and os.path.isdir(target_path):
                pass
            else:
                raise

        for key, value in placement.items():
            destination_path = os.path.join(target_path, value)
            source_path = os.path.join(self.source_path, key)

            if not os.path.exists(destination_path):
                tty.info(
                    "Moving resource stage\n\tsource: "
                    "{stage}\n\tdestination: {destination}".format(
                        stage=source_path, destination=destination_path
                    )
                )

                src = os.path.realpath(source_path)

                if os.path.isdir(src):
                    install_tree(src, destination_path)
                else:
                    install(src, destination_path)


class StageComposite(pattern.Composite):
    """Composite for Stage type objects. The first item in this composite is
    considered to be the root package, and operations that return a value are
    forwarded to it."""

    #
    # __enter__ and __exit__ delegate to all stages in the composite.
    #

    def __init__(self):
        super().__init__(
            [
                "fetch",
                "create",
                "created",
                "check",
                "expand_archive",
                "restage",
                "destroy",
                "cache_local",
                "cache_mirror",
                "steal_source",
                "disable_mirrors",
                "managed_by_spack",
            ]
        )

    @classmethod
    def from_iterable(cls, iterable: Iterable[Stage]) -> "StageComposite":
        """Create a new composite from an iterable of stages."""
        composite = cls()
        composite.extend(iterable)
        return composite

    def __enter__(self):
        for item in self:
            item.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for item in reversed(self):
            item.__exit__(exc_type, exc_val, exc_tb)

    #
    # Below functions act only on the *first* stage in the composite.
    #
    @property
    def source_path(self):
        return self[0].source_path

    @property
    def expanded(self):
        return self[0].expanded

    @property
    def path(self):
        return self[0].path

    @property
    def archive_file(self):
        return self[0].archive_file

    @property
    def keep(self):
        return self[0].keep

    @keep.setter
    def keep(self, value):
        for item in self:
            item.keep = value


class DIYStage:
    """
    Simple class that allows any directory to be a spack stage.  Consequently,
    it does not expect or require that the source path adhere to the standard
    directory naming convention.
    """

    """DIY staging is, by definition, not managed by Spack."""
    managed_by_spack = False

    def __init__(self, path):
        if path is None:
            raise ValueError("Cannot construct DIYStage without a path.")
        elif not os.path.isdir(path):
            raise StagePathError("The stage path directory does not exist:", path)

        self.archive_file = None
        self.path = path
        self.source_path = path
        self.created = True

    # DIY stages do nothing as context managers.
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fetch(self, *args, **kwargs):
        tty.debug("No need to fetch for DIY.")

    def check(self):
        tty.debug("No checksum needed for DIY.")

    def expand_archive(self):
        tty.debug("Using source directory: {0}".format(self.source_path))

    @property
    def expanded(self):
        """Returns True since the source_path must exist."""
        return True

    def restage(self):
        raise RestageError("Cannot restage a DIY stage.")

    def create(self):
        self.created = True

    def destroy(self):
        # No need to destroy DIY stage.
        pass

    def cache_local(self):
        tty.debug("Sources for DIY stages are not cached")


def ensure_access(file):
    """Ensure we can access a directory and die with an error if we can't."""
    if not can_access(file):
        tty.die("Insufficient permissions for %s" % file)


def purge():
    """Remove all build directories in the top-level stage path."""
    root = get_stage_root()
    if os.path.isdir(root):
        for stage_dir in os.listdir(root):
            if stage_dir.startswith(stage_prefix) or stage_dir == ".lock":
                stage_path = os.path.join(root, stage_dir)
                if os.path.isdir(stage_path):
                    remove_linked_tree(stage_path)
                else:
                    os.remove(stage_path)


def get_checksums_for_versions(url_dict, name, **kwargs):
    """Fetches and checksums archives from URLs.

    This function is called by both ``spack checksum`` and ``spack
    create``.  The ``first_stage_function`` argument allows the caller to
    inspect the first downloaded archive, e.g., to determine the build
    system.

    Args:
        url_dict (dict): A dictionary of the form: version -> URL
        name (str): The name of the package
        first_stage_function (typing.Callable): function that takes a Stage and a URL;
            this is run on the stage of the first URL downloaded
        keep_stage (bool): whether to keep staging area when command completes
        batch (bool): whether to ask user how many versions to fetch (false)
            or fetch all versions (true)
        fetch_options (dict): Options used for the fetcher (such as timeout
            or cookies)

    Returns:
        (dict): A dictionary of the form: version -> checksum

    """
    batch = kwargs.get("batch", False)
    fetch_options = kwargs.get("fetch_options", None)
    first_stage_function = kwargs.get("first_stage_function", None)
    keep_stage = kwargs.get("keep_stage", False)

    sorted_versions = sorted(url_dict.keys(), reverse=True)

    # Find length of longest string in the list for padding
    max_len = max(len(str(v)) for v in sorted_versions)
    num_ver = len(sorted_versions)

    tty.msg(
        "Found {0} version{1} of {2}:".format(num_ver, "" if num_ver == 1 else "s", name),
        "",
        *llnl.util.lang.elide_list(
            ["{0:{1}}  {2}".format(str(v), max_len, url_dict[v]) for v in sorted_versions]
        ),
    )
    print()

    if batch:
        archives_to_fetch = len(sorted_versions)
    else:
        archives_to_fetch = tty.get_number(
            "How many would you like to checksum?", default=1, abort="q"
        )

    if not archives_to_fetch:
        tty.die("Aborted.")

    versions = sorted_versions[:archives_to_fetch]
    urls = [url_dict[v] for v in versions]

    tty.debug("Downloading...")
    version_hashes = {}
    i = 0
    errors = []
    for url, version in zip(urls, versions):
        try:
            if fetch_options:
                url_or_fs = fs.URLFetchStrategy(url, fetch_options=fetch_options)
            else:
                url_or_fs = url
            with Stage(url_or_fs, keep=keep_stage) as stage:
                # Fetch the archive
                stage.fetch()
                if i == 0 and first_stage_function:
                    # Only run first_stage_function the first time,
                    # no need to run it every time
                    first_stage_function(stage, url)

                # Checksum the archive and add it to the list
                version_hashes[version] = spack.util.crypto.checksum(
                    hashlib.sha256, stage.archive_file
                )
                i += 1
        except FailedDownloadError:
            errors.append("Failed to fetch {0}".format(url))
        except Exception as e:
            tty.msg("Something failed on {0}, skipping.  ({1})".format(url, e))

    for msg in errors:
        tty.debug(msg)

    if not version_hashes:
        tty.die("Could not fetch any versions for {0}".format(name))

    num_hash = len(version_hashes)
    tty.debug(
        "Checksummed {0} version{1} of {2}:".format(num_hash, "" if num_hash == 1 else "s", name)
    )

    return version_hashes


class StageError(spack.error.SpackError):
    """ "Superclass for all errors encountered during staging."""


class StagePathError(StageError):
    """ "Error encountered with stage path."""


class RestageError(StageError):
    """ "Error encountered during restaging."""


class VersionFetchError(StageError):
    """Raised when we can't determine a URL to fetch a package."""


# Keep this in namespace for convenience
FailedDownloadError = fs.FailedDownloadError
