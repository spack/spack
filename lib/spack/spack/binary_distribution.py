# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import collections
import hashlib
import io
import itertools
import json
import os
import pathlib
import re
import shutil
import sys
import tarfile
import tempfile
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import warnings
from contextlib import closing
from typing import Dict, Iterable, List, NamedTuple, Optional, Set, Tuple
from urllib.error import HTTPError, URLError

import llnl.util.filesystem as fsys
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, mkdirp, visit_directory_tree

import spack.caches
import spack.cmd
import spack.config as config
import spack.database as spack_db
import spack.error
import spack.hooks
import spack.hooks.sbang
import spack.mirror
import spack.oci.image
import spack.oci.oci
import spack.oci.opener
import spack.platforms
import spack.relocate as relocate
import spack.repo
import spack.stage
import spack.store
import spack.traverse as traverse
import spack.util.archive
import spack.util.crypto
import spack.util.file_cache as file_cache
import spack.util.gpg
import spack.util.path
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.timer as timer
import spack.util.url as url_util
import spack.util.web as web_util
from spack.caches import misc_cache_location
from spack.package_prefs import get_package_dir_permissions, get_package_group
from spack.relocate_text import utf8_paths_to_single_binary_regex
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import which

BUILD_CACHE_RELATIVE_PATH = "build_cache"
BUILD_CACHE_KEYS_RELATIVE_PATH = "_pgp"

#: The build cache layout version that this version of Spack creates.
#: Version 2: includes parent directories of the package prefix in the tarball
CURRENT_BUILD_CACHE_LAYOUT_VERSION = 2


class BuildCacheDatabase(spack_db.Database):
    """A database for binary buildcaches.

    A database supports writing buildcache index files, in which case certain fields are not
    needed in each install record, and no locking is required. To use this feature, it provides
    ``lock_cfg=NO_LOCK``, and override the list of ``record_fields``.
    """

    record_fields = ("spec", "ref_count", "in_buildcache")

    def __init__(self, root):
        super().__init__(root, lock_cfg=spack_db.NO_LOCK)
        self._write_transaction_impl = llnl.util.lang.nullcontext
        self._read_transaction_impl = llnl.util.lang.nullcontext


class FetchCacheError(Exception):
    """Error thrown when fetching the cache failed, usually a composite error list."""

    def __init__(self, errors):
        if not isinstance(errors, list):
            raise TypeError("Expected a list of errors")
        self.errors = errors
        if len(errors) > 1:
            msg = "        Error {0}: {1}: {2}"
            self.message = "Multiple errors during fetching:\n"
            self.message += "\n".join(
                (
                    msg.format(i + 1, err.__class__.__name__, str(err))
                    for (i, err) in enumerate(errors)
                )
            )
        else:
            err = errors[0]
            self.message = "{0}: {1}".format(err.__class__.__name__, str(err))
        super().__init__(self.message)


class ListMirrorSpecsError(spack.error.SpackError):
    """Raised when unable to retrieve list of specs from the mirror"""


class BinaryCacheIndex:
    """
    The BinaryCacheIndex tracks what specs are available on (usually remote)
    binary caches.

    This index is "best effort", in the sense that whenever we don't find
    what we're looking for here, we will attempt to fetch it directly from
    configured mirrors anyway.  Thus, it has the potential to speed things
    up, but cache misses shouldn't break any spack functionality.

    At the moment, everything in this class is initialized as lazily as
    possible, so that it avoids slowing anything in spack down until
    absolutely necessary.

    TODO: What's the cost if, e.g., we realize in the middle of a spack
    install that the cache is out of date, and we fetch directly?  Does it
    mean we should have paid the price to update the cache earlier?
    """

    def __init__(self, cache_root: Optional[str] = None):
        self._index_cache_root: str = cache_root or binary_index_location()

        # the key associated with the serialized _local_index_cache
        self._index_contents_key = "contents.json"

        # a FileCache instance storing copies of remote binary cache indices
        self._index_file_cache: Optional[file_cache.FileCache] = None

        # stores a map of mirror URL to index hash and cache key (index path)
        self._local_index_cache: Optional[dict] = None

        # hashes of remote indices already ingested into the concrete spec
        # cache (_mirrors_for_spec)
        self._specs_already_associated: Set[str] = set()

        # mapping from mirror urls to the time.time() of the last index fetch and a bool indicating
        # whether the fetch succeeded or not.
        self._last_fetch_times: Dict[str, float] = {}

        # _mirrors_for_spec is a dictionary mapping DAG hashes to lists of
        # entries indicating mirrors where that concrete spec can be found.
        # Each entry is a dictionary consisting of:
        #
        #     - the mirror where the spec is, keyed by ``mirror_url``
        #     - the concrete spec itself, keyed by ``spec`` (including the
        #           full hash, since the dag hash may match but we want to
        #           use the updated source if available)
        self._mirrors_for_spec: Dict[str, dict] = {}

    def _init_local_index_cache(self):
        if not self._index_file_cache:
            self._index_file_cache = file_cache.FileCache(self._index_cache_root)

            cache_key = self._index_contents_key
            self._index_file_cache.init_entry(cache_key)

            cache_path = self._index_file_cache.cache_path(cache_key)

            self._local_index_cache = {}
            if os.path.isfile(cache_path):
                with self._index_file_cache.read_transaction(cache_key) as cache_file:
                    self._local_index_cache = json.load(cache_file)

    def clear(self):
        """For testing purposes we need to be able to empty the cache and
        clear associated data structures."""
        if self._index_file_cache:
            self._index_file_cache.destroy()
            self._index_file_cache = None
        self._local_index_cache = None
        self._specs_already_associated = set()
        self._last_fetch_times = {}
        self._mirrors_for_spec = {}

    def _write_local_index_cache(self):
        self._init_local_index_cache()
        cache_key = self._index_contents_key
        with self._index_file_cache.write_transaction(cache_key) as (old, new):
            json.dump(self._local_index_cache, new)

    def regenerate_spec_cache(self, clear_existing=False):
        """Populate the local cache of concrete specs (``_mirrors_for_spec``)
        from the locally cached buildcache index files.  This is essentially a
        no-op if it has already been done, as we keep track of the index
        hashes for which we have already associated the built specs."""
        self._init_local_index_cache()

        if clear_existing:
            self._specs_already_associated = set()
            self._mirrors_for_spec = {}

        for mirror_url in self._local_index_cache:
            cache_entry = self._local_index_cache[mirror_url]
            cached_index_path = cache_entry["index_path"]
            cached_index_hash = cache_entry["index_hash"]
            if cached_index_hash not in self._specs_already_associated:
                self._associate_built_specs_with_mirror(cached_index_path, mirror_url)
                self._specs_already_associated.add(cached_index_hash)

    def _associate_built_specs_with_mirror(self, cache_key, mirror_url):
        tmpdir = tempfile.mkdtemp()

        try:
            db = BuildCacheDatabase(tmpdir)

            try:
                self._index_file_cache.init_entry(cache_key)
                cache_path = self._index_file_cache.cache_path(cache_key)
                with self._index_file_cache.read_transaction(cache_key):
                    db._read_from_file(cache_path)
            except spack_db.InvalidDatabaseVersionError as e:
                tty.warn(
                    f"you need a newer Spack version to read the buildcache index for the "
                    f"following mirror: '{mirror_url}'. {e.database_version_message}"
                )
                return

            spec_list = [
                s
                for s in db.query_local(installed=any, in_buildcache=any)
                if s.external or db.query_local_by_spec_hash(s.dag_hash()).in_buildcache
            ]

            for indexed_spec in spec_list:
                dag_hash = indexed_spec.dag_hash()

                if dag_hash not in self._mirrors_for_spec:
                    self._mirrors_for_spec[dag_hash] = []

                for entry in self._mirrors_for_spec[dag_hash]:
                    # A binary mirror can only have one spec per DAG hash, so
                    # if we already have an entry under this DAG hash for this
                    # mirror url, we're done.
                    if entry["mirror_url"] == mirror_url:
                        break
                else:
                    self._mirrors_for_spec[dag_hash].append(
                        {"mirror_url": mirror_url, "spec": indexed_spec}
                    )
        finally:
            shutil.rmtree(tmpdir)

    def get_all_built_specs(self):
        spec_list = []
        for dag_hash in self._mirrors_for_spec:
            # in the absence of further information, all concrete specs
            # with the same DAG hash are equivalent, so we can just
            # return the first one in the list.
            if len(self._mirrors_for_spec[dag_hash]) > 0:
                spec_list.append(self._mirrors_for_spec[dag_hash][0]["spec"])

        return spec_list

    def find_built_spec(self, spec, mirrors_to_check=None):
        """Look in our cache for the built spec corresponding to ``spec``.

        If the spec can be found among the configured binary mirrors, a
        list is returned that contains the concrete spec and the mirror url
        of each mirror where it can be found.  Otherwise, ``None`` is
        returned.

        This method does not trigger reading anything from remote mirrors, but
        rather just checks if the concrete spec is found within the cache.

        The cache can be updated by calling ``update()`` on the cache.

        Args:
            spec (spack.spec.Spec): Concrete spec to find
            mirrors_to_check: Optional mapping containing mirrors to check.  If
                None, just assumes all configured mirrors.

        Returns:
            An list of objects containing the found specs and mirror url where
                each can be found, e.g.:

                .. code-block:: python

                    [
                        {
                            "spec": <concrete-spec>,
                            "mirror_url": <mirror-root-url>
                        }
                    ]
        """
        return self.find_by_hash(spec.dag_hash(), mirrors_to_check=mirrors_to_check)

    def find_by_hash(self, find_hash, mirrors_to_check=None):
        """Same as find_built_spec but uses the hash of a spec.

        Args:
            find_hash (str): hash of the spec to search
            mirrors_to_check: Optional mapping containing mirrors to check.  If
                None, just assumes all configured mirrors.
        """
        if find_hash not in self._mirrors_for_spec:
            return []
        results = self._mirrors_for_spec[find_hash]
        if not mirrors_to_check:
            return results
        mirror_urls = mirrors_to_check.values()
        return [r for r in results if r["mirror_url"] in mirror_urls]

    def update_spec(self, spec, found_list):
        """
        Take list of {'mirror_url': m, 'spec': s} objects and update the local
        built_spec_cache
        """
        spec_dag_hash = spec.dag_hash()

        if spec_dag_hash not in self._mirrors_for_spec:
            self._mirrors_for_spec[spec_dag_hash] = found_list
        else:
            current_list = self._mirrors_for_spec[spec_dag_hash]
            for new_entry in found_list:
                for cur_entry in current_list:
                    if new_entry["mirror_url"] == cur_entry["mirror_url"]:
                        cur_entry["spec"] = new_entry["spec"]
                        break
                else:
                    current_list.append(
                        {"mirror_url": new_entry["mirror_url"], "spec": new_entry["spec"]}
                    )

    def update(self, with_cooldown=False):
        """Make sure local cache of buildcache index files is up to date.
        If the same mirrors are configured as the last time this was called
        and none of the remote buildcache indices have changed, calling this
        method will only result in fetching the index hash from each mirror
        to confirm it is the same as what is stored locally.  Otherwise, the
        buildcache ``index.json`` and ``index.json.hash`` files are retrieved
        from each configured mirror and stored locally (both in memory and
        on disk under ``_index_cache_root``)."""
        self._init_local_index_cache()
        configured_mirror_urls = [
            m.fetch_url for m in spack.mirror.MirrorCollection(binary=True).values()
        ]
        items_to_remove = []
        spec_cache_clear_needed = False
        spec_cache_regenerate_needed = not self._mirrors_for_spec

        # First compare the mirror urls currently present in the cache to the
        # configured mirrors.  If we have a cached index for a mirror which is
        # no longer configured, we should remove it from the cache.  For any
        # cached indices corresponding to currently configured mirrors, we need
        # to check if the cache is still good, or needs to be updated.
        # Finally, if there are configured mirrors for which we don't have a
        # cache entry, we need to fetch and cache the indices from those
        # mirrors.

        # If, during this process, we find that any mirrors for which we
        # already have entries have either been removed, or their index
        # hash has changed, then our concrete spec cache (_mirrors_for_spec)
        # likely has entries that need to be removed, so we will clear it
        # and regenerate that data structure.

        # If, during this process, we find that there are new mirrors for
        # which do not yet have an entry in our index cache, then we simply
        # need to regenerate the concrete spec cache, but do not need to
        # clear it first.

        # Otherwise the concrete spec cache should not need to be updated at
        # all.

        fetch_errors = []
        all_methods_failed = True
        ttl = spack.config.get("config:binary_index_ttl", 600)
        now = time.time()

        for cached_mirror_url in self._local_index_cache:
            cache_entry = self._local_index_cache[cached_mirror_url]
            cached_index_path = cache_entry["index_path"]
            if cached_mirror_url in configured_mirror_urls:
                # Only do a fetch if the last fetch was longer than TTL ago
                if (
                    with_cooldown
                    and ttl > 0
                    and cached_mirror_url in self._last_fetch_times
                    and now - self._last_fetch_times[cached_mirror_url][0] < ttl
                ):
                    # We're in the cooldown period, don't try to fetch again
                    # If the fetch succeeded last time, consider this update a success, otherwise
                    # re-report the error here
                    if self._last_fetch_times[cached_mirror_url][1]:
                        all_methods_failed = False
                else:
                    # May need to fetch the index and update the local caches
                    try:
                        needs_regen = self._fetch_and_cache_index(
                            cached_mirror_url, cache_entry=cache_entry
                        )
                        self._last_fetch_times[cached_mirror_url] = (now, True)
                        all_methods_failed = False
                    except FetchIndexError as e:
                        needs_regen = False
                        fetch_errors.append(e)
                        self._last_fetch_times[cached_mirror_url] = (now, False)
                    # The need to regenerate implies a need to clear as well.
                    spec_cache_clear_needed |= needs_regen
                    spec_cache_regenerate_needed |= needs_regen
            else:
                # No longer have this mirror, cached index should be removed
                items_to_remove.append(
                    {
                        "url": cached_mirror_url,
                        "cache_key": os.path.join(self._index_cache_root, cached_index_path),
                    }
                )
                if cached_mirror_url in self._last_fetch_times:
                    del self._last_fetch_times[cached_mirror_url]
                spec_cache_clear_needed = True
                spec_cache_regenerate_needed = True

        # Clean up items to be removed, identified above
        for item in items_to_remove:
            url = item["url"]
            cache_key = item["cache_key"]
            self._index_file_cache.remove(cache_key)
            del self._local_index_cache[url]

        # Iterate the configured mirrors now.  Any mirror urls we do not
        # already have in our cache must be fetched, stored, and represented
        # locally.
        for mirror_url in configured_mirror_urls:
            if mirror_url in self._local_index_cache:
                continue

            # Need to fetch the index and update the local caches
            try:
                needs_regen = self._fetch_and_cache_index(mirror_url)
                self._last_fetch_times[mirror_url] = (now, True)
                all_methods_failed = False
            except FetchIndexError as e:
                fetch_errors.append(e)
                needs_regen = False
                self._last_fetch_times[mirror_url] = (now, False)
            # Generally speaking, a new mirror wouldn't imply the need to
            # clear the spec cache, so leave it as is.
            if needs_regen:
                spec_cache_regenerate_needed = True

        self._write_local_index_cache()

        if configured_mirror_urls and all_methods_failed:
            raise FetchCacheError(fetch_errors)
        if fetch_errors:
            tty.warn(
                "The following issues were ignored while updating the indices of binary caches",
                FetchCacheError(fetch_errors),
            )
        if spec_cache_regenerate_needed:
            self.regenerate_spec_cache(clear_existing=spec_cache_clear_needed)

    def _fetch_and_cache_index(self, mirror_url, cache_entry={}):
        """Fetch a buildcache index file from a remote mirror and cache it.

        If we already have a cached index from this mirror, then we first
        check if the hash has changed, and we avoid fetching it if not.

        Args:
            mirror_url (str): Base url of mirror
            cache_entry (dict): Old cache metadata with keys ``index_hash``, ``index_path``,
                ``etag``

        Returns:
            True if the local index.json was updated.

        Throws:
            FetchIndexError
        """
        # TODO: get rid of this request, handle 404 better
        scheme = urllib.parse.urlparse(mirror_url).scheme

        if scheme != "oci" and not web_util.url_exists(
            url_util.join(mirror_url, BUILD_CACHE_RELATIVE_PATH, "index.json")
        ):
            return False

        if scheme == "oci":
            # TODO: Actually etag and OCI are not mutually exclusive...
            fetcher = OCIIndexFetcher(mirror_url, cache_entry.get("index_hash", None))
        elif cache_entry.get("etag"):
            fetcher = EtagIndexFetcher(mirror_url, cache_entry["etag"])
        else:
            fetcher = DefaultIndexFetcher(
                mirror_url, local_hash=cache_entry.get("index_hash", None)
            )

        result = fetcher.conditional_fetch()

        # Nothing to do
        if result.fresh:
            return False

        # Persist new index.json
        url_hash = compute_hash(mirror_url)
        cache_key = "{}_{}.json".format(url_hash[:10], result.hash[:10])
        self._index_file_cache.init_entry(cache_key)
        with self._index_file_cache.write_transaction(cache_key) as (old, new):
            new.write(result.data)

        self._local_index_cache[mirror_url] = {
            "index_hash": result.hash,
            "index_path": cache_key,
            "etag": result.etag,
        }

        # clean up the old cache_key if necessary
        old_cache_key = cache_entry.get("index_path", None)
        if old_cache_key:
            self._index_file_cache.remove(old_cache_key)

        # We fetched an index and updated the local index cache, we should
        # regenerate the spec cache as a result.
        return True


def binary_index_location():
    """Set up a BinaryCacheIndex for remote buildcache dbs in the user's homedir."""
    cache_root = os.path.join(misc_cache_location(), "indices")
    return spack.util.path.canonicalize_path(cache_root)


#: Default binary cache index instance
BINARY_INDEX: BinaryCacheIndex = llnl.util.lang.Singleton(BinaryCacheIndex)  # type: ignore


class NoOverwriteException(spack.error.SpackError):
    """Raised when a file would be overwritten"""

    def __init__(self, file_path):
        super().__init__(f"Refusing to overwrite the following file: {file_path}")


class NoGpgException(spack.error.SpackError):
    """
    Raised when gpg2 is not in PATH
    """

    def __init__(self, msg):
        super().__init__(msg)


class NoKeyException(spack.error.SpackError):
    """
    Raised when gpg has no default key added.
    """

    def __init__(self, msg):
        super().__init__(msg)


class PickKeyException(spack.error.SpackError):
    """
    Raised when multiple keys can be used to sign.
    """

    def __init__(self, keys):
        err_msg = "Multiple keys available for signing\n%s\n" % keys
        err_msg += "Use spack buildcache create -k <key hash> to pick a key."
        super().__init__(err_msg)


class NoVerifyException(spack.error.SpackError):
    """
    Raised if file fails signature verification.
    """

    pass


class NoChecksumException(spack.error.SpackError):
    """
    Raised if file fails checksum verification.
    """

    def __init__(self, path, size, contents, algorithm, expected, computed):
        super().__init__(
            f"{algorithm} checksum failed for {path}",
            f"Expected {expected} but got {computed}. "
            f"File size = {size} bytes. Contents = {contents!r}",
        )


class NewLayoutException(spack.error.SpackError):
    """
    Raised if directory layout is different from buildcache.
    """

    def __init__(self, msg):
        super().__init__(msg)


class InvalidMetadataFile(spack.error.SpackError):
    pass


class UnsignedPackageException(spack.error.SpackError):
    """
    Raised if installation of unsigned package is attempted without
    the use of ``--no-check-signature``.
    """


def compute_hash(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def build_cache_relative_path():
    return BUILD_CACHE_RELATIVE_PATH


def build_cache_keys_relative_path():
    return BUILD_CACHE_KEYS_RELATIVE_PATH


def build_cache_prefix(prefix):
    return os.path.join(prefix, build_cache_relative_path())


def buildinfo_file_name(prefix):
    """Filename of the binary package meta-data file"""
    return os.path.join(prefix, ".spack", "binary_distribution")


def read_buildinfo_file(prefix):
    """Read buildinfo file"""
    with open(buildinfo_file_name(prefix), "r") as f:
        return syaml.load(f)


class BuildManifestVisitor(BaseDirectoryVisitor):
    """Visitor that collects a list of files and symlinks
    that can be checked for need of relocation. It knows how
    to dedupe hardlinks and deal with symlinks to files and
    directories."""

    def __init__(self):
        # Save unique identifiers of hardlinks to avoid relocating them multiple times
        self.visited = set()

        # Lists of files we will check
        self.files = []
        self.symlinks = []

    def seen_before(self, root, rel_path):
        stat_result = os.lstat(os.path.join(root, rel_path))
        if stat_result.st_nlink == 1:
            return False
        identifier = (stat_result.st_dev, stat_result.st_ino)
        if identifier in self.visited:
            return True
        else:
            self.visited.add(identifier)
            return False

    def visit_file(self, root, rel_path, depth):
        if self.seen_before(root, rel_path):
            return
        self.files.append(rel_path)

    def visit_symlinked_file(self, root, rel_path, depth):
        # Note: symlinks *can* be hardlinked, but it is unclear if
        # symlinks can be relinked in-place (preserving inode).
        # Therefore, we do *not* de-dupe hardlinked symlinks.
        self.symlinks.append(rel_path)

    def before_visit_dir(self, root, rel_path, depth):
        return os.path.basename(rel_path) not in (".spack", "man")

    def before_visit_symlinked_dir(self, root, rel_path, depth):
        # Treat symlinked directories simply as symlinks.
        self.visit_symlinked_file(root, rel_path, depth)
        # Never recurse into symlinked directories.
        return False


def file_matches(path, regex):
    with open(path, "rb") as f:
        contents = f.read()
    return bool(regex.search(contents))


def get_buildfile_manifest(spec):
    """
    Return a data structure with information about a build, including
    text_to_relocate, binary_to_relocate, binary_to_relocate_fullpath
    link_to_relocate, and other, which means it doesn't fit any of previous
    checks (and should not be relocated). We exclude docs (man) and
    metadata (.spack). This can be used to find a particular kind of file
    in spack, or to generate the build metadata.
    """
    data = {
        "text_to_relocate": [],
        "binary_to_relocate": [],
        "link_to_relocate": [],
        "other": [],
        "binary_to_relocate_fullpath": [],
        "hardlinks_deduped": True,
    }

    # Guard against filesystem footguns of hardlinks and symlinks by using
    # a visitor to retrieve a list of files and symlinks, so we don't have
    # to worry about hardlinks of symlinked dirs and what not.
    visitor = BuildManifestVisitor()
    root = spec.prefix
    visit_directory_tree(root, visitor)

    # Collect a list of prefixes for this package and it's dependencies, Spack will
    # look for them to decide if text file needs to be relocated or not
    prefixes = [d.prefix for d in spec.traverse(root=True, deptype="all") if not d.external]
    prefixes.append(spack.hooks.sbang.sbang_install_path())
    prefixes.append(str(spack.store.STORE.layout.root))

    # Create a giant regex that matches all prefixes
    regex = utf8_paths_to_single_binary_regex(prefixes)

    # Symlinks.

    # Obvious bugs:
    #   1. relative links are not relocated.
    #   2. paths are used as strings.
    for rel_path in visitor.symlinks:
        abs_path = os.path.join(root, rel_path)
        link = os.readlink(abs_path)
        if os.path.isabs(link) and link.startswith(spack.store.STORE.layout.root):
            data["link_to_relocate"].append(rel_path)

    # Non-symlinks.
    for rel_path in visitor.files:
        abs_path = os.path.join(root, rel_path)
        m_type, m_subtype = fsys.mime_type(abs_path)

        if relocate.needs_binary_relocation(m_type, m_subtype):
            # Why is this branch not part of needs_binary_relocation? :(
            if (
                (
                    m_subtype in ("x-executable", "x-sharedlib", "x-pie-executable")
                    and sys.platform != "darwin"
                )
                or (m_subtype in ("x-mach-binary") and sys.platform == "darwin")
                or (not rel_path.endswith(".o"))
            ):
                data["binary_to_relocate"].append(rel_path)
                data["binary_to_relocate_fullpath"].append(abs_path)
                continue

        elif relocate.needs_text_relocation(m_type, m_subtype) and file_matches(abs_path, regex):
            data["text_to_relocate"].append(rel_path)
            continue

        data["other"].append(abs_path)

    return data


def hashes_to_prefixes(spec):
    """Return a dictionary of hashes to prefixes for a spec and its deps, excluding externals"""
    return {
        s.dag_hash(): str(s.prefix)
        for s in itertools.chain(
            spec.traverse(root=True, deptype="link"), spec.dependencies(deptype="run")
        )
        if not s.external
    }


def get_buildinfo_dict(spec):
    """Create metadata for a tarball"""
    manifest = get_buildfile_manifest(spec)

    return {
        "sbang_install_path": spack.hooks.sbang.sbang_install_path(),
        "buildpath": spack.store.STORE.layout.root,
        "spackprefix": spack.paths.prefix,
        "relative_prefix": os.path.relpath(spec.prefix, spack.store.STORE.layout.root),
        "relocate_textfiles": manifest["text_to_relocate"],
        "relocate_binaries": manifest["binary_to_relocate"],
        "relocate_links": manifest["link_to_relocate"],
        "hardlinks_deduped": manifest["hardlinks_deduped"],
        "hash_to_prefix": hashes_to_prefixes(spec),
    }


def tarball_directory_name(spec):
    """
    Return name of the tarball directory according to the convention
    <os>-<architecture>/<compiler>/<package>-<version>/
    """
    return spec.format_path("{architecture}/{compiler.name}-{compiler.version}/{name}-{version}")


def tarball_name(spec, ext):
    """
    Return the name of the tarfile according to the convention
    <os>-<architecture>-<package>-<dag_hash><ext>
    """
    spec_formatted = spec.format_path(
        "{architecture}-{compiler.name}-{compiler.version}-{name}-{version}-{hash}"
    )
    return f"{spec_formatted}{ext}"


def tarball_path_name(spec, ext):
    """
    Return the full path+name for a given spec according to the convention
    <tarball_directory_name>/<tarball_name>
    """
    return os.path.join(tarball_directory_name(spec), tarball_name(spec, ext))


def select_signing_key(key=None):
    if key is None:
        keys = spack.util.gpg.signing_keys()
        if len(keys) == 1:
            key = keys[0]

        if len(keys) > 1:
            raise PickKeyException(str(keys))

        if len(keys) == 0:
            raise NoKeyException(
                "No default key available for signing.\n"
                "Use spack gpg init and spack gpg create"
                " to create a default key."
            )
    return key


def sign_specfile(key, force, specfile_path):
    signed_specfile_path = "%s.sig" % specfile_path
    if os.path.exists(signed_specfile_path):
        if force:
            os.remove(signed_specfile_path)
        else:
            raise NoOverwriteException(signed_specfile_path)

    key = select_signing_key(key)
    spack.util.gpg.sign(key, specfile_path, signed_specfile_path, clearsign=True)


def _read_specs_and_push_index(file_list, read_method, cache_prefix, db, temp_dir, concurrency):
    """Read all the specs listed in the provided list, using thread given thread parallelism,
        generate the index, and push it to the mirror.

    Args:
        file_list (list(str)): List of urls or file paths pointing at spec files to read
        read_method: A function taking a single argument, either a url or a file path,
            and which reads the spec file at that location, and returns the spec.
        cache_prefix (str): prefix of the build cache on s3 where index should be pushed.
        db: A spack database used for adding specs and then writing the index.
        temp_dir (str): Location to write index.json and hash for pushing
        concurrency (int): Number of parallel processes to use when fetching
    """
    for file in file_list:
        contents = read_method(file)
        # Need full spec.json name or this gets confused with index.json.
        if file.endswith(".json.sig"):
            specfile_json = Spec.extract_json_from_clearsig(contents)
            fetched_spec = Spec.from_dict(specfile_json)
        elif file.endswith(".json"):
            fetched_spec = Spec.from_json(contents)
        else:
            continue

        db.add(fetched_spec, None)
        db.mark(fetched_spec, "in_buildcache", True)

    # Now generate the index, compute its hash, and push the two files to
    # the mirror.
    index_json_path = os.path.join(temp_dir, "index.json")
    with open(index_json_path, "w") as f:
        db._write_to_file(f)

    # Read the index back in and compute its hash
    with open(index_json_path) as f:
        index_string = f.read()
        index_hash = compute_hash(index_string)

    # Write the hash out to a local file
    index_hash_path = os.path.join(temp_dir, "index.json.hash")
    with open(index_hash_path, "w") as f:
        f.write(index_hash)

    # Push the index itself
    web_util.push_to_url(
        index_json_path,
        url_util.join(cache_prefix, "index.json"),
        keep_original=False,
        extra_args={"ContentType": "application/json", "CacheControl": "no-cache"},
    )

    # Push the hash
    web_util.push_to_url(
        index_hash_path,
        url_util.join(cache_prefix, "index.json.hash"),
        keep_original=False,
        extra_args={"ContentType": "text/plain", "CacheControl": "no-cache"},
    )


def _specs_from_cache_aws_cli(cache_prefix):
    """Use aws cli to sync all the specs into a local temporary directory.

    Args:
        cache_prefix (str): prefix of the build cache on s3

    Return:
        List of the local file paths and a function that can read each one from the file system.
    """
    read_fn = None
    file_list = None
    aws = which("aws")

    def file_read_method(file_path):
        with open(file_path) as fd:
            return fd.read()

    tmpspecsdir = tempfile.mkdtemp()
    sync_command_args = [
        "s3",
        "sync",
        "--exclude",
        "*",
        "--include",
        "*.spec.json.sig",
        "--include",
        "*.spec.json",
        cache_prefix,
        tmpspecsdir,
    ]

    try:
        tty.debug(
            "Using aws s3 sync to download specs from {0} to {1}".format(cache_prefix, tmpspecsdir)
        )
        aws(*sync_command_args, output=os.devnull, error=os.devnull)
        file_list = fsys.find(tmpspecsdir, ["*.spec.json.sig", "*.spec.json"])
        read_fn = file_read_method
    except Exception:
        tty.warn("Failed to use aws s3 sync to retrieve specs, falling back to parallel fetch")
        shutil.rmtree(tmpspecsdir)

    return file_list, read_fn


def _specs_from_cache_fallback(cache_prefix):
    """Use spack.util.web module to get a list of all the specs at the remote url.

    Args:
        cache_prefix (str): Base url of mirror (location of spec files)

    Return:
        The list of complete spec file urls and a function that can read each one from its
            remote location (also using the spack.util.web module).
    """
    read_fn = None
    file_list = None

    def url_read_method(url):
        contents = None
        try:
            _, _, spec_file = web_util.read_from_url(url)
            contents = codecs.getreader("utf-8")(spec_file).read()
        except (URLError, web_util.SpackWebError) as url_err:
            tty.error("Error reading specfile: {0}".format(url))
            tty.error(url_err)
        return contents

    try:
        file_list = [
            url_util.join(cache_prefix, entry)
            for entry in web_util.list_url(cache_prefix)
            if entry.endswith("spec.json") or entry.endswith("spec.json.sig")
        ]
        read_fn = url_read_method
    except KeyError as inst:
        msg = "No packages at {0}: {1}".format(cache_prefix, inst)
        tty.warn(msg)
    except Exception as err:
        # If we got some kind of S3 (access denied or other connection
        # error), the first non boto-specific class in the exception
        # hierarchy is Exception.  Just print a warning and return
        msg = "Encountered problem listing packages at {0}: {1}".format(cache_prefix, err)
        tty.warn(msg)

    return file_list, read_fn


def _spec_files_from_cache(cache_prefix):
    """Get a list of all the spec files in the mirror and a function to
    read them.

    Args:
        cache_prefix (str): Base url of mirror (location of spec files)

    Return:
        A tuple where the first item is a list of absolute file paths or
        urls pointing to the specs that should be read from the mirror,
        and the second item is a function taking a url or file path and
        returning the spec read from that location.
    """
    callbacks = []
    if cache_prefix.startswith("s3"):
        callbacks.append(_specs_from_cache_aws_cli)

    callbacks.append(_specs_from_cache_fallback)

    for specs_from_cache_fn in callbacks:
        file_list, read_fn = specs_from_cache_fn(cache_prefix)
        if file_list:
            return file_list, read_fn

    raise ListMirrorSpecsError("Failed to get list of specs from {0}".format(cache_prefix))


def generate_package_index(cache_prefix, concurrency=32):
    """Create or replace the build cache index on the given mirror.  The
    buildcache index contains an entry for each binary package under the
    cache_prefix.

    Args:
        cache_prefix(str): Base url of binary mirror.
        concurrency: (int): The desired threading concurrency to use when
            fetching the spec files from the mirror.

    Return:
        None
    """
    try:
        file_list, read_fn = _spec_files_from_cache(cache_prefix)
    except ListMirrorSpecsError as err:
        tty.error("Unable to generate package index, {0}".format(err))
        return

    tty.debug("Retrieving spec descriptor files from {0} to build index".format(cache_prefix))

    tmpdir = tempfile.mkdtemp()

    db = BuildCacheDatabase(tmpdir)
    db.root = None
    db_root_dir = db.database_directory

    try:
        _read_specs_and_push_index(file_list, read_fn, cache_prefix, db, db_root_dir, concurrency)
    except Exception as err:
        msg = "Encountered problem pushing package index to {0}: {1}".format(cache_prefix, err)
        tty.warn(msg)
        tty.debug("\n" + traceback.format_exc())
    finally:
        shutil.rmtree(tmpdir)


def generate_key_index(key_prefix, tmpdir=None):
    """Create the key index page.

    Creates (or replaces) the "index.json" page at the location given in
    key_prefix.  This page contains an entry for each key (.pub) under
    key_prefix.
    """

    tty.debug(
        " ".join(
            ("Retrieving key.pub files from", url_util.format(key_prefix), "to build key index")
        )
    )

    try:
        fingerprints = (
            entry[:-4]
            for entry in web_util.list_url(key_prefix, recursive=False)
            if entry.endswith(".pub")
        )
    except KeyError as inst:
        msg = "No keys at {0}: {1}".format(key_prefix, inst)
        tty.warn(msg)
        return
    except Exception as err:
        # If we got some kind of S3 (access denied or other connection
        # error), the first non boto-specific class in the exception
        # hierarchy is Exception.  Just print a warning and return
        msg = "Encountered problem listing keys at {0}: {1}".format(key_prefix, err)
        tty.warn(msg)
        return

    remove_tmpdir = False

    keys_local = url_util.local_file_path(key_prefix)
    if keys_local:
        target = os.path.join(keys_local, "index.json")
    else:
        if not tmpdir:
            tmpdir = tempfile.mkdtemp()
            remove_tmpdir = True
        target = os.path.join(tmpdir, "index.json")

    index = {"keys": dict((fingerprint, {}) for fingerprint in sorted(set(fingerprints)))}
    with open(target, "w") as f:
        sjson.dump(index, f)

    if not keys_local:
        try:
            web_util.push_to_url(
                target,
                url_util.join(key_prefix, "index.json"),
                keep_original=False,
                extra_args={"ContentType": "application/json"},
            )
        except Exception as err:
            msg = "Encountered problem pushing key index to {0}: {1}".format(key_prefix, err)
            tty.warn(msg)
        finally:
            if remove_tmpdir:
                shutil.rmtree(tmpdir)


def tarfile_of_spec_prefix(tar: tarfile.TarFile, prefix: str) -> None:
    """Create a tarfile of an install prefix of a spec. Skips existing buildinfo file.

    Args:
        tar: tarfile object to add files to
        prefix: absolute install prefix of spec"""
    if not os.path.isabs(prefix) or not os.path.isdir(prefix):
        raise ValueError(f"prefix '{prefix}' must be an absolute path to a directory")
    stat_key = lambda stat: (stat.st_dev, stat.st_ino)

    try:  # skip buildinfo file if it exists
        files_to_skip = [stat_key(os.lstat(buildinfo_file_name(prefix)))]
        skip = lambda entry: stat_key(entry.stat(follow_symlinks=False)) in files_to_skip
    except OSError:
        skip = lambda entry: False

    spack.util.archive.reproducible_tarfile_from_prefix(
        tar,
        prefix,
        # Spack <= 0.21 did not include parent directories, leading to issues when tarballs are
        # used in runtimes like AWS lambda.
        include_parent_directories=True,
        skip=skip,
    )


def _do_create_tarball(tarfile_path: str, binaries_dir: str, buildinfo: dict):
    with spack.util.archive.gzip_compressed_tarfile(tarfile_path) as (
        tar,
        inner_checksum,
        outer_checksum,
    ):
        # Tarball the install prefix
        tarfile_of_spec_prefix(tar, binaries_dir)

        # Serialize buildinfo for the tarball
        bstring = syaml.dump(buildinfo, default_flow_style=True).encode("utf-8")
        tarinfo = tarfile.TarInfo(
            name=spack.util.archive.default_path_to_name(buildinfo_file_name(binaries_dir))
        )
        tarinfo.type = tarfile.REGTYPE
        tarinfo.size = len(bstring)
        tarinfo.mode = 0o644
        tar.addfile(tarinfo, io.BytesIO(bstring))

    return inner_checksum.hexdigest(), outer_checksum.hexdigest()


class PushOptions(NamedTuple):
    #: Overwrite existing tarball/metadata files in buildcache
    force: bool = False

    #: Regenerated indices after pushing
    regenerate_index: bool = False

    #: Whether to sign or not.
    unsigned: bool = False

    #: What key to use for signing
    key: Optional[str] = None


def push_or_raise(spec: Spec, out_url: str, options: PushOptions):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).

    This method raises :py:class:`NoOverwriteException` when ``force=False`` and the tarball or
    spec.json file already exist in the buildcache.
    """
    if not spec.concrete:
        raise ValueError("spec must be concrete to build tarball")

    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpdir:
        _build_tarball_in_stage_dir(spec, out_url, stage_dir=tmpdir, options=options)


def _build_tarball_in_stage_dir(spec: Spec, out_url: str, stage_dir: str, options: PushOptions):
    cache_prefix = build_cache_prefix(stage_dir)
    tarfile_name = tarball_name(spec, ".spack")
    tarfile_dir = os.path.join(cache_prefix, tarball_directory_name(spec))
    tarfile_path = os.path.join(tarfile_dir, tarfile_name)
    spackfile_path = os.path.join(cache_prefix, tarball_path_name(spec, ".spack"))
    remote_spackfile_path = url_util.join(out_url, os.path.relpath(spackfile_path, stage_dir))

    mkdirp(tarfile_dir)
    if web_util.url_exists(remote_spackfile_path):
        if options.force:
            web_util.remove_url(remote_spackfile_path)
        else:
            raise NoOverwriteException(url_util.format(remote_spackfile_path))

    # need to copy the spec file so the build cache can be downloaded
    # without concretizing with the current spack packages
    # and preferences

    spec_file = spack.store.STORE.layout.spec_file_path(spec)
    specfile_name = tarball_name(spec, ".spec.json")
    specfile_path = os.path.realpath(os.path.join(cache_prefix, specfile_name))
    signed_specfile_path = "{0}.sig".format(specfile_path)

    remote_specfile_path = url_util.join(
        out_url, os.path.relpath(specfile_path, os.path.realpath(stage_dir))
    )
    remote_signed_specfile_path = "{0}.sig".format(remote_specfile_path)

    # If force and exists, overwrite. Otherwise raise exception on collision.
    if options.force:
        if web_util.url_exists(remote_specfile_path):
            web_util.remove_url(remote_specfile_path)
        if web_util.url_exists(remote_signed_specfile_path):
            web_util.remove_url(remote_signed_specfile_path)
    elif web_util.url_exists(remote_specfile_path) or web_util.url_exists(
        remote_signed_specfile_path
    ):
        raise NoOverwriteException(url_util.format(remote_specfile_path))

    binaries_dir = spec.prefix

    # create info for later relocation and create tar
    buildinfo = get_buildinfo_dict(spec)

    checksum, _ = _do_create_tarball(tarfile_path, binaries_dir, buildinfo)

    # add sha256 checksum to spec.json
    with open(spec_file, "r") as inputfile:
        content = inputfile.read()
        if spec_file.endswith(".json"):
            spec_dict = sjson.load(content)
        else:
            raise ValueError("{0} not a valid spec file type".format(spec_file))
    spec_dict["buildcache_layout_version"] = CURRENT_BUILD_CACHE_LAYOUT_VERSION
    spec_dict["binary_cache_checksum"] = {"hash_algorithm": "sha256", "hash": checksum}

    with open(specfile_path, "w") as outfile:
        # Note: when using gpg clear sign, we need to avoid long lines (19995 chars).
        # If lines are longer, they are truncated without error. Thanks GPG!
        # So, here we still add newlines, but no indent, so save on file size and
        # line length.
        json.dump(spec_dict, outfile, indent=0, separators=(",", ":"))

    # sign the tarball and spec file with gpg
    if not options.unsigned:
        key = select_signing_key(options.key)
        sign_specfile(key, options.force, specfile_path)

    # push tarball and signed spec json to remote mirror
    web_util.push_to_url(spackfile_path, remote_spackfile_path, keep_original=False)
    web_util.push_to_url(
        signed_specfile_path if not options.unsigned else specfile_path,
        remote_signed_specfile_path if not options.unsigned else remote_specfile_path,
        keep_original=False,
    )

    # push the key to the build cache's _pgp directory so it can be
    # imported
    if not options.unsigned:
        push_keys(out_url, keys=[key], regenerate_index=options.regenerate_index, tmpdir=stage_dir)

    # create an index.json for the build_cache directory so specs can be
    # found
    if options.regenerate_index:
        generate_package_index(url_util.join(out_url, os.path.relpath(cache_prefix, stage_dir)))

    return None


class NotInstalledError(spack.error.SpackError):
    """Raised when a spec is not installed but picked to be packaged."""

    def __init__(self, specs: List[Spec]):
        super().__init__(
            "Cannot push non-installed packages",
            ", ".join(s.cformat("{name}{@version}{/hash:7}") for s in specs),
        )


def specs_to_be_packaged(
    specs: List[Spec], root: bool = True, dependencies: bool = True
) -> List[Spec]:
    """Return the list of nodes to be packaged, given a list of specs.
    Raises NotInstalledError if a spec is not installed but picked to be packaged.

    Args:
        specs: list of root specs to be processed
        root: include the root of each spec in the nodes
        dependencies: include the dependencies of each
            spec in the nodes
    """

    if not root and not dependencies:
        return []

    # Filter packageable roots
    with spack.store.STORE.db.read_transaction():
        if root:
            # Error on uninstalled roots, when roots are requested
            uninstalled_roots = list(s for s in specs if not s.installed)
            if uninstalled_roots:
                raise NotInstalledError(uninstalled_roots)
            roots = specs
        else:
            roots = []

        if dependencies:
            # Error on uninstalled deps, when deps are requested
            deps = list(
                traverse.traverse_nodes(
                    specs, deptype="all", order="breadth", root=False, key=traverse.by_dag_hash
                )
            )
            uninstalled_deps = list(s for s in deps if not s.installed)
            if uninstalled_deps:
                raise NotInstalledError(uninstalled_deps)
        else:
            deps = []

    return [s for s in itertools.chain(roots, deps) if not s.external]


def push(spec: Spec, mirror_url: str, options: PushOptions):
    """Create and push binary package for a single spec to the specified
    mirror url.

    Args:
        spec: Spec to package and push
        mirror_url: Desired destination url for binary package
        options:

    Returns:
        True if package was pushed, False otherwise.

    """
    try:
        push_or_raise(spec, mirror_url, options)
    except NoOverwriteException as e:
        warnings.warn(str(e))
        return False

    return True


def try_verify(specfile_path):
    """Utility function to attempt to verify a local file.  Assumes the
    file is a clearsigned signature file.

    Args:
        specfile_path (str): Path to file to be verified.

    Returns:
        ``True`` if the signature could be verified, ``False`` otherwise.
    """
    suppress = config.get("config:suppress_gpg_warnings", False)

    try:
        spack.util.gpg.verify(specfile_path, suppress_warnings=suppress)
    except Exception:
        return False

    return True


def try_fetch(url_to_fetch):
    """Utility function to try and fetch a file from a url, stage it
    locally, and return the path to the staged file.

    Args:
        url_to_fetch (str): Url pointing to remote resource to fetch

    Returns:
        Path to locally staged resource or ``None`` if it could not be fetched.
    """
    stage = Stage(url_to_fetch, keep=True)
    stage.create()

    try:
        stage.fetch()
    except spack.error.FetchError:
        stage.destroy()
        return None

    return stage


def _delete_staged_downloads(download_result):
    """Clean up stages used to download tarball and specfile"""
    download_result["tarball_stage"].destroy()
    download_result["specfile_stage"].destroy()


def _get_valid_spec_file(path: str, max_supported_layout: int) -> Tuple[Dict, int]:
    """Read and validate a spec file, returning the spec dict with its layout version, or raising
    InvalidMetadataFile if invalid."""
    try:
        with open(path, "rb") as f:
            binary_content = f.read()
    except OSError:
        raise InvalidMetadataFile(f"No such file: {path}")

    # In the future we may support transparently decompressing compressed spec files.
    if binary_content[:2] == b"\x1f\x8b":
        raise InvalidMetadataFile("Compressed spec files are not supported")

    try:
        as_string = binary_content.decode("utf-8")
        if path.endswith(".json.sig"):
            spec_dict = Spec.extract_json_from_clearsig(as_string)
        else:
            spec_dict = json.loads(as_string)
    except Exception as e:
        raise InvalidMetadataFile(f"Could not parse {path} due to: {e}") from e

    # Ensure this version is not too new.
    try:
        layout_version = int(spec_dict.get("buildcache_layout_version", 0))
    except ValueError as e:
        raise InvalidMetadataFile("Could not parse layout version") from e

    if layout_version > max_supported_layout:
        raise InvalidMetadataFile(
            f"Layout version {layout_version} is too new for this version of Spack"
        )

    return spec_dict, layout_version


def download_tarball(spec, unsigned: Optional[bool] = False, mirrors_for_spec=None):
    """
    Download binary tarball for given package into stage area, returning
    path to downloaded tarball if successful, None otherwise.

    Args:
        spec (spack.spec.Spec): Concrete spec
        unsigned: if ``True`` or ``False`` override the mirror signature verification defaults
        mirrors_for_spec (list): Optional list of concrete specs and mirrors
            obtained by calling binary_distribution.get_mirrors_for_spec().
            These will be checked in order first before looking in other
            configured mirrors.

    Returns:
        ``None`` if the tarball could not be downloaded (maybe also verified,
        depending on whether new-style signed binary packages were found).
        Otherwise, return an object indicating the path to the downloaded
        tarball, the path to the downloaded specfile (in the case of new-style
        buildcache), and whether or not the tarball is already verified.

    .. code-block:: JSON

       {
           "tarball_path": "path-to-locally-saved-tarfile",
           "specfile_path": "none-or-path-to-locally-saved-specfile",
           "signature_verified": "true-if-binary-pkg-was-already-verified"
       }
    """
    configured_mirrors: Iterable[spack.mirror.Mirror] = spack.mirror.MirrorCollection(
        binary=True
    ).values()
    if not configured_mirrors:
        tty.die("Please add a spack mirror to allow download of pre-compiled packages.")

    tarball = tarball_path_name(spec, ".spack")
    specfile_prefix = tarball_name(spec, ".spec")

    # Note on try_first and try_next:
    # mirrors_for_spec mostly likely came from spack caching remote
    # mirror indices locally and adding their specs to a local data
    # structure supporting quick lookup of concrete specs.  Those
    # mirrors are likely a subset of all configured mirrors, and
    # we'll probably find what we need in one of them.  But we'll
    # look in all configured mirrors if needed, as maybe the spec
    # we need was in an un-indexed mirror.  No need to check any
    # mirror for the spec twice though.
    try_first = [i["mirror_url"] for i in mirrors_for_spec] if mirrors_for_spec else []
    try_next = [i.fetch_url for i in configured_mirrors if i.fetch_url not in try_first]
    mirror_urls = try_first + try_next

    # TODO: turn `mirrors_for_spec` into a list of Mirror instances, instead of doing that here.
    def fetch_url_to_mirror(url):
        for mirror in configured_mirrors:
            if mirror.fetch_url == url:
                return mirror
        return spack.mirror.Mirror(url)

    mirrors = [fetch_url_to_mirror(url) for url in mirror_urls]

    tried_to_verify_sigs = []

    # Assumes we care more about finding a spec file by preferred ext
    # than by mirrory priority.  This can be made less complicated as
    # we remove support for deprecated spec formats and buildcache layouts.
    for try_signed in (True, False):
        for mirror in mirrors:
            # Override mirror's default if
            currently_unsigned = unsigned if unsigned is not None else not mirror.signed

            # If it's an OCI index, do things differently, since we cannot compose URLs.
            fetch_url = mirror.fetch_url

            # TODO: refactor this to some "nice" place.
            if fetch_url.startswith("oci://"):
                ref = spack.oci.image.ImageReference.from_string(
                    fetch_url[len("oci://") :]
                ).with_tag(spack.oci.image.default_tag(spec))

                # Fetch the manifest
                try:
                    response = spack.oci.opener.urlopen(
                        urllib.request.Request(
                            url=ref.manifest_url(),
                            headers={"Accept": ", ".join(spack.oci.oci.manifest_content_type)},
                        )
                    )
                except Exception:
                    continue

                # Download the config = spec.json and the relevant tarball
                try:
                    manifest = json.loads(response.read())
                    spec_digest = spack.oci.image.Digest.from_string(manifest["config"]["digest"])
                    tarball_digest = spack.oci.image.Digest.from_string(
                        manifest["layers"][-1]["digest"]
                    )
                except Exception:
                    continue

                with spack.oci.oci.make_stage(
                    ref.blob_url(spec_digest), spec_digest, keep=True
                ) as local_specfile_stage:
                    try:
                        local_specfile_stage.fetch()
                        local_specfile_stage.check()
                        try:
                            _get_valid_spec_file(
                                local_specfile_stage.save_filename,
                                CURRENT_BUILD_CACHE_LAYOUT_VERSION,
                            )
                        except InvalidMetadataFile as e:
                            tty.warn(
                                f"Ignoring binary package for {spec.name}/{spec.dag_hash()[:7]} "
                                f"from {fetch_url} due to invalid metadata file: {e}"
                            )
                            local_specfile_stage.destroy()
                            continue
                    except Exception:
                        continue
                    local_specfile_stage.cache_local()

                with spack.oci.oci.make_stage(
                    ref.blob_url(tarball_digest), tarball_digest, keep=True
                ) as tarball_stage:
                    try:
                        tarball_stage.fetch()
                        tarball_stage.check()
                    except Exception:
                        continue
                    tarball_stage.cache_local()

                return {
                    "tarball_stage": tarball_stage,
                    "specfile_stage": local_specfile_stage,
                    "signature_verified": False,
                    "signature_required": not currently_unsigned,
                }

            else:
                ext = "json.sig" if try_signed else "json"
                specfile_path = url_util.join(
                    fetch_url, BUILD_CACHE_RELATIVE_PATH, specfile_prefix
                )
                specfile_url = f"{specfile_path}.{ext}"
                spackfile_url = url_util.join(fetch_url, BUILD_CACHE_RELATIVE_PATH, tarball)
                local_specfile_stage = try_fetch(specfile_url)
                if local_specfile_stage:
                    local_specfile_path = local_specfile_stage.save_filename
                    signature_verified = False

                    try:
                        _get_valid_spec_file(
                            local_specfile_path, CURRENT_BUILD_CACHE_LAYOUT_VERSION
                        )
                    except InvalidMetadataFile as e:
                        tty.warn(
                            f"Ignoring binary package for {spec.name}/{spec.dag_hash()[:7]} "
                            f"from {fetch_url} due to invalid metadata file: {e}"
                        )
                        local_specfile_stage.destroy()
                        continue

                    if try_signed and not currently_unsigned:
                        # If we found a signed specfile at the root, try to verify
                        # the signature immediately.  We will not download the
                        # tarball if we could not verify the signature.
                        tried_to_verify_sigs.append(specfile_url)
                        signature_verified = try_verify(local_specfile_path)
                        if not signature_verified:
                            tty.warn(f"Failed to verify: {specfile_url}")

                    if currently_unsigned or signature_verified or not try_signed:
                        # We will download the tarball in one of three cases:
                        #     1. user asked for --no-check-signature
                        #     2. user didn't ask for --no-check-signature, but we
                        #     found a spec.json.sig and verified the signature already
                        #     3. neither of the first two cases are true, but this file
                        #     is *not* a signed json (not a spec.json.sig file).  That
                        #     means we already looked at all the mirrors and either didn't
                        #     find any .sig files or couldn't verify any of them.  But it
                        #     is still possible to find an old style binary package where
                        #     the signature is a detached .asc file in the outer archive
                        #     of the tarball, and in that case, the only way to know is to
                        #     download the tarball.  This is a deprecated use case, so if
                        #     something goes wrong during the extraction process (can't
                        #     verify signature, checksum doesn't match) we will fail at
                        #     that point instead of trying to download more tarballs from
                        #     the remaining mirrors, looking for one we can use.
                        tarball_stage = try_fetch(spackfile_url)
                        if tarball_stage:
                            return {
                                "tarball_stage": tarball_stage,
                                "specfile_stage": local_specfile_stage,
                                "signature_verified": signature_verified,
                                "signature_required": not currently_unsigned,
                            }

                    local_specfile_stage.destroy()

    # Falling through the nested loops meeans we exhaustively searched
    # for all known kinds of spec files on all mirrors and did not find
    # an acceptable one for which we could download a tarball.

    if tried_to_verify_sigs:
        raise NoVerifyException(
            (
                "Spack found new style signed binary packages, "
                "but was unable to verify any of them.  Please "
                "obtain and trust the correct public key.  If "
                "these are public spack binaries, please see the "
                "spack docs for locations where keys can be found."
            )
        )

    return None


def dedupe_hardlinks_if_necessary(root, buildinfo):
    """Updates a buildinfo dict for old archives that did
    not dedupe hardlinks. De-duping hardlinks is necessary
    when relocating files in parallel and in-place. This
    means we must preserve inodes when relocating."""

    # New archives don't need this.
    if buildinfo.get("hardlinks_deduped", False):
        return

    # Clearly we can assume that an inode is either in the
    # textfile or binary group, but let's just stick to
    # a single set of visited nodes.
    visited = set()

    # Note: we do *not* dedupe hardlinked symlinks, since
    # it seems difficult or even impossible to relink
    # symlinks while preserving inode.
    for key in ("relocate_textfiles", "relocate_binaries"):
        if key not in buildinfo:
            continue
        new_list = []
        for rel_path in buildinfo[key]:
            stat_result = os.lstat(os.path.join(root, rel_path))
            identifier = (stat_result.st_dev, stat_result.st_ino)
            if stat_result.st_nlink > 1:
                if identifier in visited:
                    continue
                visited.add(identifier)
            new_list.append(rel_path)
        buildinfo[key] = new_list


def relocate_package(spec):
    """
    Relocate the given package
    """
    workdir = str(spec.prefix)
    buildinfo = read_buildinfo_file(workdir)
    new_layout_root = str(spack.store.STORE.layout.root)
    new_prefix = str(spec.prefix)
    new_rel_prefix = str(os.path.relpath(new_prefix, new_layout_root))
    new_spack_prefix = str(spack.paths.prefix)

    old_sbang_install_path = None
    if "sbang_install_path" in buildinfo:
        old_sbang_install_path = str(buildinfo["sbang_install_path"])
    old_layout_root = str(buildinfo["buildpath"])
    old_spack_prefix = str(buildinfo.get("spackprefix"))
    old_rel_prefix = buildinfo.get("relative_prefix")
    old_prefix = os.path.join(old_layout_root, old_rel_prefix)
    rel = buildinfo.get("relative_rpaths", False)

    # In the past prefix_to_hash was the default and externals were not dropped, so prefixes
    # were not unique.
    if "hash_to_prefix" in buildinfo:
        hash_to_old_prefix = buildinfo["hash_to_prefix"]
    elif "prefix_to_hash" in buildinfo:
        hash_to_old_prefix = dict((v, k) for (k, v) in buildinfo["prefix_to_hash"].items())
    else:
        hash_to_old_prefix = dict()

    if old_rel_prefix != new_rel_prefix and not hash_to_old_prefix:
        msg = "Package tarball was created from an install "
        msg += "prefix with a different directory layout and an older "
        msg += "buildcache create implementation. It cannot be relocated."
        raise NewLayoutException(msg)

    # Spurious replacements (e.g. sbang) will cause issues with binaries
    # For example, the new sbang can be longer than the old one.
    # Hence 2 dictionaries are maintained here.
    prefix_to_prefix_text = collections.OrderedDict()
    prefix_to_prefix_bin = collections.OrderedDict()

    if old_sbang_install_path:
        install_path = spack.hooks.sbang.sbang_install_path()
        prefix_to_prefix_text[old_sbang_install_path] = install_path

    # First match specific prefix paths. Possibly the *local* install prefix
    # of some dependency is in an upstream, so we cannot assume the original
    # spack store root can be mapped uniformly to the new spack store root.
    for dag_hash, new_dep_prefix in hashes_to_prefixes(spec).items():
        if dag_hash in hash_to_old_prefix:
            old_dep_prefix = hash_to_old_prefix[dag_hash]
            prefix_to_prefix_bin[old_dep_prefix] = new_dep_prefix
            prefix_to_prefix_text[old_dep_prefix] = new_dep_prefix

    # Only then add the generic fallback of install prefix -> install prefix.
    prefix_to_prefix_text[old_prefix] = new_prefix
    prefix_to_prefix_bin[old_prefix] = new_prefix
    prefix_to_prefix_text[old_layout_root] = new_layout_root
    prefix_to_prefix_bin[old_layout_root] = new_layout_root

    # This is vestigial code for the *old* location of sbang. Previously,
    # sbang was a bash script, and it lived in the spack prefix. It is
    # now a POSIX script that lives in the install prefix. Old packages
    # will have the old sbang location in their shebangs.
    orig_sbang = "#!/bin/bash {0}/bin/sbang".format(old_spack_prefix)
    new_sbang = spack.hooks.sbang.sbang_shebang_line()
    prefix_to_prefix_text[orig_sbang] = new_sbang

    tty.debug("Relocating package from", "%s to %s." % (old_layout_root, new_layout_root))

    # Old archives maybe have hardlinks repeated.
    dedupe_hardlinks_if_necessary(workdir, buildinfo)

    def is_backup_file(file):
        return file.endswith("~")

    # Text files containing the prefix text
    text_names = list()
    for filename in buildinfo["relocate_textfiles"]:
        text_name = os.path.join(workdir, filename)
        # Don't add backup files generated by filter_file during install step.
        if not is_backup_file(text_name):
            text_names.append(text_name)

    # If we are not installing back to the same install tree do the relocation
    if old_prefix != new_prefix:
        files_to_relocate = [
            os.path.join(workdir, filename) for filename in buildinfo.get("relocate_binaries")
        ]
        # If the buildcache was not created with relativized rpaths
        # do the relocation of path in binaries
        platform = spack.platforms.by_name(spec.platform)
        if "macho" in platform.binary_formats:
            relocate.relocate_macho_binaries(
                files_to_relocate,
                old_layout_root,
                new_layout_root,
                prefix_to_prefix_bin,
                rel,
                old_prefix,
                new_prefix,
            )
        elif "elf" in platform.binary_formats and not rel:
            # The new ELF dynamic section relocation logic only handles absolute to
            # absolute relocation.
            relocate.new_relocate_elf_binaries(files_to_relocate, prefix_to_prefix_bin)
        elif "elf" in platform.binary_formats and rel:
            relocate.relocate_elf_binaries(
                files_to_relocate,
                old_layout_root,
                new_layout_root,
                prefix_to_prefix_bin,
                rel,
                old_prefix,
                new_prefix,
            )

        # Relocate links to the new install prefix
        links = [os.path.join(workdir, f) for f in buildinfo.get("relocate_links", [])]
        relocate.relocate_links(links, prefix_to_prefix_bin)

        # For all buildcaches
        # relocate the install prefixes in text files including dependencies
        relocate.relocate_text(text_names, prefix_to_prefix_text)

        # relocate the install prefixes in binary files including dependencies
        changed_files = relocate.relocate_text_bin(files_to_relocate, prefix_to_prefix_bin)

        # Add ad-hoc signatures to patched macho files when on macOS.
        if "macho" in platform.binary_formats and sys.platform == "darwin":
            codesign = which("codesign")
            if not codesign:
                return
            for binary in changed_files:
                codesign("-fs-", binary)

    # If we are installing back to the same location
    # relocate the sbang location if the spack directory changed
    else:
        if old_spack_prefix != new_spack_prefix:
            relocate.relocate_text(text_names, prefix_to_prefix_text)


def _extract_inner_tarball(spec, filename, extract_to, signature_required: bool, remote_checksum):
    stagepath = os.path.dirname(filename)
    spackfile_name = tarball_name(spec, ".spack")
    spackfile_path = os.path.join(stagepath, spackfile_name)
    tarfile_name = tarball_name(spec, ".tar.gz")
    tarfile_path = os.path.join(extract_to, tarfile_name)
    json_name = tarball_name(spec, ".spec.json")
    json_path = os.path.join(extract_to, json_name)
    with closing(tarfile.open(spackfile_path, "r")) as tar:
        tar.extractall(extract_to)
    # some buildcache tarfiles use bzip2 compression
    if not os.path.exists(tarfile_path):
        tarfile_name = tarball_name(spec, ".tar.bz2")
        tarfile_path = os.path.join(extract_to, tarfile_name)

    if os.path.exists(json_path):
        specfile_path = json_path
    else:
        raise ValueError("Cannot find spec file for {0}.".format(extract_to))

    if signature_required:
        if os.path.exists("%s.asc" % specfile_path):
            suppress = config.get("config:suppress_gpg_warnings", False)
            try:
                spack.util.gpg.verify("%s.asc" % specfile_path, specfile_path, suppress)
            except Exception:
                raise NoVerifyException(
                    "Spack was unable to verify package "
                    "signature, please obtain and trust the "
                    "correct public key."
                )
        else:
            raise UnsignedPackageException(
                "To install unsigned packages, use the --no-check-signature option."
            )

    # compute the sha256 checksum of the tarball
    local_checksum = spack.util.crypto.checksum(hashlib.sha256, tarfile_path)
    expected = remote_checksum["hash"]

    # if the checksums don't match don't install
    if local_checksum != expected:
        size, contents = fsys.filesummary(tarfile_path)
        raise NoChecksumException(tarfile_path, size, contents, "sha256", expected, local_checksum)

    return tarfile_path


def _tar_strip_component(tar: tarfile.TarFile, prefix: str):
    """Yield all members of tarfile that start with given prefix, and strip that prefix (including
    symlinks)"""
    # Including trailing /, otherwise we end up with absolute paths.
    regex = re.compile(re.escape(prefix) + "/*")

    # Only yield members in the package prefix.
    # Note: when a tarfile is created, relative in-prefix symlinks are
    # expanded to matching member names of tarfile entries. So, we have
    # to ensure that those are updated too.
    # Absolute symlinks are copied verbatim -- relocation should take care of
    # them.
    for m in tar.getmembers():
        result = regex.match(m.name)
        if not result:
            continue
        m.name = m.name[result.end() :]
        if m.linkname:
            result = regex.match(m.linkname)
            if result:
                m.linkname = m.linkname[result.end() :]
        yield m


def extract_tarball(spec, download_result, force=False, timer=timer.NULL_TIMER):
    """
    extract binary tarball for given package into install area
    """
    timer.start("extract")
    if os.path.exists(spec.prefix):
        if force:
            shutil.rmtree(spec.prefix)
        else:
            raise NoOverwriteException(str(spec.prefix))

    # Create the install prefix
    fsys.mkdirp(
        spec.prefix,
        mode=get_package_dir_permissions(spec),
        group=get_package_group(spec),
        default_perms="parents",
    )

    specfile_path = download_result["specfile_stage"].save_filename
    spec_dict, layout_version = _get_valid_spec_file(
        specfile_path, CURRENT_BUILD_CACHE_LAYOUT_VERSION
    )
    bchecksum = spec_dict["binary_cache_checksum"]

    filename = download_result["tarball_stage"].save_filename
    signature_verified: bool = download_result["signature_verified"]
    signature_required: bool = download_result["signature_required"]
    tmpdir = None

    if layout_version == 0:
        # Handle the older buildcache layout where the .spack file
        # contains a spec json, maybe an .asc file (signature),
        # and another tarball containing the actual install tree.
        tmpdir = tempfile.mkdtemp()
        try:
            tarfile_path = _extract_inner_tarball(
                spec, filename, tmpdir, signature_required, bchecksum
            )
        except Exception as e:
            _delete_staged_downloads(download_result)
            shutil.rmtree(tmpdir)
            raise e
    elif 1 <= layout_version <= 2:
        # Newer buildcache layout: the .spack file contains just
        # in the install tree, the signature, if it exists, is
        # wrapped around the spec.json at the root.  If sig verify
        # was required, it was already done before downloading
        # the tarball.
        tarfile_path = filename

        if signature_required and not signature_verified:
            raise UnsignedPackageException(
                "To install unsigned packages, use the --no-check-signature option, "
                "or configure the mirror with signed: false."
            )

        # compute the sha256 checksum of the tarball
        local_checksum = spack.util.crypto.checksum(hashlib.sha256, tarfile_path)
        expected = bchecksum["hash"]

        # if the checksums don't match don't install
        if local_checksum != expected:
            size, contents = fsys.filesummary(tarfile_path)
            _delete_staged_downloads(download_result)
            raise NoChecksumException(
                tarfile_path, size, contents, "sha256", expected, local_checksum
            )
    try:
        with closing(tarfile.open(tarfile_path, "r")) as tar:
            # Remove install prefix from tarfil to extract directly into spec.prefix
            tar.extractall(
                path=spec.prefix,
                members=_tar_strip_component(tar, prefix=_ensure_common_prefix(tar)),
            )
    except Exception:
        shutil.rmtree(spec.prefix, ignore_errors=True)
        _delete_staged_downloads(download_result)
        raise

    os.remove(tarfile_path)
    os.remove(specfile_path)
    timer.stop("extract")

    timer.start("relocate")
    try:
        relocate_package(spec)
    except Exception as e:
        shutil.rmtree(spec.prefix, ignore_errors=True)
        raise e
    else:
        manifest_file = os.path.join(
            spec.prefix,
            spack.store.STORE.layout.metadata_dir,
            spack.store.STORE.layout.manifest_file_name,
        )
        if not os.path.exists(manifest_file):
            spec_id = spec.format("{name}/{hash:7}")
            tty.warn("No manifest file in tarball for spec %s" % spec_id)
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)
        if os.path.exists(filename):
            os.remove(filename)
        _delete_staged_downloads(download_result)
    timer.stop("relocate")


def _ensure_common_prefix(tar: tarfile.TarFile) -> str:
    # Find the lowest `binary_distribution` file (hard-coded forward slash is on purpose).
    binary_distribution = min(
        (
            e.name
            for e in tar.getmembers()
            if e.isfile() and e.name.endswith(".spack/binary_distribution")
        ),
        key=len,
        default=None,
    )

    if binary_distribution is None:
        raise ValueError("Tarball is not a Spack package, missing binary_distribution file")

    pkg_path = pathlib.PurePosixPath(binary_distribution).parent.parent

    # Even the most ancient Spack version has required to list the dir of the package itself, so
    # guard against broken tarballs where `path.parent.parent` is empty.
    if pkg_path == pathlib.PurePosixPath():
        raise ValueError("Invalid tarball, missing package prefix dir")

    pkg_prefix = str(pkg_path)

    # Ensure all tar entries are in the pkg_prefix dir, and if they're not, they should be parent
    # dirs of it.
    has_prefix = False
    for member in tar.getmembers():
        stripped = member.name.rstrip("/")
        if not (
            stripped.startswith(pkg_prefix) or member.isdir() and pkg_prefix.startswith(stripped)
        ):
            raise ValueError(f"Tarball contains file {stripped} outside of prefix {pkg_prefix}")
        if member.isdir() and stripped == pkg_prefix:
            has_prefix = True

    # This is technically not required, but let's be defensive about the existence of the package
    # prefix dir.
    if not has_prefix:
        raise ValueError(f"Tarball does not contain a common prefix {pkg_prefix}")

    return pkg_prefix


def install_root_node(spec, unsigned=False, force=False, sha256=None):
    """Install the root node of a concrete spec from a buildcache.

    Checking the sha256 sum of a node before installation is usually needed only
    for software installed during Spack's bootstrapping (since we might not have
    a proper signature verification mechanism available).

    Args:
        spec: spec to be installed (note that only the root node will be installed)
        unsigned (bool): if True allows installing unsigned binaries
        force (bool): force installation if the spec is already present in the
            local store
        sha256 (str): optional sha256 of the binary package, to be checked
            before installation
    """
    # Early termination
    if spec.external or spec.virtual:
        warnings.warn("Skipping external or virtual package {0}".format(spec.format()))
        return
    elif spec.concrete and spec.installed and not force:
        warnings.warn("Package for spec {0} already installed.".format(spec.format()))
        return

    download_result = download_tarball(spec, unsigned)
    if not download_result:
        msg = 'download of binary cache file for spec "{0}" failed'
        raise RuntimeError(msg.format(spec.format()))

    if sha256:
        checker = spack.util.crypto.Checker(sha256)
        msg = 'cannot verify checksum for "{0}" [expected={1}]'
        tarball_path = download_result["tarball_stage"].save_filename
        msg = msg.format(tarball_path, sha256)
        if not checker.check(tarball_path):
            size, contents = fsys.filesummary(tarball_path)
            _delete_staged_downloads(download_result)
            raise NoChecksumException(
                tarball_path, size, contents, checker.hash_name, sha256, checker.sum
            )
        tty.debug("Verified SHA256 checksum of the build cache")

    # don't print long padded paths while extracting/relocating binaries
    with spack.util.path.filter_padding():
        tty.msg('Installing "{0}" from a buildcache'.format(spec.format()))
        extract_tarball(spec, download_result, force)
        spack.hooks.post_install(spec, False)
        spack.store.STORE.db.add(spec, spack.store.STORE.layout)


def install_single_spec(spec, unsigned=False, force=False):
    """Install a single concrete spec from a buildcache.

    Args:
        spec (spack.spec.Spec): spec to be installed
        unsigned (bool): if True allows installing unsigned binaries
        force (bool): force installation if the spec is already present in the
            local store
    """
    for node in spec.traverse(root=True, order="post", deptype=("link", "run")):
        install_root_node(node, unsigned=unsigned, force=force)


def try_direct_fetch(spec, mirrors=None):
    """
    Try to find the spec directly on the configured mirrors
    """
    specfile_name = tarball_name(spec, ".spec.json")
    signed_specfile_name = tarball_name(spec, ".spec.json.sig")
    specfile_is_signed = False
    found_specs = []

    binary_mirrors = spack.mirror.MirrorCollection(mirrors=mirrors, binary=True).values()

    for mirror in binary_mirrors:
        buildcache_fetch_url_json = url_util.join(
            mirror.fetch_url, BUILD_CACHE_RELATIVE_PATH, specfile_name
        )
        buildcache_fetch_url_signed_json = url_util.join(
            mirror.fetch_url, BUILD_CACHE_RELATIVE_PATH, signed_specfile_name
        )
        try:
            _, _, fs = web_util.read_from_url(buildcache_fetch_url_signed_json)
            specfile_is_signed = True
        except (URLError, web_util.SpackWebError, HTTPError) as url_err:
            try:
                _, _, fs = web_util.read_from_url(buildcache_fetch_url_json)
            except (URLError, web_util.SpackWebError, HTTPError) as url_err_x:
                tty.debug(
                    "Did not find {0} on {1}".format(
                        specfile_name, buildcache_fetch_url_signed_json
                    ),
                    url_err,
                    level=2,
                )
                tty.debug(
                    "Did not find {0} on {1}".format(specfile_name, buildcache_fetch_url_json),
                    url_err_x,
                    level=2,
                )
                continue
        specfile_contents = codecs.getreader("utf-8")(fs).read()

        # read the spec from the build cache file. All specs in build caches
        # are concrete (as they are built) so we need to mark this spec
        # concrete on read-in.
        if specfile_is_signed:
            specfile_json = Spec.extract_json_from_clearsig(specfile_contents)
            fetched_spec = Spec.from_dict(specfile_json)
        else:
            fetched_spec = Spec.from_json(specfile_contents)
        fetched_spec._mark_concrete()

        found_specs.append({"mirror_url": mirror.fetch_url, "spec": fetched_spec})

    return found_specs


def get_mirrors_for_spec(spec=None, mirrors_to_check=None, index_only=False):
    """
    Check if concrete spec exists on mirrors and return a list
    indicating the mirrors on which it can be found

    Args:
        spec (spack.spec.Spec): The spec to look for in binary mirrors
        mirrors_to_check (dict): Optionally override the configured mirrors
            with the mirrors in this dictionary.
        index_only (bool): When ``index_only`` is set to ``True``, only the local
            cache is checked, no requests are made.

    Return:
        A list of objects, each containing a ``mirror_url`` and ``spec`` key
            indicating all mirrors where the spec can be found.
    """
    if spec is None:
        return []

    if not spack.mirror.MirrorCollection(mirrors=mirrors_to_check, binary=True):
        tty.debug("No Spack mirrors are currently configured")
        return {}

    results = BINARY_INDEX.find_built_spec(spec, mirrors_to_check=mirrors_to_check)

    # The index may be out-of-date. If we aren't only considering indices, try
    # to fetch directly since we know where the file should be.
    if not results and not index_only:
        results = try_direct_fetch(spec, mirrors=mirrors_to_check)
        # We found a spec by the direct fetch approach, we might as well
        # add it to our mapping.
        if results:
            BINARY_INDEX.update_spec(spec, results)

    return results


def update_cache_and_get_specs():
    """
    Get all concrete specs for build caches available on configured mirrors.
    Initialization of internal cache data structures is done as lazily as
    possible, so this method will also attempt to initialize and update the
    local index cache (essentially a no-op if it has been done already and
    nothing has changed on the configured mirrors.)

    Throws:
        FetchCacheError
    """
    BINARY_INDEX.update()
    return BINARY_INDEX.get_all_built_specs()


def clear_spec_cache():
    BINARY_INDEX.clear()


def get_keys(install=False, trust=False, force=False, mirrors=None):
    """Get pgp public keys available on mirror with suffix .pub"""
    mirror_collection = mirrors or spack.mirror.MirrorCollection(binary=True)

    if not mirror_collection:
        tty.die("Please add a spack mirror to allow " + "download of build caches.")

    for mirror in mirror_collection.values():
        fetch_url = mirror.fetch_url
        keys_url = url_util.join(
            fetch_url, BUILD_CACHE_RELATIVE_PATH, BUILD_CACHE_KEYS_RELATIVE_PATH
        )
        keys_index = url_util.join(keys_url, "index.json")

        tty.debug("Finding public keys in {0}".format(url_util.format(fetch_url)))

        try:
            _, _, json_file = web_util.read_from_url(keys_index)
            json_index = sjson.load(codecs.getreader("utf-8")(json_file))
        except (URLError, web_util.SpackWebError) as url_err:
            if web_util.url_exists(keys_index):
                err_msg = [
                    "Unable to find public keys in {0},",
                    " caught exception attempting to read from {1}.",
                ]

                tty.error(
                    "".join(err_msg).format(
                        url_util.format(fetch_url), url_util.format(keys_index)
                    )
                )

                tty.debug(url_err)

            continue

        for fingerprint, key_attributes in json_index["keys"].items():
            link = os.path.join(keys_url, fingerprint + ".pub")

            with Stage(link, name="build_cache", keep=True) as stage:
                if os.path.exists(stage.save_filename) and force:
                    os.remove(stage.save_filename)
                if not os.path.exists(stage.save_filename):
                    try:
                        stage.fetch()
                    except spack.error.FetchError:
                        continue

            tty.debug("Found key {0}".format(fingerprint))
            if install:
                if trust:
                    spack.util.gpg.trust(stage.save_filename)
                    tty.debug("Added this key to trusted keys.")
                else:
                    tty.debug(
                        "Will not add this key to trusted keys."
                        "Use -t to install all downloaded keys"
                    )


def push_keys(*mirrors, **kwargs):
    """
    Upload pgp public keys to the given mirrors
    """
    keys = kwargs.get("keys")
    regenerate_index = kwargs.get("regenerate_index", False)
    tmpdir = kwargs.get("tmpdir")
    remove_tmpdir = False

    keys = spack.util.gpg.public_keys(*(keys or []))

    try:
        for mirror in mirrors:
            push_url = getattr(mirror, "push_url", mirror)
            keys_url = url_util.join(
                push_url, BUILD_CACHE_RELATIVE_PATH, BUILD_CACHE_KEYS_RELATIVE_PATH
            )
            keys_local = url_util.local_file_path(keys_url)

            verb = "Writing" if keys_local else "Uploading"
            tty.debug("{0} public keys to {1}".format(verb, url_util.format(push_url)))

            if keys_local:  # mirror is local, don't bother with the tmpdir
                prefix = keys_local
                mkdirp(keys_local)
            else:
                # A tmp dir is created for the first mirror that is non-local.
                # On the off-hand chance that all the mirrors are local, then
                # we can avoid the need to create a tmp dir.
                if tmpdir is None:
                    tmpdir = tempfile.mkdtemp()
                    remove_tmpdir = True
                prefix = tmpdir

            for fingerprint in keys:
                tty.debug("    " + fingerprint)
                filename = fingerprint + ".pub"

                export_target = os.path.join(prefix, filename)

                # Export public keys (private is set to False)
                spack.util.gpg.export_keys(export_target, [fingerprint])

                # If mirror is local, the above export writes directly to the
                # mirror (export_target points directly to the mirror).
                #
                # If not, then export_target is a tmpfile that needs to be
                # uploaded to the mirror.
                if not keys_local:
                    spack.util.web.push_to_url(
                        export_target, url_util.join(keys_url, filename), keep_original=False
                    )

            if regenerate_index:
                if keys_local:
                    generate_key_index(keys_url)
                else:
                    generate_key_index(keys_url, tmpdir)
    finally:
        if remove_tmpdir:
            shutil.rmtree(tmpdir)


def needs_rebuild(spec, mirror_url):
    if not spec.concrete:
        raise ValueError("spec must be concrete to check against mirror")

    pkg_name = spec.name
    pkg_version = spec.version
    pkg_hash = spec.dag_hash()

    tty.debug("Checking {0}-{1}, dag_hash = {2}".format(pkg_name, pkg_version, pkg_hash))
    tty.debug(spec.tree())

    # Try to retrieve the specfile directly, based on the known
    # format of the name, in order to determine if the package
    # needs to be rebuilt.
    cache_prefix = build_cache_prefix(mirror_url)
    specfile_name = tarball_name(spec, ".spec.json")
    specfile_path = os.path.join(cache_prefix, specfile_name)

    # Only check for the presence of the json version of the spec.  If the
    # mirror only has the json version, or doesn't have the spec at all, we
    # need to rebuild.
    return not web_util.url_exists(specfile_path)


def check_specs_against_mirrors(mirrors, specs, output_file=None):
    """Check all the given specs against buildcaches on the given mirrors and
    determine if any of the specs need to be rebuilt.  Specs need to be rebuilt
    when their hash doesn't exist in the mirror.

    Arguments:
        mirrors (dict): Mirrors to check against
        specs (typing.Iterable): Specs to check against mirrors
        output_file (str): Path to output file to be written.  If provided,
            mirrors with missing or out-of-date specs will be formatted as a
            JSON object and written to this file.

    Returns: 1 if any spec was out-of-date on any mirror, 0 otherwise.

    """
    rebuilds = {}
    for mirror in spack.mirror.MirrorCollection(mirrors, binary=True).values():
        tty.debug("Checking for built specs at {0}".format(mirror.fetch_url))

        rebuild_list = []

        for spec in specs:
            if needs_rebuild(spec, mirror.fetch_url):
                rebuild_list.append({"short_spec": spec.short_spec, "hash": spec.dag_hash()})

        if rebuild_list:
            rebuilds[mirror.fetch_url] = {
                "mirrorName": mirror.name,
                "mirrorUrl": mirror.fetch_url,
                "rebuildSpecs": rebuild_list,
            }

    if output_file:
        with open(output_file, "w") as outf:
            outf.write(json.dumps(rebuilds))

    return 1 if rebuilds else 0


def _download_buildcache_entry(mirror_root, descriptions):
    for description in descriptions:
        path = description["path"]
        mkdirp(path)
        fail_if_missing = description["required"]
        for url in description["url"]:
            description_url = os.path.join(mirror_root, url)
            stage = Stage(description_url, name="build_cache", path=path, keep=True)
            try:
                stage.fetch()
                break
            except spack.error.FetchError as e:
                tty.debug(e)
        else:
            if fail_if_missing:
                tty.error("Failed to download required url {0}".format(description_url))
                return False
    return True


def download_buildcache_entry(file_descriptions, mirror_url=None):
    if not mirror_url and not spack.mirror.MirrorCollection(binary=True):
        tty.die(
            "Please provide or add a spack mirror to allow " + "download of buildcache entries."
        )

    if mirror_url:
        mirror_root = os.path.join(mirror_url, BUILD_CACHE_RELATIVE_PATH)
        return _download_buildcache_entry(mirror_root, file_descriptions)

    for mirror in spack.mirror.MirrorCollection(binary=True).values():
        mirror_root = os.path.join(mirror.fetch_url, BUILD_CACHE_RELATIVE_PATH)

        if _download_buildcache_entry(mirror_root, file_descriptions):
            return True
        else:
            continue

    return False


def download_single_spec(concrete_spec, destination, mirror_url=None):
    """Download the buildcache files for a single concrete spec.

    Args:
        concrete_spec: concrete spec to be downloaded
        destination (str): path where to put the downloaded buildcache
        mirror_url (str): url of the mirror from which to download
    """
    tarfile_name = tarball_name(concrete_spec, ".spack")
    tarball_dir_name = tarball_directory_name(concrete_spec)
    tarball_path_name = os.path.join(tarball_dir_name, tarfile_name)
    local_tarball_path = os.path.join(destination, tarball_dir_name)

    files_to_fetch = [
        {"url": [tarball_path_name], "path": local_tarball_path, "required": True},
        {
            "url": [
                tarball_name(concrete_spec, ".spec.json.sig"),
                tarball_name(concrete_spec, ".spec.json"),
            ],
            "path": destination,
            "required": True,
        },
    ]

    return download_buildcache_entry(files_to_fetch, mirror_url)


class BinaryCacheQuery:
    """Callable object to query if a spec is in a binary cache"""

    def __init__(self, all_architectures):
        """
        Args:
            all_architectures (bool): if True consider all the spec for querying,
                otherwise restrict to the current default architecture
        """
        self.all_architectures = all_architectures

        specs = update_cache_and_get_specs()

        if not self.all_architectures:
            arch = spack.spec.Spec.default_arch()
            specs = [s for s in specs if s.satisfies(arch)]

        self.possible_specs = specs

    def __call__(self, spec: Spec, **kwargs):
        """
        Args:
            spec: The spec being searched for
        """
        return [s for s in self.possible_specs if s.satisfies(spec)]


class FetchIndexError(Exception):
    def __str__(self):
        if len(self.args) == 1:
            return str(self.args[0])
        else:
            return "{}, due to: {}".format(self.args[0], self.args[1])


class BuildcacheIndexError(spack.error.SpackError):
    """Raised when a buildcache cannot be read for any reason"""


FetchIndexResult = collections.namedtuple("FetchIndexResult", "etag hash data fresh")


class DefaultIndexFetcher:
    """Fetcher for index.json, using separate index.json.hash as cache invalidation strategy"""

    def __init__(self, url, local_hash, urlopen=web_util.urlopen):
        self.url = url
        self.local_hash = local_hash
        self.urlopen = urlopen
        self.headers = {"User-Agent": web_util.SPACK_USER_AGENT}

    def get_remote_hash(self):
        # Failure to fetch index.json.hash is not fatal
        url_index_hash = url_util.join(self.url, BUILD_CACHE_RELATIVE_PATH, "index.json.hash")
        try:
            response = self.urlopen(urllib.request.Request(url_index_hash, headers=self.headers))
        except urllib.error.URLError:
            return None

        # Validate the hash
        remote_hash = response.read(64)
        if not re.match(rb"[a-f\d]{64}$", remote_hash):
            return None
        return remote_hash.decode("utf-8")

    def conditional_fetch(self) -> FetchIndexResult:
        # Do an intermediate fetch for the hash
        # and a conditional fetch for the contents

        # Early exit if our cache is up to date.
        if self.local_hash and self.local_hash == self.get_remote_hash():
            return FetchIndexResult(etag=None, hash=None, data=None, fresh=True)

        # Otherwise, download index.json
        url_index = url_util.join(self.url, BUILD_CACHE_RELATIVE_PATH, "index.json")

        try:
            response = self.urlopen(urllib.request.Request(url_index, headers=self.headers))
        except urllib.error.URLError as e:
            raise FetchIndexError("Could not fetch index from {}".format(url_index), e) from e

        try:
            result = codecs.getreader("utf-8")(response).read()
        except ValueError as e:
            raise FetchIndexError("Remote index {} is invalid".format(url_index), e) from e

        computed_hash = compute_hash(result)

        # We don't handle computed_hash != remote_hash here, which can happen
        # when remote index.json and index.json.hash are out of sync, or if
        # the hash algorithm changed.
        # The most likely scenario is that we got index.json got updated
        # while we fetched index.json.hash. Warning about an issue thus feels
        # wrong, as it's more of an issue with race conditions in the cache
        # invalidation strategy.

        # For now we only handle etags on http(s), since 304 error handling
        # in s3:// is not there yet.
        if urllib.parse.urlparse(self.url).scheme not in ("http", "https"):
            etag = None
        else:
            etag = web_util.parse_etag(
                response.headers.get("Etag", None) or response.headers.get("etag", None)
            )

        return FetchIndexResult(etag=etag, hash=computed_hash, data=result, fresh=False)


class EtagIndexFetcher:
    """Fetcher for index.json, using ETags headers as cache invalidation strategy"""

    def __init__(self, url, etag, urlopen=web_util.urlopen):
        self.url = url
        self.etag = etag
        self.urlopen = urlopen

    def conditional_fetch(self) -> FetchIndexResult:
        # Just do a conditional fetch immediately
        url = url_util.join(self.url, BUILD_CACHE_RELATIVE_PATH, "index.json")
        headers = {
            "User-Agent": web_util.SPACK_USER_AGENT,
            "If-None-Match": '"{}"'.format(self.etag),
        }

        try:
            response = self.urlopen(urllib.request.Request(url, headers=headers))
        except urllib.error.HTTPError as e:
            if e.getcode() == 304:
                # Not modified; that means fresh.
                return FetchIndexResult(etag=None, hash=None, data=None, fresh=True)
            raise FetchIndexError("Could not fetch index {}".format(url), e) from e
        except urllib.error.URLError as e:
            raise FetchIndexError("Could not fetch index {}".format(url), e) from e

        try:
            result = codecs.getreader("utf-8")(response).read()
        except ValueError as e:
            raise FetchIndexError("Remote index {} is invalid".format(url), e) from e

        headers = response.headers
        etag_header_value = headers.get("Etag", None) or headers.get("etag", None)
        return FetchIndexResult(
            etag=web_util.parse_etag(etag_header_value),
            hash=compute_hash(result),
            data=result,
            fresh=False,
        )


class OCIIndexFetcher:
    def __init__(self, url: str, local_hash, urlopen=None) -> None:
        self.local_hash = local_hash

        # Remove oci:// prefix
        assert url.startswith("oci://")
        self.ref = spack.oci.image.ImageReference.from_string(url[6:])
        self.urlopen = urlopen or spack.oci.opener.urlopen

    def conditional_fetch(self) -> FetchIndexResult:
        """Download an index from an OCI registry type mirror."""
        url_manifest = self.ref.with_tag(spack.oci.image.default_index_tag).manifest_url()
        try:
            response = self.urlopen(
                urllib.request.Request(
                    url=url_manifest,
                    headers={"Accept": "application/vnd.oci.image.manifest.v1+json"},
                )
            )
        except urllib.error.URLError as e:
            raise FetchIndexError(
                "Could not fetch manifest from {}".format(url_manifest), e
            ) from e

        try:
            manifest = json.loads(response.read())
        except Exception as e:
            raise FetchIndexError("Remote index {} is invalid".format(url_manifest), e) from e

        # Get first blob hash, which should be the index.json
        try:
            index_digest = spack.oci.image.Digest.from_string(manifest["layers"][0]["digest"])
        except Exception as e:
            raise FetchIndexError("Remote index {} is invalid".format(url_manifest), e) from e

        # Fresh?
        if index_digest.digest == self.local_hash:
            return FetchIndexResult(etag=None, hash=None, data=None, fresh=True)

        # Otherwise fetch the blob / index.json
        response = self.urlopen(
            urllib.request.Request(
                url=self.ref.blob_url(index_digest),
                headers={"Accept": "application/vnd.oci.image.layer.v1.tar+gzip"},
            )
        )

        result = codecs.getreader("utf-8")(response).read()

        # Make sure the blob we download has the advertised hash
        if compute_hash(result) != index_digest.digest:
            raise FetchIndexError(f"Remote index {url_manifest} is invalid")

        return FetchIndexResult(etag=None, hash=index_digest.digest, data=result, fresh=False)
