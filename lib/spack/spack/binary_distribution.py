# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import collections
import hashlib
import io
import itertools
import json
import multiprocessing.pool
import os
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
from contextlib import closing, contextmanager
from gzip import GzipFile
from urllib.error import HTTPError, URLError

import ruamel.yaml as yaml

import llnl.util.filesystem as fsys
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, mkdirp, visit_directory_tree

import spack.cmd
import spack.config as config
import spack.database as spack_db
import spack.hooks
import spack.hooks.sbang
import spack.mirror
import spack.platforms
import spack.relocate as relocate
import spack.repo
import spack.store
import spack.traverse as traverse
import spack.util.crypto
import spack.util.file_cache as file_cache
import spack.util.gpg
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.util.web as web_util
from spack.caches import misc_cache_location
from spack.relocate_text import utf8_paths_to_single_binary_regex
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import which

_build_cache_relative_path = "build_cache"
_build_cache_keys_relative_path = "_pgp"


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
        super(FetchCacheError, self).__init__(self.message)


class ListMirrorSpecsError(spack.error.SpackError):
    """Raised when unable to retrieve list of specs from the mirror"""


class BinaryCacheIndex(object):
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

    def __init__(self, cache_root):
        self._index_cache_root = cache_root

        # the key associated with the serialized _local_index_cache
        self._index_contents_key = "contents.json"

        # a FileCache instance storing copies of remote binary cache indices
        self._index_file_cache = None

        # stores a map of mirror URL to index hash and cache key (index path)
        self._local_index_cache = None

        # hashes of remote indices already ingested into the concrete spec
        # cache (_mirrors_for_spec)
        self._specs_already_associated = set()

        # mapping from mirror urls to the time.time() of the last index fetch and a bool indicating
        # whether the fetch succeeded or not.
        self._last_fetch_times = {}

        # _mirrors_for_spec is a dictionary mapping DAG hashes to lists of
        # entries indicating mirrors where that concrete spec can be found.
        # Each entry is a dictionary consisting of:
        #
        #     - the mirror where the spec is, keyed by ``mirror_url``
        #     - the concrete spec itself, keyed by ``spec`` (including the
        #           full hash, since the dag hash may match but we want to
        #           use the updated source if available)
        self._mirrors_for_spec = {}

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
            db_root_dir = os.path.join(tmpdir, "db_root")
            db = spack_db.Database(None, db_dir=db_root_dir, enable_transaction_locking=False)

            self._index_file_cache.init_entry(cache_key)
            cache_path = self._index_file_cache.cache_path(cache_key)
            with self._index_file_cache.read_transaction(cache_key):
                db._read_from_file(cache_path)

            spec_list = db.query_local(installed=False, in_buildcache=True)

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

        mirrors = spack.mirror.MirrorCollection()
        configured_mirror_urls = [m.fetch_url for m in mirrors.values()]
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

        if all_methods_failed:
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
        if not web_util.url_exists(
            url_util.join(mirror_url, _build_cache_relative_path, "index.json")
        ):
            return False

        etag = cache_entry.get("etag", None)
        if etag:
            fetcher = EtagIndexFetcher(mirror_url, etag)
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


def _binary_index():
    """Get the singleton store instance."""
    return BinaryCacheIndex(binary_index_location())


#: Singleton binary_index instance
binary_index = llnl.util.lang.Singleton(_binary_index)


class NoOverwriteException(spack.error.SpackError):
    """
    Raised when a file exists and must be overwritten.
    """

    def __init__(self, file_path):
        super(NoOverwriteException, self).__init__(
            '"{}" exists in buildcache. Use --force flag to overwrite.'.format(file_path)
        )


class NoGpgException(spack.error.SpackError):
    """
    Raised when gpg2 is not in PATH
    """

    def __init__(self, msg):
        super(NoGpgException, self).__init__(msg)


class NoKeyException(spack.error.SpackError):
    """
    Raised when gpg has no default key added.
    """

    def __init__(self, msg):
        super(NoKeyException, self).__init__(msg)


class PickKeyException(spack.error.SpackError):
    """
    Raised when multiple keys can be used to sign.
    """

    def __init__(self, keys):
        err_msg = "Multiple keys available for signing\n%s\n" % keys
        err_msg += "Use spack buildcache create -k <key hash> to pick a key."
        super(PickKeyException, self).__init__(err_msg)


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
        super(NoChecksumException, self).__init__(
            f"{algorithm} checksum failed for {path}",
            f"Expected {expected} but got {computed}. "
            f"File size = {size} bytes. Contents = {contents!r}",
        )


class NewLayoutException(spack.error.SpackError):
    """
    Raised if directory layout is different from buildcache.
    """

    def __init__(self, msg):
        super(NewLayoutException, self).__init__(msg)


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
    return _build_cache_relative_path


def build_cache_keys_relative_path():
    return _build_cache_keys_relative_path


def build_cache_prefix(prefix):
    return os.path.join(prefix, build_cache_relative_path())


def buildinfo_file_name(prefix):
    """
    Filename of the binary package meta-data file
    """
    name = os.path.join(prefix, ".spack/binary_distribution")
    return name


def read_buildinfo_file(prefix):
    """
    Read buildinfo file
    """
    filename = buildinfo_file_name(prefix)
    with open(filename, "r") as inputfile:
        content = inputfile.read()
        buildinfo = yaml.load(content)
    return buildinfo


class BuildManifestVisitor(BaseDirectoryVisitor):
    """Visitor that collects a list of files and symlinks
    that can be checked for need of relocation. It knows how
    to dedupe hardlinks and deal with symlinks to files and
    directories."""

    def __init__(self):
        # Save unique identifiers of files to avoid
        # relocating hardlink files for each path.
        self.visited = set()

        # Lists of files we will check
        self.files = []
        self.symlinks = []

    def seen_before(self, root, rel_path):
        stat_result = os.lstat(os.path.join(root, rel_path))
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
    prefixes.append(str(spack.store.layout.root))

    # Create a giant regex that matches all prefixes
    regex = utf8_paths_to_single_binary_regex(prefixes)

    # Symlinks.

    # Obvious bugs:
    #   1. relative links are not relocated.
    #   2. paths are used as strings.
    for rel_path in visitor.symlinks:
        abs_path = os.path.join(root, rel_path)
        link = os.readlink(abs_path)
        if os.path.isabs(link) and link.startswith(spack.store.layout.root):
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


def prefixes_to_hashes(spec):
    return {
        str(s.prefix): s.dag_hash()
        for s in itertools.chain(
            spec.traverse(root=True, deptype="link"), spec.dependencies(deptype="run")
        )
    }


def get_buildinfo_dict(spec, rel=False):
    """Create metadata for a tarball"""
    manifest = get_buildfile_manifest(spec)

    return {
        "sbang_install_path": spack.hooks.sbang.sbang_install_path(),
        "relative_rpaths": rel,
        "buildpath": spack.store.layout.root,
        "spackprefix": spack.paths.prefix,
        "relative_prefix": os.path.relpath(spec.prefix, spack.store.layout.root),
        "relocate_textfiles": manifest["text_to_relocate"],
        "relocate_binaries": manifest["binary_to_relocate"],
        "relocate_links": manifest["link_to_relocate"],
        "hardlinks_deduped": manifest["hardlinks_deduped"],
        "prefix_to_hash": prefixes_to_hashes(spec),
    }


def tarball_directory_name(spec):
    """
    Return name of the tarball directory according to the convention
    <os>-<architecture>/<compiler>/<package>-<version>/
    """
    return "%s/%s/%s-%s" % (
        spec.architecture,
        str(spec.compiler).replace("@", "-"),
        spec.name,
        spec.version,
    )


def tarball_name(spec, ext):
    """
    Return the name of the tarfile according to the convention
    <os>-<architecture>-<package>-<dag_hash><ext>
    """
    return "%s-%s-%s-%s-%s%s" % (
        spec.architecture,
        str(spec.compiler).replace("@", "-"),
        spec.name,
        spec.version,
        spec.dag_hash(),
        ext,
    )


def tarball_path_name(spec, ext):
    """
    Return the full path+name for a given spec according to the convention
    <tarball_directory_name>/<tarball_name>
    """
    return os.path.join(tarball_directory_name(spec), tarball_name(spec, ext))


def checksum_tarball(file):
    # calculate sha256 hash of tar file
    block_size = 65536
    hasher = hashlib.sha256()
    with open(file, "rb") as tfile:
        buf = tfile.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = tfile.read(block_size)
    return hasher.hexdigest()


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

    Return:
        None
    """

    def _fetch_spec_from_mirror(spec_url):
        spec_file_contents = read_method(spec_url)

        if spec_file_contents:
            # Need full spec.json name or this gets confused with index.json.
            if spec_url.endswith(".json.sig"):
                specfile_json = Spec.extract_json_from_clearsig(spec_file_contents)
                return Spec.from_dict(specfile_json)
            if spec_url.endswith(".json"):
                return Spec.from_json(spec_file_contents)

    tp = multiprocessing.pool.ThreadPool(processes=concurrency)
    try:
        fetched_specs = tp.map(
            llnl.util.lang.star(_fetch_spec_from_mirror), [(f,) for f in file_list]
        )
    finally:
        tp.terminate()
        tp.join()

    for fetched_spec in fetched_specs:
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
        extra_args={"ContentType": "application/json"},
    )

    # Push the hash
    web_util.push_to_url(
        index_hash_path,
        url_util.join(cache_prefix, "index.json.hash"),
        keep_original=False,
        extra_args={"ContentType": "text/plain"},
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
    db_root_dir = os.path.join(tmpdir, "db_root")
    db = spack_db.Database(
        None,
        db_dir=db_root_dir,
        enable_transaction_locking=False,
        record_fields=["spec", "ref_count", "in_buildcache"],
    )

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


@contextmanager
def gzip_compressed_tarfile(path):
    """Create a reproducible, compressed tarfile"""
    # Create gzip compressed tarball of the install prefix
    # 1) Use explicit empty filename and mtime 0 for gzip header reproducibility.
    #    If the filename="" is dropped, Python will use fileobj.name instead.
    #    This should effectively mimick `gzip --no-name`.
    # 2) On AMD Ryzen 3700X and an SSD disk, we have the following on compression speed:
    # compresslevel=6 gzip default: llvm takes 4mins, roughly 2.1GB
    # compresslevel=9 python default: llvm takes 12mins, roughly 2.1GB
    # So we follow gzip.
    with open(path, "wb") as fileobj, closing(
        GzipFile(filename="", mode="wb", compresslevel=6, mtime=0, fileobj=fileobj)
    ) as gzip_file, tarfile.TarFile(name="", mode="w", fileobj=gzip_file) as tar:
        yield tar


def deterministic_tarinfo(tarinfo: tarfile.TarInfo):
    # We only add files, symlinks, hardlinks, and directories
    # No character devices, block devices and FIFOs should ever enter a tarball.
    if tarinfo.isdev():
        return None

    # For distribution, it makes no sense to user/group data; since (a) they don't exist
    # on other machines, and (b) they lead to surprises as `tar x` run as root will change
    # ownership if it can. We want to extract as the current user. By setting owner to root,
    # root will extract as root, and non-privileged user will extract as themselves.
    tarinfo.uid = 0
    tarinfo.gid = 0
    tarinfo.uname = ""
    tarinfo.gname = ""

    # Reset mtime to epoch time, our prefixes are not truly immutable, so files may get
    # touched; as long as the content does not change, this ensures we get stable tarballs.
    tarinfo.mtime = 0

    # Normalize mode
    if tarinfo.isfile() or tarinfo.islnk():
        # If user can execute, use 0o755; else 0o644
        # This is to avoid potentially unsafe world writable & exeutable files that may get
        # extracted when Python or tar is run with privileges
        tarinfo.mode = 0o644 if tarinfo.mode & 0o100 == 0 else 0o755
    else:  # symbolic link and directories
        tarinfo.mode = 0o755

    return tarinfo


def tar_add_metadata(tar: tarfile.TarFile, path: str, data: dict):
    # Serialize buildinfo for the tarball
    bstring = syaml.dump(data, default_flow_style=True).encode("utf-8")
    tarinfo = tarfile.TarInfo(name=path)
    tarinfo.size = len(bstring)
    tar.addfile(deterministic_tarinfo(tarinfo), io.BytesIO(bstring))


def _do_create_tarball(tarfile_path, binaries_dir, pkg_dir, buildinfo):
    with gzip_compressed_tarfile(tarfile_path) as tar:
        tar.add(name=binaries_dir, arcname=pkg_dir, filter=deterministic_tarinfo)
        tar_add_metadata(tar, buildinfo_file_name(pkg_dir), buildinfo)


def _build_tarball(
    spec,
    out_url,
    force=False,
    relative=False,
    unsigned=False,
    allow_root=False,
    key=None,
    regenerate_index=False,
):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).
    """
    if not spec.concrete:
        raise ValueError("spec must be concrete to build tarball")

    # set up some paths
    tmpdir = tempfile.mkdtemp()
    cache_prefix = build_cache_prefix(tmpdir)

    tarfile_name = tarball_name(spec, ".spack")
    tarfile_dir = os.path.join(cache_prefix, tarball_directory_name(spec))
    tarfile_path = os.path.join(tarfile_dir, tarfile_name)
    spackfile_path = os.path.join(cache_prefix, tarball_path_name(spec, ".spack"))
    remote_spackfile_path = url_util.join(out_url, os.path.relpath(spackfile_path, tmpdir))

    mkdirp(tarfile_dir)
    if web_util.url_exists(remote_spackfile_path):
        if force:
            web_util.remove_url(remote_spackfile_path)
        else:
            raise NoOverwriteException(url_util.format(remote_spackfile_path))

    # need to copy the spec file so the build cache can be downloaded
    # without concretizing with the current spack packages
    # and preferences

    spec_file = spack.store.layout.spec_file_path(spec)
    specfile_name = tarball_name(spec, ".spec.json")
    specfile_path = os.path.realpath(os.path.join(cache_prefix, specfile_name))
    signed_specfile_path = "{0}.sig".format(specfile_path)

    remote_specfile_path = url_util.join(
        out_url, os.path.relpath(specfile_path, os.path.realpath(tmpdir))
    )
    remote_signed_specfile_path = "{0}.sig".format(remote_specfile_path)

    # If force and exists, overwrite. Otherwise raise exception on collision.
    if force:
        if web_util.url_exists(remote_specfile_path):
            web_util.remove_url(remote_specfile_path)
        if web_util.url_exists(remote_signed_specfile_path):
            web_util.remove_url(remote_signed_specfile_path)
    elif web_util.url_exists(remote_specfile_path) or web_util.url_exists(
        remote_signed_specfile_path
    ):
        raise NoOverwriteException(url_util.format(remote_specfile_path))

    pkg_dir = os.path.basename(spec.prefix.rstrip(os.path.sep))
    workdir = os.path.join(tmpdir, pkg_dir)

    # TODO: We generally don't want to mutate any files, but when using relative
    # mode, Spack unfortunately *does* mutate rpaths and links ahead of time.
    # For now, we only make a full copy of the spec prefix when in relative mode.

    if relative:
        # tarfile is used because it preserves hardlink etc best.
        binaries_dir = workdir
        temp_tarfile_name = tarball_name(spec, ".tar")
        temp_tarfile_path = os.path.join(tarfile_dir, temp_tarfile_name)
        with closing(tarfile.open(temp_tarfile_path, "w")) as tar:
            tar.add(name="%s" % spec.prefix, arcname=".")
        with closing(tarfile.open(temp_tarfile_path, "r")) as tar:
            tar.extractall(workdir)
        os.remove(temp_tarfile_path)
    else:
        binaries_dir = spec.prefix

    # create info for later relocation and create tar
    buildinfo = get_buildinfo_dict(spec, relative)

    # optionally make the paths in the binaries relative to each other
    # in the spack install tree before creating tarball
    try:
        if relative:
            make_package_relative(workdir, spec, buildinfo, allow_root)
        elif not allow_root:
            ensure_package_relocatable(buildinfo, binaries_dir)
    except Exception as e:
        shutil.rmtree(tmpdir)
        tty.die(e)

    _do_create_tarball(tarfile_path, binaries_dir, pkg_dir, buildinfo)

    # remove copy of install directory
    if relative:
        shutil.rmtree(workdir)

    # get the sha256 checksum of the tarball
    checksum = checksum_tarball(tarfile_path)

    # add sha256 checksum to spec.json

    with open(spec_file, "r") as inputfile:
        content = inputfile.read()
        if spec_file.endswith(".json"):
            spec_dict = sjson.load(content)
        else:
            raise ValueError("{0} not a valid spec file type".format(spec_file))
    spec_dict["buildcache_layout_version"] = 1
    bchecksum = {}
    bchecksum["hash_algorithm"] = "sha256"
    bchecksum["hash"] = checksum
    spec_dict["binary_cache_checksum"] = bchecksum
    # Add original install prefix relative to layout root to spec.json.
    # This will be used to determine is the directory layout has changed.
    buildinfo = {}
    buildinfo["relative_prefix"] = os.path.relpath(spec.prefix, spack.store.layout.root)
    buildinfo["relative_rpaths"] = relative
    spec_dict["buildinfo"] = buildinfo

    with open(specfile_path, "w") as outfile:
        outfile.write(sjson.dump(spec_dict))

    # sign the tarball and spec file with gpg
    if not unsigned:
        key = select_signing_key(key)
        sign_specfile(key, force, specfile_path)

    # push tarball and signed spec json to remote mirror
    web_util.push_to_url(spackfile_path, remote_spackfile_path, keep_original=False)
    web_util.push_to_url(
        signed_specfile_path if not unsigned else specfile_path,
        remote_signed_specfile_path if not unsigned else remote_specfile_path,
        keep_original=False,
    )

    tty.debug('Buildcache for "{0}" written to \n {1}'.format(spec, remote_spackfile_path))

    try:
        # push the key to the build cache's _pgp directory so it can be
        # imported
        if not unsigned:
            push_keys(out_url, keys=[key], regenerate_index=regenerate_index, tmpdir=tmpdir)

        # create an index.json for the build_cache directory so specs can be
        # found
        if regenerate_index:
            generate_package_index(url_util.join(out_url, os.path.relpath(cache_prefix, tmpdir)))
    finally:
        shutil.rmtree(tmpdir)

    return None


def nodes_to_be_packaged(specs, root=True, dependencies=True):
    """Return the list of nodes to be packaged, given a list of specs.

    Args:
        specs (List[spack.spec.Spec]): list of root specs to be processed
        root (bool): include the root of each spec in the nodes
        dependencies (bool): include the dependencies of each
            spec in the nodes
    """
    if not root and not dependencies:
        return []
    elif dependencies:
        nodes = traverse.traverse_nodes(specs, root=root, deptype="all")
    else:
        nodes = set(specs)

    # Limit to installed non-externals.
    packageable = lambda n: not n.external and n.installed

    # Mass install check
    with spack.store.db.read_transaction():
        return list(filter(packageable, nodes))


def push(specs, push_url, include_root: bool = True, include_dependencies: bool = True, **kwargs):
    """Create a binary package for each of the specs passed as input and push them
    to a given push URL.

    Args:
        specs (List[spack.spec.Spec]): installed specs to be packaged
        push_url (str): url where to push the binary package
        include_root (bool): include the root of each spec in the nodes
        include_dependencies (bool): include the dependencies of each
            spec in the nodes
        **kwargs: TODO

    """
    # Be explicit about the arugment type
    if type(include_root) != bool or type(include_dependencies) != bool:
        raise ValueError("Expected include_root/include_dependencies to be True/False")

    nodes = nodes_to_be_packaged(specs, root=include_root, dependencies=include_dependencies)

    # TODO: This seems to be an easy target for task
    # TODO: distribution using a parallel pool
    for node in nodes:
        try:
            _build_tarball(node, push_url, **kwargs)
        except NoOverwriteException as e:
            warnings.warn(str(e))


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
    except web_util.FetchError:
        stage.destroy()
        return None

    return stage


def _delete_staged_downloads(download_result):
    """Clean up stages used to download tarball and specfile"""
    download_result["tarball_stage"].destroy()
    download_result["specfile_stage"].destroy()


def download_tarball(spec, unsigned=False, mirrors_for_spec=None):
    """
    Download binary tarball for given package into stage area, returning
    path to downloaded tarball if successful, None otherwise.

    Args:
        spec (spack.spec.Spec): Concrete spec
        unsigned (bool): Whether or not to require signed binaries
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
    if not spack.mirror.MirrorCollection():
        tty.die("Please add a spack mirror to allow " + "download of pre-compiled packages.")

    tarball = tarball_path_name(spec, ".spack")
    specfile_prefix = tarball_name(spec, ".spec")

    mirrors_to_try = []

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
    try_next = [
        i.fetch_url
        for i in spack.mirror.MirrorCollection().values()
        if i.fetch_url not in try_first
    ]

    for url in try_first + try_next:
        mirrors_to_try.append(
            {
                "specfile": url_util.join(url, _build_cache_relative_path, specfile_prefix),
                "spackfile": url_util.join(url, _build_cache_relative_path, tarball),
            }
        )

    tried_to_verify_sigs = []

    # Assumes we care more about finding a spec file by preferred ext
    # than by mirrory priority.  This can be made less complicated as
    # we remove support for deprecated spec formats and buildcache layouts.
    for ext in ["json.sig", "json"]:
        for mirror_to_try in mirrors_to_try:
            specfile_url = "{0}.{1}".format(mirror_to_try["specfile"], ext)
            spackfile_url = mirror_to_try["spackfile"]
            local_specfile_stage = try_fetch(specfile_url)
            if local_specfile_stage:
                local_specfile_path = local_specfile_stage.save_filename
                signature_verified = False

                if ext.endswith(".sig") and not unsigned:
                    # If we found a signed specfile at the root, try to verify
                    # the signature immediately.  We will not download the
                    # tarball if we could not verify the signature.
                    tried_to_verify_sigs.append(specfile_url)
                    signature_verified = try_verify(local_specfile_path)
                    if not signature_verified:
                        tty.warn("Failed to verify: {0}".format(specfile_url))

                if unsigned or signature_verified or not ext.endswith(".sig"):
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


def make_package_relative(workdir, spec, buildinfo, allow_root):
    """
    Change paths in binaries to relative paths. Change absolute symlinks
    to relative symlinks.
    """
    prefix = spec.prefix
    old_layout_root = buildinfo["buildpath"]
    orig_path_names = list()
    cur_path_names = list()
    for filename in buildinfo["relocate_binaries"]:
        orig_path_names.append(os.path.join(prefix, filename))
        cur_path_names.append(os.path.join(workdir, filename))

    platform = spack.platforms.by_name(spec.platform)
    if "macho" in platform.binary_formats:
        relocate.make_macho_binaries_relative(cur_path_names, orig_path_names, old_layout_root)

    if "elf" in platform.binary_formats:
        relocate.make_elf_binaries_relative(cur_path_names, orig_path_names, old_layout_root)

    allow_root or relocate.ensure_binaries_are_relocatable(cur_path_names)
    orig_path_names = list()
    cur_path_names = list()
    for linkname in buildinfo.get("relocate_links", []):
        orig_path_names.append(os.path.join(prefix, linkname))
        cur_path_names.append(os.path.join(workdir, linkname))
    relocate.make_link_relative(cur_path_names, orig_path_names)


def ensure_package_relocatable(buildinfo, binaries_dir):
    """Check if package binaries are relocatable."""
    binaries = [os.path.join(binaries_dir, f) for f in buildinfo["relocate_binaries"]]
    relocate.ensure_binaries_are_relocatable(binaries)


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
            if identifier in visited:
                continue
            visited.add(identifier)
            new_list.append(rel_path)
        buildinfo[key] = new_list


def relocate_package(spec, allow_root):
    """
    Relocate the given package
    """
    workdir = str(spec.prefix)
    buildinfo = read_buildinfo_file(workdir)
    new_layout_root = str(spack.store.layout.root)
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
    rel = buildinfo.get("relative_rpaths")
    prefix_to_hash = buildinfo.get("prefix_to_hash", None)
    if old_rel_prefix != new_rel_prefix and not prefix_to_hash:
        msg = "Package tarball was created from an install "
        msg += "prefix with a different directory layout and an older "
        msg += "buildcache create implementation. It cannot be relocated."
        raise NewLayoutException(msg)
    # older buildcaches do not have the prefix_to_hash dictionary
    # need to set an empty dictionary and add one entry to
    # prefix_to_prefix to reproduce the old behavior
    if not prefix_to_hash:
        prefix_to_hash = dict()
    hash_to_prefix = dict()
    hash_to_prefix[spec.format("{hash}")] = str(spec.package.prefix)
    new_deps = spack.build_environment.get_rpath_deps(spec.package)
    for d in new_deps + spec.dependencies(deptype="run"):
        hash_to_prefix[d.format("{hash}")] = str(d.prefix)
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
    for orig_prefix, hash in prefix_to_hash.items():
        prefix_to_prefix_text[orig_prefix] = hash_to_prefix.get(hash, None)
        prefix_to_prefix_bin[orig_prefix] = hash_to_prefix.get(hash, None)

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
        relocate.relocate_text_bin(files_to_relocate, prefix_to_prefix_bin)

    # If we are installing back to the same location
    # relocate the sbang location if the spack directory changed
    else:
        if old_spack_prefix != new_spack_prefix:
            relocate.relocate_text(text_names, prefix_to_prefix_text)


def _extract_inner_tarball(spec, filename, extract_to, unsigned, remote_checksum):
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

    if not unsigned:
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
    local_checksum = checksum_tarball(tarfile_path)
    expected = remote_checksum["hash"]

    # if the checksums don't match don't install
    if local_checksum != expected:
        size, contents = fsys.filesummary(tarfile_path)
        raise NoChecksumException(tarfile_path, size, contents, "sha256", expected, local_checksum)

    return tarfile_path


def extract_tarball(spec, download_result, allow_root=False, unsigned=False, force=False):
    """
    extract binary tarball for given package into install area
    """
    if os.path.exists(spec.prefix):
        if force:
            shutil.rmtree(spec.prefix)
        else:
            raise NoOverwriteException(str(spec.prefix))

    specfile_path = download_result["specfile_stage"].save_filename

    with open(specfile_path, "r") as inputfile:
        content = inputfile.read()
        if specfile_path.endswith(".json.sig"):
            spec_dict = Spec.extract_json_from_clearsig(content)
        else:
            spec_dict = sjson.load(content)

    bchecksum = spec_dict["binary_cache_checksum"]
    filename = download_result["tarball_stage"].save_filename
    signature_verified = download_result["signature_verified"]
    tmpdir = None

    if (
        "buildcache_layout_version" not in spec_dict
        or int(spec_dict["buildcache_layout_version"]) < 1
    ):
        # Handle the older buildcache layout where the .spack file
        # contains a spec json, maybe an .asc file (signature),
        # and another tarball containing the actual install tree.
        tmpdir = tempfile.mkdtemp()
        try:
            tarfile_path = _extract_inner_tarball(spec, filename, tmpdir, unsigned, bchecksum)
        except Exception as e:
            _delete_staged_downloads(download_result)
            shutil.rmtree(tmpdir)
            raise e
    else:
        # Newer buildcache layout: the .spack file contains just
        # in the install tree, the signature, if it exists, is
        # wrapped around the spec.json at the root.  If sig verify
        # was required, it was already done before downloading
        # the tarball.
        tarfile_path = filename

        if not unsigned and not signature_verified:
            raise UnsignedPackageException(
                "To install unsigned packages, use the --no-check-signature option."
            )

        # compute the sha256 checksum of the tarball
        local_checksum = checksum_tarball(tarfile_path)
        expected = bchecksum["hash"]

        # if the checksums don't match don't install
        if local_checksum != expected:
            size, contents = fsys.filesummary(tarfile_path)
            _delete_staged_downloads(download_result)
            raise NoChecksumException(
                tarfile_path, size, contents, "sha256", expected, local_checksum
            )

    new_relative_prefix = str(os.path.relpath(spec.prefix, spack.store.layout.root))
    # if the original relative prefix is in the spec file use it
    buildinfo = spec_dict.get("buildinfo", {})
    old_relative_prefix = buildinfo.get("relative_prefix", new_relative_prefix)
    rel = buildinfo.get("relative_rpaths")
    info = "old relative prefix %s\nnew relative prefix %s\nrelative rpaths %s"
    tty.debug(info % (old_relative_prefix, new_relative_prefix, rel), level=2)

    # Extract the tarball into the store root, presumably on the same filesystem.
    # The directory created is the base directory name of the old prefix.
    # Moving the old prefix name to the new prefix location should preserve
    # hard links and symbolic links.
    extract_tmp = os.path.join(spack.store.layout.root, ".tmp")
    mkdirp(extract_tmp)
    extracted_dir = os.path.join(extract_tmp, old_relative_prefix.split(os.path.sep)[-1])

    with closing(tarfile.open(tarfile_path, "r")) as tar:
        try:
            tar.extractall(path=extract_tmp)
        except Exception as e:
            _delete_staged_downloads(download_result)
            shutil.rmtree(extracted_dir)
            raise e
    try:
        shutil.move(extracted_dir, spec.prefix)
    except Exception as e:
        _delete_staged_downloads(download_result)
        shutil.rmtree(extracted_dir)
        raise e
    os.remove(tarfile_path)
    os.remove(specfile_path)

    try:
        relocate_package(spec, allow_root)
    except Exception as e:
        shutil.rmtree(spec.prefix)
        raise e
    else:
        manifest_file = os.path.join(
            spec.prefix, spack.store.layout.metadata_dir, spack.store.layout.manifest_file_name
        )
        if not os.path.exists(manifest_file):
            spec_id = spec.format("{name}/{hash:7}")
            tty.warn("No manifest file in tarball for spec %s" % spec_id)
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir)
        if os.path.exists(filename):
            os.remove(filename)
        _delete_staged_downloads(download_result)


def install_root_node(spec, allow_root, unsigned=False, force=False, sha256=None):
    """Install the root node of a concrete spec from a buildcache.

    Checking the sha256 sum of a node before installation is usually needed only
    for software installed during Spack's bootstrapping (since we might not have
    a proper signature verification mechanism available).

    Args:
        spec: spec to be installed (note that only the root node will be installed)
        allow_root (bool): allows the root directory to be present in binaries
            (may affect relocation)
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
        extract_tarball(spec, download_result, allow_root, unsigned, force)
        spack.hooks.post_install(spec)
        spack.store.db.add(spec, spack.store.layout)


def install_single_spec(spec, allow_root=False, unsigned=False, force=False):
    """Install a single concrete spec from a buildcache.

    Args:
        spec (spack.spec.Spec): spec to be installed
        allow_root (bool): allows the root directory to be present in binaries
            (may affect relocation)
        unsigned (bool): if True allows installing unsigned binaries
        force (bool): force installation if the spec is already present in the
            local store
    """
    for node in spec.traverse(root=True, order="post", deptype=("link", "run")):
        install_root_node(node, allow_root=allow_root, unsigned=unsigned, force=force)


def try_direct_fetch(spec, mirrors=None):
    """
    Try to find the spec directly on the configured mirrors
    """
    specfile_name = tarball_name(spec, ".spec.json")
    signed_specfile_name = tarball_name(spec, ".spec.json.sig")
    specfile_is_signed = False
    found_specs = []

    for mirror in spack.mirror.MirrorCollection(mirrors=mirrors).values():
        buildcache_fetch_url_json = url_util.join(
            mirror.fetch_url, _build_cache_relative_path, specfile_name
        )
        buildcache_fetch_url_signed_json = url_util.join(
            mirror.fetch_url, _build_cache_relative_path, signed_specfile_name
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

    if not spack.mirror.MirrorCollection(mirrors=mirrors_to_check):
        tty.debug("No Spack mirrors are currently configured")
        return {}

    results = binary_index.find_built_spec(spec, mirrors_to_check=mirrors_to_check)

    # The index may be out-of-date. If we aren't only considering indices, try
    # to fetch directly since we know where the file should be.
    if not results and not index_only:
        results = try_direct_fetch(spec, mirrors=mirrors_to_check)
        # We found a spec by the direct fetch approach, we might as well
        # add it to our mapping.
        if results:
            binary_index.update_spec(spec, results)

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
    binary_index.update()
    return binary_index.get_all_built_specs()


def clear_spec_cache():
    binary_index.clear()


def get_keys(install=False, trust=False, force=False, mirrors=None):
    """Get pgp public keys available on mirror with suffix .pub"""
    mirror_collection = mirrors or spack.mirror.MirrorCollection()

    if not mirror_collection:
        tty.die("Please add a spack mirror to allow " + "download of build caches.")

    for mirror in mirror_collection.values():
        fetch_url = mirror.fetch_url
        keys_url = url_util.join(
            fetch_url, _build_cache_relative_path, _build_cache_keys_relative_path
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
                    except web_util.FetchError:
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
                push_url, _build_cache_relative_path, _build_cache_keys_relative_path
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
    for mirror in spack.mirror.MirrorCollection(mirrors).values():
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
            except web_util.FetchError as e:
                tty.debug(e)
        else:
            if fail_if_missing:
                tty.error("Failed to download required url {0}".format(description_url))
                return False
    return True


def download_buildcache_entry(file_descriptions, mirror_url=None):
    if not mirror_url and not spack.mirror.MirrorCollection():
        tty.die(
            "Please provide or add a spack mirror to allow " + "download of buildcache entries."
        )

    if mirror_url:
        mirror_root = os.path.join(mirror_url, _build_cache_relative_path)
        return _download_buildcache_entry(mirror_root, file_descriptions)

    for mirror in spack.mirror.MirrorCollection().values():
        mirror_root = os.path.join(mirror.fetch_url, _build_cache_relative_path)

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


class BinaryCacheQuery(object):
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

    def __call__(self, spec, **kwargs):
        matches = []
        if spec.startswith("/"):
            # Matching a DAG hash
            query_hash = spec.replace("/", "")
            for candidate_spec in self.possible_specs:
                if candidate_spec.dag_hash().startswith(query_hash):
                    matches.append(candidate_spec)
        else:
            # Matching a spec constraint
            matches = [s for s in self.possible_specs if s.satisfies(spec)]
        return matches


class FetchIndexError(Exception):
    def __str__(self):
        if len(self.args) == 1:
            return str(self.args[0])
        else:
            return "{}, due to: {}".format(self.args[0], self.args[1])


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
        url_index_hash = url_util.join(self.url, _build_cache_relative_path, "index.json.hash")
        try:
            response = self.urlopen(urllib.request.Request(url_index_hash, headers=self.headers))
        except urllib.error.URLError:
            return None

        # Validate the hash
        remote_hash = response.read(64)
        if not re.match(rb"[a-f\d]{64}$", remote_hash):
            return None
        return remote_hash.decode("utf-8")

    def conditional_fetch(self):
        # Do an intermediate fetch for the hash
        # and a conditional fetch for the contents

        # Early exit if our cache is up to date.
        if self.local_hash and self.local_hash == self.get_remote_hash():
            return FetchIndexResult(etag=None, hash=None, data=None, fresh=True)

        # Otherwise, download index.json
        url_index = url_util.join(self.url, _build_cache_relative_path, "index.json")

        try:
            response = self.urlopen(urllib.request.Request(url_index, headers=self.headers))
        except urllib.error.URLError as e:
            raise FetchIndexError("Could not fetch index from {}".format(url_index), e)

        try:
            result = codecs.getreader("utf-8")(response).read()
        except ValueError as e:
            return FetchCacheError("Remote index {} is invalid".format(url_index), e)

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

    def conditional_fetch(self):
        # Just do a conditional fetch immediately
        url = url_util.join(self.url, _build_cache_relative_path, "index.json")
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
