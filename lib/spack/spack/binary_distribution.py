# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import collections
import hashlib
import json
import multiprocessing.pool
import os
import shutil
import sys
import tarfile
import tempfile
import time
import traceback
import typing
import warnings
from contextlib import closing
from urllib.error import HTTPError, URLError

import ruamel.yaml as yaml

import llnl.util.filesystem as fsys
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, mkdirp, visit_directory_tree

import spack.cmd
import spack.config as config
import spack.hash_types as ht
import spack.hooks
import spack.hooks.sbang
import spack.mirror
import spack.platforms
import spack.relocate as relocate
import spack.repo
import spack.store
import spack.util.file_cache as file_cache
import spack.util.gpg
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.util.web as web_util
from spack.caches import misc_cache_location
from spack.relocate import utf8_paths_to_single_binary_regex
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import which

_build_cache_relative_path = "build_cache"
_build_cache_keys_relative_path = "_pgp"


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

    def __init__(self, cache_root: str):
        # a FileCache instance storing copies of remote binary cache indices
        self._file_cache = file_cache.FileCache(cache_root)

        # mapping from mirror urls to the time.time() of the last index fetch.
        self._last_fetch_times: typing.Dict[str, float] = {}

        # mapping from mirror urls to either:
        #  - The dict[str, Spec] of concrete specs available indexed by DAG hash, or
        #  - The set[str] of DAG hashes of available concrete specs.
        self._mirror_specs: typing.Dict[
            str, typing.Union[typing.Dict[str, Spec], typing.Set[str]]
        ] = {}

    def clear(self) -> None:
        """For testing purposes we need to be able to empty the cache and
        clear associated data structures."""
        self._file_cache.destroy()
        self._last_fetch_times = {}
        self._mirror_specs = {}

    @classmethod
    def _cache_keys_for(cls, mirror_url: str, filename: str) -> typing.Tuple[str, str]:
        """
        Construct the cache keys for the given cached files.

        Args:
            mirror_url (str): Base URL of the mirror
            filename (str): Filenames of the file cached from the mirror

        Returns:
            hash_key (str): Cache key for the content hash
            data_key (str): Cache key for the content
        """
        hash_str = hashlib.sha256(mirror_url.encode("utf-8")).hexdigest()
        prefix = f"{hash_str[:2]}/{hash_str[2:]}/"
        return prefix + filename + ".hash", prefix + filename

    def get_all_built_specs(self) -> typing.List[Spec]:
        result: typing.List[Spec] = []
        for m in spack.mirror.MirrorCollection().values():
            result.extend(self._load_specs_for(m.fetch_url).values())
        return result

    def find_built_spec(
        self,
        spec,
        *,
        mirrors_to_check: typing.Optional[typing.Dict[str, str]] = None,
        concrete: bool = True,
    ) -> list:
        """Look in our cache for the built spec corresponding to ``spec``.

        If the spec can be found among the configured binary mirrors, a
        list is returned that contains the mirror URLs of a subset of mirrors
        where it can be found.  Otherwise, ``None`` is returned.

        Note that this does NOT check whether ``spec`` is exactly in the remote
        mirror's buildcache, it only checks whether the DAG hash matches.

        Args:
            spec (spack.spec.Spec): Concrete spec to find
            mirrors_to_check: Optional mapping containing mirrors to check.  If
                None, just assumes all configured mirrors.
            concrete (bool): If False, the ``"spec"`` key is removed from the
                output ``dicts``, which may improve performance.

        Returns:
            An list of objects containing the mirror url when ``spec`` was found:

                .. code-block:: python

                    [
                        {
                            "mirror_url": <mirror-root-url>,
                            "spec": <upstream-concrete-spec>,
                        }, ...
                    ]
        """

        spec_hash = spec.dag_hash()
        m_urls = (
            mirrors_to_check.values()
            if mirrors_to_check is not None
            else map(lambda m: m.fetch_url, spack.mirror.MirrorCollection().values())
        )

        if not concrete:
            # Fast path: we don't need to load the full Spec objects
            return [{"mirror_url": mu} for mu in m_urls if spec_hash in self._load_hashes_for(mu)]

        found = []
        for mu in m_urls:
            spec = self._load_specs_for(mu).get(spec_hash)
            if spec is not None:
                found.append({"mirror_url": mu, "spec": spec})
        return found

    @classmethod
    def _specs_from_index(cls, data: dict) -> typing.Dict[str, typing.Tuple[dict, bool]]:
        """Read an index.json and extract the list of contained specs.

        Returns a dict, keys are DAG hash of the Specs and values are a tuple of:
            sdict (dict): Spec in node-dict form
            in_buildcache (bool): If False, this spec is not actually in the buildcache
        """
        if "database" not in data:
            raise ValueError("Corrupt index.json, no database field!")
        db = data["database"]
        if "version" not in db or db["version"] != "6":
            raise ValueError("Corrupt index.json, must be version 6!")
        if "installs" not in db:
            raise ValueError("Corrupt index.json, no installs field!")

        def parse(shash: str, rec: dict) -> typing.Tuple[dict, bool]:
            sdict = rec["spec"]
            sdict[ht.dag_hash.name] = shash
            return sdict, rec.get("in_buildcache", False)

        return {shash: parse(shash, sdict) for shash, sdict in db["installs"].items()}

    def _load_hashes_for(self, mirror_url: str) -> collections.abc.Container:
        """
        Lazily load part of the index for the given mirror into memory.

        This version only loads the DAG hashes for the concrete specs. If the
        full Spec objects are required, see ``_load_specs_for()``.

        Returns the final entry in ``self._mirror_specs``, or an empty set if
        the mirror is not in the cache.
        """

        if mirror_url in self._mirror_specs:
            # Specs are already loaded, don't reload
            return self._mirror_specs[mirror_url]

        _, data_key = self._cache_keys_for(mirror_url, "index.json")
        if not self._file_cache.init_entry(data_key):
            # Data file doesn't exist, we don't have anything to load
            return set()

        # Load and convert to set
        with self._file_cache.read_transaction(data_key) as data_f:
            data = json.load(data_f)
        result = set(self._specs_from_index(data).keys())

        # Memoize and return
        self._mirror_specs[mirror_url] = result
        return result

    def _load_specs_for(self, mirror_url: str) -> typing.Dict[str, Spec]:
        """
        Lazily load the index for the given mirror into memory.

        This version loads the full concrete Spec objects. If only the DAG
        hashes are required, see ``_load_hashes_for()``.

        Returns the final entry in ``self._mirror_specs``, or an empty dict if
        the mirror is not in the cache.
        """

        previous = self._mirror_specs.get(mirror_url)
        if isinstance(previous, dict):
            # Specs are already loaded, don't reload
            return previous

        _, data_key = self._cache_keys_for(mirror_url, "index.json")
        if not self._file_cache.init_entry(data_key):
            # Data file doesn't exist, we don't have anything to load
            return dict()

        with self._file_cache.read_transaction(data_key) as data_f:
            data = json.load(data_f)
        raw_specs = self._specs_from_index(data)
        result = {shash: Spec.from_node_dict(sdict) for shash, (sdict, _) in raw_specs.items()}

        # Add dependency links between Specs
        for shash, spec in result.items():
            sdict = raw_specs[shash][0]
            if "dependencies" in sdict:
                for _, dhash, dtypes, _ in Spec.read_yaml_dep_specs(sdict["dependencies"]):
                    spec._add_dependency(result[dhash], dtypes)

        # Mark all Specs as concrete
        for spec in result.values():
            spec._mark_root_concrete()

        # Only keep the root specs that are actually in_buildcache
        for shash, (_, in_bc) in raw_specs.items():
            if not in_bc:
                del result[shash]

        # Memoize and return
        self._mirror_specs[mirror_url] = result
        return result

    def update(self, *, with_cooldown: bool = False) -> None:
        """
        Make sure local cache of buildcache index files is up to date.

        If the remote buildcache indices for configured mirrors have not changed
        since the indices were previously fetched, calling this method will only
        result in fetching the ``index.json.hash`` from each mirror. Otherwise,
        the buildcache ``index.json`` is retrieved and stored locally under the
        ``cache_root`` passed to ``__init__()``.

        The actual indices are loaded into memory lazily on request.

        Returns nothing and raises no errors on failure.
        """
        filename = "index.json"

        ttl = spack.config.get("config:binary_index_ttl", 600)
        now = time.time()

        new_fetch_times = {}
        for m in spack.mirror.MirrorCollection().values():
            fetch_url = m.fetch_url

            # If we're in the cooldown period, don't re-fetch and assume the
            # current state is good enough.
            if (
                with_cooldown
                and ttl > 0
                and fetch_url in self._last_fetch_times
                and now - self._last_fetch_times[fetch_url] < ttl
            ):
                new_fetch_times[fetch_url] = self._last_fetch_times[fetch_url]
                continue
            new_fetch_times[fetch_url] = now

            # Update our local copy of the index in the file cache
            # If it changed, purge our in-memory cache of the file cache
            if self._update_for(fetch_url, filename):
                self._mirror_specs.pop(fetch_url, None)

        self._last_fetch_times = new_fetch_times

    def _update_for(self, mirror_url: str, filename: str) -> typing.Optional[bool]:
        """Ensure a cached buildcache file for a remote mirror is up-to-date.

        If we already have a cached file from this mirror, we first check if
        the hash has changed and avoid a larger fetch if it has not.

        Args:
           mirror_url (str): Base URL of mirror
           filename (str): Filename for the file to fetch from the mirror
           key (str): Identifier to use in the metadata for this file

        Returns:
           True if this function updated the cached file,
           False if it detected that no update was needed, and
           None if there was an error preventing the update.

        Note that a return value of None does not mean there isn't a cached
        file present, it just means that it may not be perfectly up-to-date.
        """

        hash_url = url_util.join(mirror_url, _build_cache_relative_path, filename + ".hash")
        data_url = url_util.join(mirror_url, _build_cache_relative_path, filename)

        hash_key, data_key = self._cache_keys_for(mirror_url, filename)

        # Fast path: we already have the file and it is up-to-date
        previous_hash = None
        if self._file_cache.init_entry(hash_key):
            with self._file_cache.read_transaction(hash_key) as hash_f:
                try:
                    _, _, fs = web_util.read_from_url(hash_url)
                    expected_hash = codecs.getreader("utf-8")(fs).read()
                except (URLError, web_util.SpackWebError):
                    pass  # No expected hash upstream, ignore
                else:
                    previous_hash = hash_f.read()
                    if previous_hash == expected_hash:
                        return False  # Up-to-date, skip the update

        # We either don't have the file, or it is out-of-date. Let's update!
        try:
            with self._file_cache.write_transaction(hash_key) as (oldhash_f, newhash_f):
                # Fast path: someone else updated the file in the moment when we weren't
                # holding the lock. Our expected_hash may be out-of-date now, so assume
                # the other guy did good instead of aggressively checking.
                if oldhash_f is not None:
                    current_hash = oldhash_f.read()
                    if current_hash != previous_hash:
                        return False

                # At this point: we need to fetch the file. No two ways about it.
                # Do the fetch now, so that if it fails we don't leave any cruft behind.
                # We will catch the exception this raises outside the write_transaction
                _, _, fs = web_util.read_from_url(data_url)
                data = codecs.getreader("utf-8")(fs).read()

                # Stash the final updated file in the cache at the appropriate key
                with self._file_cache.write_transaction(data_key) as (_, data_f):
                    data_f.write(data)

                # Update the hash to match our new reality
                newhash_f.write(compute_hash(data))
        except (URLError, web_util.SpackWebError):
            # We had an error while attempting to fetch the data. These indices
            # do not need to exist for proper operation, so ignore the error.
            return None

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
        err_msg = "\n%s\nexists\n" % file_path
        err_msg += "Use -f option to overwrite."
        super(NoOverwriteException, self).__init__(err_msg)


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

    pass


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
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


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


def write_buildinfo_file(spec, workdir, rel=False):
    """
    Create a cache file containing information
    required for the relocation
    """
    manifest = get_buildfile_manifest(spec)

    prefix_to_hash = dict()
    prefix_to_hash[str(spec.package.prefix)] = spec.dag_hash()
    deps = spack.build_environment.get_rpath_deps(spec.package)
    for d in deps + spec.dependencies(deptype="run"):
        prefix_to_hash[str(d.prefix)] = d.dag_hash()

    # Create buildinfo data and write it to disk
    buildinfo = {}
    buildinfo["sbang_install_path"] = spack.hooks.sbang.sbang_install_path()
    buildinfo["relative_rpaths"] = rel
    buildinfo["buildpath"] = spack.store.layout.root
    buildinfo["spackprefix"] = spack.paths.prefix
    buildinfo["relative_prefix"] = os.path.relpath(spec.prefix, spack.store.layout.root)
    buildinfo["relocate_textfiles"] = manifest["text_to_relocate"]
    buildinfo["relocate_binaries"] = manifest["binary_to_relocate"]
    buildinfo["relocate_links"] = manifest["link_to_relocate"]
    buildinfo["hardlinks_deduped"] = manifest["hardlinks_deduped"]
    buildinfo["prefix_to_hash"] = prefix_to_hash
    filename = buildinfo_file_name(workdir)
    with open(filename, "w") as outfile:
        outfile.write(syaml.dump(buildinfo, default_flow_style=True))


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


def _read_specs_and_push_index(file_list, read_method, cache_prefix, concurrency):
    """Read all the specs listed in the provided list, using thread given thread parallelism,
        generate the index, and push it to the mirror.

    Args:
        file_list (list(str)): List of urls or file paths pointing at spec files to read
        read_method: A function taking a single argument, either a url or a file path,
            and which reads the spec file at that location, and returns the spec.
        cache_prefix (str): prefix of the build cache on s3 where index should be pushed.
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

    # Recursively lower the Specs into spec-dict (+ record) form
    installs = {}

    def add(spec):
        key = spec.dag_hash()
        if key in installs:
            return installs[key]
        for edge in spec.edges_to_dependencies(deptype=ht.dag_hash.deptype):
            add(edge.spec)
        result = {"spec": spec.node_dict_with_hashes()}
        installs[key] = result
        return result

    for s in fetched_specs:
        r = add(s)
        r["in_buildcache"] = True

    db = {
        "database": {
            "version": "6",
            "installs": installs,
        },
    }

    # Now convert the index to JSON, compute its hash, and push the two files to
    # the mirror.
    index = sjson.dump(db)
    index_hash = compute_hash(index)
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write out the index JSON
        index_json_path = os.path.join(temp_dir, "index.json")
        with open(index_json_path, "w") as f:
            f.write(index)

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
        tty.error("Unabled to generate package index, {0}".format(err))
        return

    tty.debug("Retrieving spec descriptor files from {0} to build index".format(cache_prefix))

    try:
        _read_specs_and_push_index(file_list, read_fn, cache_prefix, concurrency)
    except Exception as err:
        msg = "Encountered problem pushing package index to {0}: {1}".format(cache_prefix, err)
        tty.warn(msg)
        tty.debug("\n" + traceback.format_exc())


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

    # make a copy of the install directory to work with
    workdir = os.path.join(tmpdir, os.path.basename(spec.prefix))
    # install_tree copies hardlinks
    # create a temporary tarfile from prefix and exract it to workdir
    # tarfile preserves hardlinks
    temp_tarfile_name = tarball_name(spec, ".tar")
    temp_tarfile_path = os.path.join(tarfile_dir, temp_tarfile_name)
    with closing(tarfile.open(temp_tarfile_path, "w")) as tar:
        tar.add(name="%s" % spec.prefix, arcname=".")
    with closing(tarfile.open(temp_tarfile_path, "r")) as tar:
        tar.extractall(workdir)
    os.remove(temp_tarfile_path)

    # create info for later relocation and create tar
    write_buildinfo_file(spec, workdir, relative)

    # optionally make the paths in the binaries relative to each other
    # in the spack install tree before creating tarball
    if relative:
        try:
            make_package_relative(workdir, spec, allow_root)
        except Exception as e:
            shutil.rmtree(workdir)
            shutil.rmtree(tarfile_dir)
            shutil.rmtree(tmpdir)
            tty.die(e)
    else:
        try:
            check_package_relocatable(workdir, spec, allow_root)
        except Exception as e:
            shutil.rmtree(workdir)
            shutil.rmtree(tarfile_dir)
            shutil.rmtree(tmpdir)
            tty.die(e)

    # create gzip compressed tarball of the install prefix
    # On AMD Ryzen 3700X and an SSD disk, we have the following on compression speed:
    # compresslevel=6 gzip default: llvm takes 4mins, roughly 2.1GB
    # compresslevel=9 python default: llvm takes 12mins, roughly 2.1GB
    # So we follow gzip.
    with closing(tarfile.open(tarfile_path, "w:gz", compresslevel=6)) as tar:
        tar.add(name="%s" % workdir, arcname="%s" % os.path.basename(spec.prefix))
    # remove copy of install directory
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


def nodes_to_be_packaged(specs, include_root=True, include_dependencies=True):
    """Return the list of nodes to be packaged, given a list of specs.

    Args:
        specs (List[spack.spec.Spec]): list of root specs to be processed
        include_root (bool): include the root of each spec in the nodes
        include_dependencies (bool): include the dependencies of each
            spec in the nodes
    """
    if not include_root and not include_dependencies:
        return set()

    def skip_node(current_node):
        if current_node.external or current_node.virtual:
            return True
        return spack.store.db.query_one(current_node) is None

    expanded_set = set()
    for current_spec in specs:
        if not include_dependencies:
            nodes = [current_spec]
        else:
            nodes = [
                n
                for n in current_spec.traverse(
                    order="post", root=include_root, deptype=("link", "run")
                )
            ]

        for node in nodes:
            if not skip_node(node):
                expanded_set.add(node)

    return expanded_set


def push(specs, push_url, specs_kwargs=None, **kwargs):
    """Create a binary package for each of the specs passed as input and push them
    to a given push URL.

    Args:
        specs (List[spack.spec.Spec]): installed specs to be packaged
        push_url (str): url where to push the binary package
        specs_kwargs (dict): dictionary with two possible boolean keys, "include_root"
            and "include_dependencies", which determine which part of each spec is
            packaged and pushed to the mirror
        **kwargs: TODO

    """
    specs_kwargs = specs_kwargs or {"include_root": True, "include_dependencies": True}
    nodes = nodes_to_be_packaged(specs, **specs_kwargs)

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


def make_package_relative(workdir, spec, allow_root):
    """
    Change paths in binaries to relative paths. Change absolute symlinks
    to relative symlinks.
    """
    prefix = spec.prefix
    buildinfo = read_buildinfo_file(workdir)
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


def check_package_relocatable(workdir, spec, allow_root):
    """
    Check if package binaries are relocatable.
    Change links to placeholder links.
    """
    buildinfo = read_buildinfo_file(workdir)
    cur_path_names = list()
    for filename in buildinfo["relocate_binaries"]:
        cur_path_names.append(os.path.join(workdir, filename))
    allow_root or relocate.ensure_binaries_are_relocatable(cur_path_names)


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
        relocate.unsafe_relocate_text(text_names, prefix_to_prefix_text)

        # relocate the install prefixes in binary files including dependencies
        relocate.unsafe_relocate_text_bin(files_to_relocate, prefix_to_prefix_bin)

    # If we are installing back to the same location
    # relocate the sbang location if the spack directory changed
    else:
        if old_spack_prefix != new_spack_prefix:
            relocate.unsafe_relocate_text(text_names, prefix_to_prefix_text)


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
    # get the sha256 checksum of the tarball
    local_checksum = checksum_tarball(tarfile_path)

    # if the checksums don't match don't install
    if local_checksum != remote_checksum["hash"]:
        raise NoChecksumException(
            "Package tarball failed checksum verification.\n" "It cannot be installed."
        )

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

        # if the checksums don't match don't install
        if local_checksum != bchecksum["hash"]:
            _delete_staged_downloads(download_result)
            raise NoChecksumException(
                "Package tarball failed checksum verification.\n" "It cannot be installed."
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
            _delete_staged_downloads(download_result)
            raise spack.binary_distribution.NoChecksumException(msg)
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

        found_specs.append(
            {
                "mirror_url": mirror.fetch_url,
                "spec": fetched_spec,
            }
        )

    return found_specs


def get_mirrors_for_spec(
    spec=None,
    mirrors_to_check: typing.Optional[typing.Dict[str, str]] = None,
    index_only: bool = False,
    concrete: bool = True,
):
    """
    Check if concrete spec exists on mirrors and return a list
    indicating the mirrors on which it can be found

    Args:
        spec (spack.spec.Spec): The spec to look for in binary mirrors
        mirrors_to_check (dict): Optionally override the configured mirrors
            with the mirrors in this dictionary.
        index_only (bool): When ``index_only`` is set to ``True``, only the local
            cache is checked, no requests are made.
        concrete (bool): If ``False``, the concrete spec may not be returned for
            improved performance.

    Return:
        A list of objects, each containing a ``mirror_url`` and ``spec`` key
            indicating all mirrors where the spec can be found.
    """
    if spec is None:
        return []

    if not spack.mirror.MirrorCollection(mirrors=mirrors_to_check):
        tty.debug("No Spack mirrors are currently configured")
        return {}

    results = binary_index.find_built_spec(
        spec, mirrors_to_check=mirrors_to_check, concrete=concrete
    )

    # The index may be out-of-date. If we aren't only considering indices, try
    # to fetch directly since we know where the file should be.
    if not results and not index_only:
        results = try_direct_fetch(spec, mirrors=mirrors_to_check)

    return results


def update_cache_and_get_specs():
    """
    Get all concrete specs for build caches available on configured mirrors.
    Initialization of internal cache data structures is done as lazily as
    possible, so this method will also attempt to initialize and update the
    local index cache (essentially a no-op if it has been done already and
    nothing has changed on the configured mirrors.)
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
        {
            "url": [tarball_path_name],
            "path": local_tarball_path,
            "required": True,
        },
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
