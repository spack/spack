# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import collections
import hashlib
import json
import os
import shutil
import sys
import tarfile
import tempfile
import traceback
import warnings
from contextlib import closing

import ruamel.yaml as yaml
from six.moves.urllib.error import HTTPError, URLError

import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.cmd
import spack.config as config
import spack.database as spack_db
import spack.fetch_strategy as fs
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
from spack.spec import Spec
from spack.stage import Stage

_build_cache_relative_path = 'build_cache'
_build_cache_keys_relative_path = '_pgp'


class FetchCacheError(Exception):
    """Error thrown when fetching the cache failed, usually a composite error list."""
    def __init__(self, errors):
        if not isinstance(errors, list):
            raise TypeError("Expected a list of errors")
        self.errors = errors
        if len(errors) > 1:
            msg = "        Error {0}: {1}: {2}"
            self.message = "Multiple errors during fetching:\n"
            self.message += "\n".join((
                msg.format(i + 1, err.__class__.__name__, str(err))
                for (i, err) in enumerate(errors)
            ))
        else:
            err = errors[0]
            self.message = "{0}: {1}".format(err.__class__.__name__, str(err))
        super(FetchCacheError, self).__init__(self.message)


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
        self._index_contents_key = 'contents.json'

        # a FileCache instance storing copies of remote binary cache indices
        self._index_file_cache = None

        # stores a map of mirror URL to index hash and cache key (index path)
        self._local_index_cache = None

        # hashes of remote indices already ingested into the concrete spec
        # cache (_mirrors_for_spec)
        self._specs_already_associated = set()

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
            self._index_file_cache = file_cache.FileCache(
                self._index_cache_root)

            cache_key = self._index_contents_key
            self._index_file_cache.init_entry(cache_key)

            cache_path = self._index_file_cache.cache_path(cache_key)

            self._local_index_cache = {}
            if os.path.isfile(cache_path):
                with self._index_file_cache.read_transaction(
                        cache_key) as cache_file:
                    self._local_index_cache = json.load(cache_file)

    def clear(self):
        """ For testing purposes we need to be able to empty the cache and
        clear associated data structures. """
        if self._index_file_cache:
            self._index_file_cache.destroy()
            self._index_file_cache = None
        self._local_index_cache = None
        self._specs_already_associated = set()
        self._mirrors_for_spec = {}

    def _write_local_index_cache(self):
        self._init_local_index_cache()
        cache_key = self._index_contents_key
        with self._index_file_cache.write_transaction(cache_key) as (old, new):
            json.dump(self._local_index_cache, new)

    def regenerate_spec_cache(self, clear_existing=False):
        """ Populate the local cache of concrete specs (``_mirrors_for_spec``)
        from the locally cached buildcache index files.  This is essentially a
        no-op if it has already been done, as we keep track of the index
        hashes for which we have already associated the built specs. """
        self._init_local_index_cache()

        if clear_existing:
            self._specs_already_associated = set()
            self._mirrors_for_spec = {}

        for mirror_url in self._local_index_cache:
            cache_entry = self._local_index_cache[mirror_url]
            cached_index_path = cache_entry['index_path']
            cached_index_hash = cache_entry['index_hash']
            if cached_index_hash not in self._specs_already_associated:
                self._associate_built_specs_with_mirror(cached_index_path,
                                                        mirror_url)
                self._specs_already_associated.add(cached_index_hash)

    def _associate_built_specs_with_mirror(self, cache_key, mirror_url):
        tmpdir = tempfile.mkdtemp()

        try:
            db_root_dir = os.path.join(tmpdir, 'db_root')
            db = spack_db.Database(None, db_dir=db_root_dir,
                                   enable_transaction_locking=False)

            self._index_file_cache.init_entry(cache_key)
            cache_path = self._index_file_cache.cache_path(cache_key)
            with self._index_file_cache.read_transaction(cache_key):
                db._read_from_file(cache_path)

            spec_list = db.query_local(installed=False, in_buildcache=True)

            for indexed_spec in spec_list:
                dag_hash = indexed_spec.dag_hash()
                full_hash = indexed_spec._full_hash

                if dag_hash not in self._mirrors_for_spec:
                    self._mirrors_for_spec[dag_hash] = []

                for entry in self._mirrors_for_spec[dag_hash]:
                    # A binary mirror can only have one spec per DAG hash, so
                    # if we already have an entry under this DAG hash for this
                    # mirror url, we may need to replace the spec associated
                    # with it (but only if it has a different full_hash).
                    if entry['mirror_url'] == mirror_url:
                        if full_hash and full_hash != entry['spec']._full_hash:
                            entry['spec'] = indexed_spec
                        break
                else:
                    self._mirrors_for_spec[dag_hash].append({
                        "mirror_url": mirror_url,
                        "spec": indexed_spec,
                    })
        finally:
            shutil.rmtree(tmpdir)

    def get_all_built_specs(self):
        spec_list = []
        for dag_hash in self._mirrors_for_spec:
            # in the absence of further information, all concrete specs
            # with the same DAG hash are equivalent, so we can just
            # return the first one in the list.
            if len(self._mirrors_for_spec[dag_hash]) > 0:
                spec_list.append(self._mirrors_for_spec[dag_hash][0]['spec'])

        return spec_list

    def find_built_spec(self, spec):
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
        self.regenerate_spec_cache()
        return self.find_by_hash(spec.dag_hash())

    def find_by_hash(self, find_hash):
        """Same as find_built_spec but uses the hash of a spec.

        Args:
            find_hash (str): hash of the spec to search
        """
        if find_hash not in self._mirrors_for_spec:
            return None
        return self._mirrors_for_spec[find_hash]

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
                    if new_entry['mirror_url'] == cur_entry['mirror_url']:
                        cur_entry['spec'] = new_entry['spec']
                        break
                else:
                    current_list.append = {
                        'mirror_url': new_entry['mirror_url'],
                        'spec': new_entry['spec'],
                    }

    def update(self):
        """ Make sure local cache of buildcache index files is up to date.
        If the same mirrors are configured as the last time this was called
        and none of the remote buildcache indices have changed, calling this
        method will only result in fetching the index hash from each mirror
        to confirm it is the same as what is stored locally.  Otherwise, the
        buildcache ``index.json`` and ``index.json.hash`` files are retrieved
        from each configured mirror and stored locally (both in memory and
        on disk under ``_index_cache_root``). """
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

        for cached_mirror_url in self._local_index_cache:
            cache_entry = self._local_index_cache[cached_mirror_url]
            cached_index_hash = cache_entry['index_hash']
            cached_index_path = cache_entry['index_path']
            if cached_mirror_url in configured_mirror_urls:
                # May need to fetch the index and update the local caches
                try:
                    needs_regen = self._fetch_and_cache_index(
                        cached_mirror_url, expect_hash=cached_index_hash)
                    all_methods_failed = False
                except FetchCacheError as fetch_error:
                    needs_regen = False
                    fetch_errors.extend(fetch_error.errors)
                # The need to regenerate implies a need to clear as well.
                spec_cache_clear_needed |= needs_regen
                spec_cache_regenerate_needed |= needs_regen
            else:
                # No longer have this mirror, cached index should be removed
                items_to_remove.append({
                    'url': cached_mirror_url,
                    'cache_key': os.path.join(self._index_cache_root,
                                              cached_index_path)
                })
                spec_cache_clear_needed = True
                spec_cache_regenerate_needed = True

        # Clean up items to be removed, identified above
        for item in items_to_remove:
            url = item['url']
            cache_key = item['cache_key']
            self._index_file_cache.remove(cache_key)
            del self._local_index_cache[url]

        # Iterate the configured mirrors now.  Any mirror urls we do not
        # already have in our cache must be fetched, stored, and represented
        # locally.
        for mirror_url in configured_mirror_urls:
            if mirror_url not in self._local_index_cache:
                # Need to fetch the index and update the local caches
                try:
                    needs_regen = self._fetch_and_cache_index(mirror_url)
                    all_methods_failed = False
                except FetchCacheError as fetch_error:
                    fetch_errors.extend(fetch_error.errors)
                    needs_regen = False
                # Generally speaking, a new mirror wouldn't imply the need to
                # clear the spec cache, so leave it as is.
                if needs_regen:
                    spec_cache_regenerate_needed = True

        self._write_local_index_cache()

        if all_methods_failed:
            raise FetchCacheError(fetch_errors)
        elif spec_cache_regenerate_needed:
            self.regenerate_spec_cache(clear_existing=spec_cache_clear_needed)

    def _fetch_and_cache_index(self, mirror_url, expect_hash=None):
        """ Fetch a buildcache index file from a remote mirror and cache it.

        If we already have a cached index from this mirror, then we first
        check if the hash has changed, and we avoid fetching it if not.

        Args:
            mirror_url (str): Base url of mirror
            expect_hash (str): If provided, this hash will be compared against
                the index hash we retrieve from the mirror, to determine if we
                need to fetch the index or not.

        Returns:
            True if this function thinks the concrete spec cache,
                ``_mirrors_for_spec``, should be regenerated.  Returns False
                otherwise.
        Throws:
            FetchCacheError: a composite exception.
        """
        index_fetch_url = url_util.join(
            mirror_url, _build_cache_relative_path, 'index.json')
        hash_fetch_url = url_util.join(
            mirror_url, _build_cache_relative_path, 'index.json.hash')

        old_cache_key = None
        fetched_hash = None

        errors = []

        # Fetch the hash first so we can check if we actually need to fetch
        # the index itself.
        try:
            _, _, fs = web_util.read_from_url(hash_fetch_url)
            fetched_hash = codecs.getreader('utf-8')(fs).read()
        except (URLError, web_util.SpackWebError) as url_err:
            errors.append(
                RuntimeError("Unable to read index hash {0} due to {1}: {2}".format(
                    hash_fetch_url, url_err.__class__.__name__, str(url_err)
                ))
            )

        # The only case where we'll skip attempting to fetch the buildcache
        # index from the mirror is when we already have a hash for this
        # mirror, we were able to retrieve one from the mirror, and
        # the two hashes are the same.
        if expect_hash and fetched_hash:
            if fetched_hash == expect_hash:
                tty.debug('Cached index for {0} already up to date'.format(
                    mirror_url))
                return False
            else:
                # We expected a hash, we fetched a hash, and they were not the
                # same.  If we end up fetching an index successfully and
                # replacing our entry for this mirror, we should clean up the
                # existing cache file
                if mirror_url in self._local_index_cache:
                    existing_entry = self._local_index_cache[mirror_url]
                    old_cache_key = existing_entry['index_path']

        tty.debug('Fetching index from {0}'.format(index_fetch_url))

        # Fetch index itself
        try:
            _, _, fs = web_util.read_from_url(index_fetch_url)
            index_object_str = codecs.getreader('utf-8')(fs).read()
        except (URLError, web_util.SpackWebError) as url_err:
            errors.append(
                RuntimeError("Unable to read index {0} due to {1}: {2}".format(
                    index_fetch_url, url_err.__class__.__name__, str(url_err)
                ))
            )
            raise FetchCacheError(errors)

        locally_computed_hash = compute_hash(index_object_str)

        if fetched_hash is not None and locally_computed_hash != fetched_hash:
            msg = ('Computed hash ({0}) did not match remote ({1}), '
                   'indicating error in index transmission').format(
                       locally_computed_hash, expect_hash)
            errors.append(RuntimeError(msg))
            # We somehow got an index that doesn't match the remote one, maybe
            # the next time we try we'll be successful.
            raise FetchCacheError(errors)

        url_hash = compute_hash(mirror_url)

        cache_key = '{0}_{1}.json'.format(
            url_hash[:10], locally_computed_hash[:10])
        self._index_file_cache.init_entry(cache_key)
        with self._index_file_cache.write_transaction(cache_key) as (old, new):
            new.write(index_object_str)

        self._local_index_cache[mirror_url] = {
            'index_hash': locally_computed_hash,
            'index_path': cache_key,
        }

        # clean up the old cache_key if necessary
        if old_cache_key:
            self._index_file_cache.remove(old_cache_key)

        # We fetched an index and updated the local index cache, we should
        # regenerate the spec cache as a result.
        return True


def binary_index_location():
    """Set up a BinaryCacheIndex for remote buildcache dbs in the user's homedir."""
    cache_root = os.path.join(misc_cache_location(), 'indices')
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


def compute_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


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
    with open(filename, 'r') as inputfile:
        content = inputfile.read()
        buildinfo = yaml.load(content)
    return buildinfo


def get_buildfile_manifest(spec):
    """
    Return a data structure with information about a build, including
    text_to_relocate, binary_to_relocate, binary_to_relocate_fullpath
    link_to_relocate, and other, which means it doesn't fit any of previous
    checks (and should not be relocated). We blacklist docs (man) and
    metadata (.spack). This can be used to find a particular kind of file
    in spack, or to generate the build metadata.
    """
    data = {"text_to_relocate": [], "binary_to_relocate": [],
            "link_to_relocate": [], "other": [],
            "binary_to_relocate_fullpath": []}

    blacklist = (".spack", "man")

    # Do this at during tarball creation to save time when tarball unpacked.
    # Used by make_package_relative to determine binaries to change.
    for root, dirs, files in os.walk(spec.prefix, topdown=True):
        dirs[:] = [d for d in dirs if d not in blacklist]

        # Directories may need to be relocated too.
        for directory in dirs:
            dir_path_name = os.path.join(root, directory)
            rel_path_name = os.path.relpath(dir_path_name, spec.prefix)
            if os.path.islink(dir_path_name):
                link = os.readlink(dir_path_name)
                if os.path.isabs(link) and link.startswith(spack.store.layout.root):
                    data['link_to_relocate'].append(rel_path_name)

        for filename in files:
            path_name = os.path.join(root, filename)
            m_type, m_subtype = relocate.mime_type(path_name)
            rel_path_name = os.path.relpath(path_name, spec.prefix)
            added = False

            if os.path.islink(path_name):
                link = os.readlink(path_name)
                if os.path.isabs(link):
                    # Relocate absolute links into the spack tree
                    if link.startswith(spack.store.layout.root):
                        data['link_to_relocate'].append(rel_path_name)
                    added = True

            if relocate.needs_binary_relocation(m_type, m_subtype):
                if ((m_subtype in ('x-executable', 'x-sharedlib', 'x-pie-executable')
                    and sys.platform != 'darwin') or
                   (m_subtype in ('x-mach-binary')
                    and sys.platform == 'darwin') or
                   (not filename.endswith('.o'))):
                    data['binary_to_relocate'].append(rel_path_name)
                    data['binary_to_relocate_fullpath'].append(path_name)
                    added = True

            if relocate.needs_text_relocation(m_type, m_subtype):
                data['text_to_relocate'].append(rel_path_name)
                added = True

            if not added:
                data['other'].append(path_name)
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
    for d in deps:
        prefix_to_hash[str(d.prefix)] = d.dag_hash()

    # Create buildinfo data and write it to disk
    buildinfo = {}
    buildinfo['sbang_install_path'] = spack.hooks.sbang.sbang_install_path()
    buildinfo['relative_rpaths'] = rel
    buildinfo['buildpath'] = spack.store.layout.root
    buildinfo['spackprefix'] = spack.paths.prefix
    buildinfo['relative_prefix'] = os.path.relpath(
        spec.prefix, spack.store.layout.root)
    buildinfo['relocate_textfiles'] = manifest['text_to_relocate']
    buildinfo['relocate_binaries'] = manifest['binary_to_relocate']
    buildinfo['relocate_links'] = manifest['link_to_relocate']
    buildinfo['prefix_to_hash'] = prefix_to_hash
    filename = buildinfo_file_name(workdir)
    with open(filename, 'w') as outfile:
        outfile.write(syaml.dump(buildinfo, default_flow_style=True))


def tarball_directory_name(spec):
    """
    Return name of the tarball directory according to the convention
    <os>-<architecture>/<compiler>/<package>-<version>/
    """
    return "%s/%s/%s-%s" % (spec.architecture,
                            str(spec.compiler).replace("@", "-"),
                            spec.name, spec.version)


def tarball_name(spec, ext):
    """
    Return the name of the tarfile according to the convention
    <os>-<architecture>-<package>-<dag_hash><ext>
    """
    return "%s-%s-%s-%s-%s%s" % (spec.architecture,
                                 str(spec.compiler).replace("@", "-"),
                                 spec.name,
                                 spec.version,
                                 spec.dag_hash(),
                                 ext)


def tarball_path_name(spec, ext):
    """
    Return the full path+name for a given spec according to the convention
    <tarball_directory_name>/<tarball_name>
    """
    return os.path.join(tarball_directory_name(spec),
                        tarball_name(spec, ext))


def checksum_tarball(file):
    # calculate sha256 hash of tar file
    block_size = 65536
    hasher = hashlib.sha256()
    with open(file, 'rb') as tfile:
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
                " to create a default key.")
    return key


def sign_tarball(key, force, specfile_path):
    if os.path.exists('%s.sig' % specfile_path):
        if force:
            os.remove('%s.sig' % specfile_path)
        else:
            raise NoOverwriteException('%s.sig' % specfile_path)

    key = select_signing_key(key)
    spack.util.gpg.sign(key, specfile_path, '%s.sig' % specfile_path, clearsign=True)


def generate_package_index(cache_prefix):
    """Create the build cache index page.

    Creates (or replaces) the "index.json" page at the location given in
    cache_prefix.  This page contains a link for each binary package (.yaml or
    .json) under cache_prefix.
    """
    try:
        file_list = (
            entry
            for entry in web_util.list_url(cache_prefix)
            if entry.endswith('.yaml') or entry.endswith('spec.json'))
    except KeyError as inst:
        msg = 'No packages at {0}: {1}'.format(cache_prefix, inst)
        tty.warn(msg)
        return
    except Exception as err:
        # If we got some kind of S3 (access denied or other connection
        # error), the first non boto-specific class in the exception
        # hierarchy is Exception.  Just print a warning and return
        msg = 'Encountered problem listing packages at {0}: {1}'.format(
            cache_prefix, err)
        tty.warn(msg)
        return

    tty.debug('Retrieving spec descriptor files from {0} to build index'.format(
        cache_prefix))

    all_mirror_specs = {}

    for file_path in file_list:
        try:
            spec_url = url_util.join(cache_prefix, file_path)
            tty.debug('fetching {0}'.format(spec_url))
            _, _, spec_file = web_util.read_from_url(spec_url)
            spec_file_contents = codecs.getreader('utf-8')(spec_file).read()
            # Need full spec.json name or this gets confused with index.json.
            if spec_url.endswith('.json'):
                spec_dict = sjson.load(spec_file_contents)
                s = Spec.from_json(spec_file_contents)
            elif spec_url.endswith('.yaml'):
                spec_dict = syaml.load(spec_file_contents)
                s = Spec.from_yaml(spec_file_contents)
            all_mirror_specs[s.dag_hash()] = {
                'spec_url': spec_url,
                'spec': s,
                'num_deps': len(list(s.traverse(root=False))),
                'binary_cache_checksum': spec_dict['binary_cache_checksum'],
                'buildinfo': spec_dict['buildinfo'],
            }
        except (URLError, web_util.SpackWebError) as url_err:
            tty.error('Error reading specfile: {0}'.format(file_path))
            tty.error(url_err)

    sorted_specs = sorted(all_mirror_specs.keys(),
                          key=lambda k: all_mirror_specs[k]['num_deps'])

    tmpdir = tempfile.mkdtemp()
    db_root_dir = os.path.join(tmpdir, 'db_root')
    db = spack_db.Database(None, db_dir=db_root_dir,
                           enable_transaction_locking=False,
                           record_fields=['spec', 'ref_count', 'in_buildcache'])

    try:
        tty.debug('Specs sorted by number of dependencies:')
        for dag_hash in sorted_specs:
            spec_record = all_mirror_specs[dag_hash]
            s = spec_record['spec']
            num_deps = spec_record['num_deps']
            tty.debug('  {0}/{1} -> {2}'.format(
                s.name, dag_hash[:7], num_deps))
            if num_deps > 0:
                # Check each of this spec's dependencies (which we have already
                # processed), as they are the source of truth for their own
                # full hash.  If the full hash we have for any deps does not
                # match what those deps have themselves, then we need to splice
                # this spec with those deps, and push this spliced spec
                # (spec.json file) back to the mirror, as well as update the
                # all_mirror_specs dictionary with this spliced spec.
                to_splice = []
                for dep in s.dependencies():
                    dep_dag_hash = dep.dag_hash()
                    if dep_dag_hash in all_mirror_specs:
                        true_dep = all_mirror_specs[dep_dag_hash]['spec']
                        if true_dep.full_hash() != dep.full_hash():
                            to_splice.append(true_dep)

                if to_splice:
                    tty.debug('    needs the following deps spliced:')
                    for true_dep in to_splice:
                        tty.debug('      {0}/{1}'.format(
                            true_dep.name, true_dep.dag_hash()[:7]))
                        s = s.splice(true_dep, True)

                    # Push this spliced spec back to the mirror
                    spliced_spec_dict = s.to_dict(hash=ht.full_hash)
                    for key in ['binary_cache_checksum', 'buildinfo']:
                        spliced_spec_dict[key] = spec_record[key]

                    temp_json_path = os.path.join(tmpdir, 'spliced.spec.json')
                    with open(temp_json_path, 'w') as fd:
                        fd.write(sjson.dump(spliced_spec_dict))

                    spliced_spec_url = spec_record['spec_url']
                    web_util.push_to_url(
                        temp_json_path, spliced_spec_url, keep_original=False)
                    tty.debug('    spliced and wrote {0}'.format(
                        spliced_spec_url))
                    spec_record['spec'] = s

            db.add(s, None)
            db.mark(s, 'in_buildcache', True)

        # Now that we have fixed any old specfiles that might have had the wrong
        # full hash for their dependencies, we can generate the index, compute
        # the hash, and push those files to the mirror.
        index_json_path = os.path.join(db_root_dir, 'index.json')
        with open(index_json_path, 'w') as f:
            db._write_to_file(f)

        # Read the index back in and compute it's hash
        with open(index_json_path) as f:
            index_string = f.read()
            index_hash = compute_hash(index_string)

        # Write the hash out to a local file
        index_hash_path = os.path.join(db_root_dir, 'index.json.hash')
        with open(index_hash_path, 'w') as f:
            f.write(index_hash)

        # Push the index itself
        web_util.push_to_url(
            index_json_path,
            url_util.join(cache_prefix, 'index.json'),
            keep_original=False,
            extra_args={'ContentType': 'application/json'})

        # Push the hash
        web_util.push_to_url(
            index_hash_path,
            url_util.join(cache_prefix, 'index.json.hash'),
            keep_original=False,
            extra_args={'ContentType': 'text/plain'})
    except Exception as err:
        msg = 'Encountered problem pushing package index to {0}: {1}'.format(
            cache_prefix, err)
        tty.warn(msg)
        tty.debug('\n' + traceback.format_exc())
    finally:
        shutil.rmtree(tmpdir)


def generate_key_index(key_prefix, tmpdir=None):
    """Create the key index page.

    Creates (or replaces) the "index.json" page at the location given in
    key_prefix.  This page contains an entry for each key (.pub) under
    key_prefix.
    """

    tty.debug(' '.join(('Retrieving key.pub files from',
                        url_util.format(key_prefix),
                        'to build key index')))

    try:
        fingerprints = (
            entry[:-4]
            for entry in web_util.list_url(key_prefix, recursive=False)
            if entry.endswith('.pub'))
    except KeyError as inst:
        msg = 'No keys at {0}: {1}'.format(key_prefix, inst)
        tty.warn(msg)
        return
    except Exception as err:
        # If we got some kind of S3 (access denied or other connection
        # error), the first non boto-specific class in the exception
        # hierarchy is Exception.  Just print a warning and return
        msg = 'Encountered problem listing keys at {0}: {1}'.format(
            key_prefix, err)
        tty.warn(msg)
        return

    remove_tmpdir = False

    keys_local = url_util.local_file_path(key_prefix)
    if keys_local:
        target = os.path.join(keys_local, 'index.json')
    else:
        if not tmpdir:
            tmpdir = tempfile.mkdtemp()
            remove_tmpdir = True
        target = os.path.join(tmpdir, 'index.json')

    index = {
        'keys': dict(
            (fingerprint, {}) for fingerprint
            in sorted(set(fingerprints)))
    }
    with open(target, 'w') as f:
        sjson.dump(index, f)

    if not keys_local:
        try:
            web_util.push_to_url(
                target,
                url_util.join(key_prefix, 'index.json'),
                keep_original=False,
                extra_args={'ContentType': 'application/json'})
        except Exception as err:
            msg = 'Encountered problem pushing key index to {0}: {1}'.format(
                key_prefix, err)
            tty.warn(msg)
        finally:
            if remove_tmpdir:
                shutil.rmtree(tmpdir)


def _build_tarball(
        spec, outdir,
        force=False, relative=False, unsigned=False,
        allow_root=False, key=None, regenerate_index=False
):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).
    """
    if not spec.concrete:
        raise ValueError('spec must be concrete to build tarball')

    # set up some paths
    tmpdir = tempfile.mkdtemp()
    cache_prefix = build_cache_prefix(tmpdir)

    tarfile_name = tarball_name(spec, '.spack')
    tarfile_dir = os.path.join(cache_prefix, tarball_directory_name(spec))
    tarfile_path = os.path.join(tarfile_dir, tarfile_name)
    spackfile_path = os.path.join(
        cache_prefix, tarball_path_name(spec, '.spack'))

    remote_spackfile_path = url_util.join(
        outdir, os.path.relpath(spackfile_path, tmpdir))

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
    specfile_name = tarball_name(spec, '.spec.json')
    specfile_path = os.path.realpath(os.path.join(cache_prefix, specfile_name))
    deprecated_specfile_path = specfile_path.replace('.spec.json', '.spec.yaml')

    remote_specfile_path = url_util.join(
        outdir, os.path.relpath(specfile_path, os.path.realpath(tmpdir)))
    remote_specfile_path_deprecated = url_util.join(
        outdir, os.path.relpath(deprecated_specfile_path,
                                os.path.realpath(tmpdir)))

    # If force and exists, overwrite. Otherwise raise exception on collision.
    if force:
        if web_util.url_exists(remote_specfile_path):
            web_util.remove_url(remote_specfile_path)
        if web_util.url_exists(remote_specfile_path_deprecated):
            web_util.remove_url(remote_specfile_path_deprecated)
    elif (web_util.url_exists(remote_specfile_path) or
            web_util.url_exists(remote_specfile_path_deprecated)):
        raise NoOverwriteException(url_util.format(remote_specfile_path))

    # make a copy of the install directory to work with
    workdir = os.path.join(tmpdir, os.path.basename(spec.prefix))
    # install_tree copies hardlinks
    # create a temporary tarfile from prefix and exract it to workdir
    # tarfile preserves hardlinks
    temp_tarfile_name = tarball_name(spec, '.tar')
    temp_tarfile_path = os.path.join(tarfile_dir, temp_tarfile_name)
    with closing(tarfile.open(temp_tarfile_path, 'w')) as tar:
        tar.add(name='%s' % spec.prefix,
                arcname='.')
    with closing(tarfile.open(temp_tarfile_path, 'r')) as tar:
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
    with closing(tarfile.open(tarfile_path, 'w:gz')) as tar:
        tar.add(name='%s' % workdir,
                arcname='%s' % os.path.basename(spec.prefix))
    # remove copy of install directory
    shutil.rmtree(workdir)

    # get the sha256 checksum of the tarball
    checksum = checksum_tarball(tarfile_path)

    # add sha256 checksum to spec.json

    with open(spec_file, 'r') as inputfile:
        content = inputfile.read()
        if spec_file.endswith('.yaml'):
            spec_dict = yaml.load(content)
        elif spec_file.endswith('.json'):
            spec_dict = sjson.load(content)
        else:
            raise ValueError(
                '{0} not a valid spec file type (json or yaml)'.format(
                    spec_file))
    spec_dict['buildcache_layout_version'] = 1
    bchecksum = {}
    bchecksum['hash_algorithm'] = 'sha256'
    bchecksum['hash'] = checksum
    spec_dict['binary_cache_checksum'] = bchecksum
    # Add original install prefix relative to layout root to spec.json.
    # This will be used to determine is the directory layout has changed.
    buildinfo = {}
    buildinfo['relative_prefix'] = os.path.relpath(
        spec.prefix, spack.store.layout.root)
    buildinfo['relative_rpaths'] = relative
    spec_dict['buildinfo'] = buildinfo

    with open(specfile_path, 'w') as outfile:
        outfile.write(sjson.dump(spec_dict))

    # sign the tarball and spec file with gpg
    if not unsigned:
        key = select_signing_key(key)
        sign_tarball(key, force, specfile_path)

    # push tarball and signed spec json to remote mirror
    web_util.push_to_url(
        spackfile_path, remote_spackfile_path, keep_original=False)
    web_util.push_to_url(
        '%s.sig' % specfile_path, '%s.sig' % remote_specfile_path, keep_original=False)

    tty.debug('Buildcache for "{0}" written to \n {1}'
              .format(spec, remote_spackfile_path))

    try:
        # push the key to the build cache's _pgp directory so it can be
        # imported
        if not unsigned:
            push_keys(outdir,
                      keys=[key],
                      regenerate_index=regenerate_index,
                      tmpdir=tmpdir)

        # create an index.json for the build_cache directory so specs can be
        # found
        if regenerate_index:
            generate_package_index(url_util.join(
                outdir, os.path.relpath(cache_prefix, tmpdir)))
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
            nodes = [n for n in current_spec.traverse(
                order='post', root=include_root, deptype=('link', 'run')
            )]

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
    specs_kwargs = specs_kwargs or {'include_root': True, 'include_dependencies': True}
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
        specfile_path (string): Path to file to be verified.

    Returns:
        ``True`` if the signature could be verified, ``False`` otherwise.
    """
    if not specfile_path:
        return False

    suppress = config.get('config:suppress_gpg_warnings', False)

    try:
        spack.util.gpg.verify(specfile_path, suppress_warnings=suppress)
    except Exception:
        return False

    return True


def try_fetch(url_to_fetch):
    """Utility function to try and fetch a file from a url, stage it
    locally, and return the path to the staged file.

    Args:
        url_to_fetch (string): Url pointing to remote resource to fetch

    Returns:
        Path to locally staged resource or ``None`` if it could not be fetched.
    """
    stage = Stage(url_to_fetch, keep=True)
    stage.create()

    try:
        stage.fetch()
    except fs.FetchError:
        return None

    return stage.save_filename


def download_tarball(spec, unsigned, mirrors_for_spec=None):
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
           "verify_requested": "true-if-not-unsigned",
           "verfied": "true-if-binary-pkg-was-already-verified"
       }
    """
    if not spack.mirror.MirrorCollection():
        tty.die("Please add a spack mirror to allow " +
                "download of pre-compiled packages.")

    tarball = tarball_path_name(spec, '.spack')
    specfile_prefix = tarball_name(spec, '.spec')

    mirrors_to_try = []

    try_first = [i['mirror_url'] for i in mirrors_for_spec]
    try_next = [
        i.fetch_url for i in spack.mirror.MirrorCollection().values()
        if i.fetch_url not in try_first
    ]

    for url in try_first + try_next:
        mirrors_to_try.append({
            'specfile': url_util.join(url,
                                      _build_cache_relative_path, specfile_prefix),
            'spackfile': url_util.join(url,
                                       _build_cache_relative_path, tarball)
        })

    tried_to_verify_sigs = []

    # Assumes we care more about finding a spec file by preferred ext
    # than by mirrory priority.  This can be made less complicated as
    # we remove support for deprecated spec formats and buildcache layouts.
    for ext in ['json.sig', 'json', 'yaml']:
        for mirror_to_try in mirrors_to_try:
            specfile_url = '{0}.{1}'.format(mirror_to_try['specfile'], ext)
            spackfile_url = mirror_to_try['spackfile']
            local_specfile_path = try_fetch(specfile_url)
            if local_specfile_path:
                signature_verified = False

                if ext.endswith('.sig') and not unsigned:
                    tried_to_verify_sigs.append(specfile_url)
                    signature_verified = try_verify(local_specfile_path)
                    if not signature_verified:
                        tty.warn("Failed to verify: {0}".format(specfile_url))

                if unsigned or signature_verified:
                    tarball_path = try_fetch(spackfile_url)
                    if tarball_path:
                        if signature_verified:
                            pass
                            # TODO: If we already verified the signature, then we have
                            # TODO: the new layout here and we will find the tarball
                            # TODO: checksum within the data we extract from the
                            # TODO: clearsigned file.  In this case, before claiming
                            # TODO: victory (that the package is completely verified),
                            # TODO: we must first compare that checksum to one we
                            # TODO: compute of the locally downloaded tarball.
                        return {
                            'tarball_path': tarball_path,
                            'specfile_path': local_specfile_path,
                        }

    if tried_to_verify_sigs:
        raise NoVerifyException(("Spack found new style signed binary packages"
                                 ", but was unable to verify any of them"))

    tty.warn("download_tarball() was unable to download " +
             "{0} from any configured mirrors".format(spec))
    return None


def make_package_relative(workdir, spec, allow_root):
    """
    Change paths in binaries to relative paths. Change absolute symlinks
    to relative symlinks.
    """
    prefix = spec.prefix
    buildinfo = read_buildinfo_file(workdir)
    old_layout_root = buildinfo['buildpath']
    orig_path_names = list()
    cur_path_names = list()
    for filename in buildinfo['relocate_binaries']:
        orig_path_names.append(os.path.join(prefix, filename))
        cur_path_names.append(os.path.join(workdir, filename))

    platform = spack.platforms.by_name(spec.platform)
    if 'macho' in platform.binary_formats:
        relocate.make_macho_binaries_relative(
            cur_path_names, orig_path_names, old_layout_root)

    if 'elf' in platform.binary_formats:
        relocate.make_elf_binaries_relative(
            cur_path_names, orig_path_names, old_layout_root)

    relocate.raise_if_not_relocatable(cur_path_names, allow_root)
    orig_path_names = list()
    cur_path_names = list()
    for linkname in buildinfo.get('relocate_links', []):
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
    for filename in buildinfo['relocate_binaries']:
        cur_path_names.append(os.path.join(workdir, filename))
    relocate.raise_if_not_relocatable(cur_path_names, allow_root)


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
    if 'sbang_install_path' in buildinfo:
        old_sbang_install_path = str(buildinfo['sbang_install_path'])
    old_layout_root = str(buildinfo['buildpath'])
    old_spack_prefix = str(buildinfo.get('spackprefix'))
    old_rel_prefix = buildinfo.get('relative_prefix')
    old_prefix = os.path.join(old_layout_root, old_rel_prefix)
    rel = buildinfo.get('relative_rpaths')
    prefix_to_hash = buildinfo.get('prefix_to_hash', None)
    if (old_rel_prefix != new_rel_prefix and not prefix_to_hash):
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
    hash_to_prefix[spec.format('{hash}')] = str(spec.package.prefix)
    new_deps = spack.build_environment.get_rpath_deps(spec.package)
    for d in new_deps:
        hash_to_prefix[d.format('{hash}')] = str(d.prefix)
    # Spurious replacements (e.g. sbang) will cause issues with binaries
    # For example, the new sbang can be longer than the old one.
    # Hence 2 dictionaries are maintained here.
    prefix_to_prefix_text = collections.OrderedDict()
    prefix_to_prefix_bin = collections.OrderedDict()

    if old_sbang_install_path:
        install_path = spack.hooks.sbang.sbang_install_path()
        prefix_to_prefix_text[old_sbang_install_path] = install_path

    prefix_to_prefix_text[old_prefix] = new_prefix
    prefix_to_prefix_bin[old_prefix] = new_prefix
    prefix_to_prefix_text[old_layout_root] = new_layout_root
    prefix_to_prefix_bin[old_layout_root] = new_layout_root
    for orig_prefix, hash in prefix_to_hash.items():
        prefix_to_prefix_text[orig_prefix] = hash_to_prefix.get(hash, None)
        prefix_to_prefix_bin[orig_prefix] = hash_to_prefix.get(hash, None)
    # This is vestigial code for the *old* location of sbang. Previously,
    # sbang was a bash script, and it lived in the spack prefix. It is
    # now a POSIX script that lives in the install prefix. Old packages
    # will have the old sbang location in their shebangs.
    orig_sbang = '#!/bin/bash {0}/bin/sbang'.format(old_spack_prefix)
    new_sbang = spack.hooks.sbang.sbang_shebang_line()
    prefix_to_prefix_text[orig_sbang] = new_sbang

    tty.debug("Relocating package from",
              "%s to %s." % (old_layout_root, new_layout_root))

    def is_backup_file(file):
        return file.endswith('~')

    # Text files containing the prefix text
    text_names = list()
    for filename in buildinfo['relocate_textfiles']:
        text_name = os.path.join(workdir, filename)
        # Don't add backup files generated by filter_file during install step.
        if not is_backup_file(text_name):
            text_names.append(text_name)

    # If we are not installing back to the same install tree do the relocation
    if old_prefix != new_prefix:
        files_to_relocate = [os.path.join(workdir, filename)
                             for filename in buildinfo.get('relocate_binaries')
                             ]
        # If the buildcache was not created with relativized rpaths
        # do the relocation of path in binaries
        platform = spack.platforms.by_name(spec.platform)
        if 'macho' in platform.binary_formats:
            relocate.relocate_macho_binaries(files_to_relocate,
                                             old_layout_root,
                                             new_layout_root,
                                             prefix_to_prefix_bin, rel,
                                             old_prefix,
                                             new_prefix)
        if 'elf' in platform.binary_formats:
            relocate.relocate_elf_binaries(files_to_relocate,
                                           old_layout_root,
                                           new_layout_root,
                                           prefix_to_prefix_bin, rel,
                                           old_prefix,
                                           new_prefix)
            # Relocate links to the new install prefix
            links = [link for link in buildinfo.get('relocate_links', [])]
            relocate.relocate_links(
                links, old_layout_root, old_prefix, new_prefix
            )

        # For all buildcaches
        # relocate the install prefixes in text files including dependencies
        relocate.relocate_text(text_names, prefix_to_prefix_text)

        paths_to_relocate = [old_prefix, old_layout_root]
        paths_to_relocate.extend(prefix_to_hash.keys())
        files_to_relocate = list(filter(
            lambda pathname: not relocate.file_is_relocatable(
                pathname, paths_to_relocate=paths_to_relocate),
            map(lambda filename: os.path.join(workdir, filename),
                buildinfo['relocate_binaries'])))
        # relocate the install prefixes in binary files including dependencies
        relocate.relocate_text_bin(files_to_relocate, prefix_to_prefix_bin)

    # If we are installing back to the same location
    # relocate the sbang location if the spack directory changed
    else:
        if old_spack_prefix != new_spack_prefix:
            relocate.relocate_text(text_names, prefix_to_prefix_text)


def _extract_inner_tarball(spec, filename, extract_to, unsigned, remote_checksum):
    extract_to = tempfile.mkdtemp()
    stagepath = os.path.dirname(filename)
    spackfile_name = tarball_name(spec, '.spack')
    spackfile_path = os.path.join(stagepath, spackfile_name)
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_path = os.path.join(extract_to, tarfile_name)
    deprecated_yaml_name = tarball_name(spec, '.spec.yaml')
    deprecated_yaml_path = os.path.join(extract_to, deprecated_yaml_name)
    json_name = tarball_name(spec, '.spec.json')
    json_path = os.path.join(extract_to, json_name)
    with closing(tarfile.open(spackfile_path, 'r')) as tar:
        tar.extractall(extract_to)
    # some buildcache tarfiles use bzip2 compression
    if not os.path.exists(tarfile_path):
        tarfile_name = tarball_name(spec, '.tar.bz2')
        tarfile_path = os.path.join(extract_to, tarfile_name)

    if os.path.exists(json_path):
        specfile_path = json_path
    elif os.path.exists(deprecated_yaml_path):
        specfile_path = deprecated_yaml_path
    else:
        raise ValueError('Cannot find spec file for {0}.'.format(extract_to))

    if not unsigned:
        if os.path.exists('%s.asc' % specfile_path):
            suppress = config.get('config:suppress_gpg_warnings', False)
            spack.util.gpg.verify(
                '%s.asc' % specfile_path, specfile_path, suppress)
        else:
            raise NoVerifyException(
                "Package spec file failed signature verification.\n"
                "Old style buildcache entry is missing .asc file.")
    # get the sha256 checksum of the tarball
    local_checksum = checksum_tarball(tarfile_path)

    # if the checksums don't match don't install
    if local_checksum != remote_checksum:
        raise NoChecksumException(
            "Package tarball failed checksum verification.\n"
            "It cannot be installed.")

    return tarfile_path


def extract_tarball(spec, download_result, allow_root=False, unsigned=False,
                    force=False):
    """
    extract binary tarball for given package into install area
    """
    if os.path.exists(spec.prefix):
        if force:
            shutil.rmtree(spec.prefix)
        else:
            raise NoOverwriteException(str(spec.prefix))

    specfile_path = download_result['specfile_path']

    with open(specfile_path, 'r') as inputfile:
        content = inputfile.read()
        if specfile_path.endswith('.json.sig'):
            spec_dict = Spec.extract_json_from_clearsig(content)
        elif specfile_path.endswith('.json'):
            spec_dict = sjson.load(content)
        else:
            spec_dict = syaml.load(content)

    filename = download_result['tarball_path']

    if ('buildcache_layout_version' not in spec_dict or
            int(spec_dict['buildcache_layout_version']) < 1):
        # Handle the older buildcache layout where the .spack file
        # contains a spec json/yaml, maybe an .asc file (signature),
        # and another tarball containing the actual install tree.
        tmpdir = tempfile.mkdtemp()
        bchecksum = spec_dict['binary_cache_checksum']
        try:
            tarfile_path = _extract_inner_tarball(
                spec, filename, tmpdir, bchecksum, unsigned)
        except Exception as e:
            shutil.rmtree(tmpdir)
            raise e
    else:
        # Newer buildcache layout: the .spack file contains just
        # in the install tree, the signature, if it exists, is
        # wrapped around the spec.json at the root.  If sig verify
        # was required, it was already done before downloading
        # the tarball.
        tarfile_path = filename

    new_relative_prefix = str(os.path.relpath(spec.prefix,
                                              spack.store.layout.root))
    # if the original relative prefix is in the spec file use it
    buildinfo = spec_dict.get('buildinfo', {})
    old_relative_prefix = buildinfo.get('relative_prefix', new_relative_prefix)
    rel = buildinfo.get('relative_rpaths')
    info = 'old relative prefix %s\nnew relative prefix %s\nrelative rpaths %s'
    tty.debug(info %
              (old_relative_prefix, new_relative_prefix, rel))

    # Extract the tarball into the store root, presumably on the same filesystem.
    # The directory created is the base directory name of the old prefix.
    # Moving the old prefix name to the new prefix location should preserve
    # hard links and symbolic links.
    extract_tmp = os.path.join(spack.store.layout.root, '.tmp')
    mkdirp(extract_tmp)
    extracted_dir = os.path.join(extract_tmp,
                                 old_relative_prefix.split(os.path.sep)[-1])

    with closing(tarfile.open(tarfile_path, 'r')) as tar:
        try:
            tar.extractall(path=extract_tmp)
        except Exception as e:
            shutil.rmtree(extracted_dir)
            raise e
    try:
        shutil.move(extracted_dir, spec.prefix)
    except Exception as e:
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
        manifest_file = os.path.join(spec.prefix,
                                     spack.store.layout.metadata_dir,
                                     spack.store.layout.manifest_file_name)
        if not os.path.exists(manifest_file):
            spec_id = spec.format('{name}/{hash:7}')
            tty.warn('No manifest file in tarball for spec %s' % spec_id)
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir)
        if os.path.exists(filename):
            os.remove(filename)


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
        msg = msg.format(download_result['tarball_path'], sha256)
        if not checker.check(download_result['tarball_path']):
            raise spack.binary_distribution.NoChecksumException(msg)
        tty.debug('Verified SHA256 checksum of the build cache')

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
    for node in spec.traverse(root=True, order='post', deptype=('link', 'run')):
        install_root_node(node, allow_root=allow_root, unsigned=unsigned, force=force)


def try_direct_fetch(spec, full_hash_match=False, mirrors=None):
    """
    Try to find the spec directly on the configured mirrors
    """
    deprecated_specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_name = tarball_name(spec, '.spec.json')
    signed_specfile_name = tarball_name(spec, '.spec.json.sig')
    specfile_is_signed = False
    specfile_is_json = True
    lenient = not full_hash_match
    found_specs = []
    spec_full_hash = spec.full_hash()

    for mirror in spack.mirror.MirrorCollection(mirrors=mirrors).values():
        buildcache_fetch_url_yaml = url_util.join(
            mirror.fetch_url, _build_cache_relative_path, deprecated_specfile_name)
        buildcache_fetch_url_json = url_util.join(
            mirror.fetch_url, _build_cache_relative_path, specfile_name)
        buildcache_fetch_url_signed_json = url_util.join(
            mirror.fetch_url, _build_cache_relative_path, signed_specfile_name)
        try:
            _, _, fs = web_util.read_from_url(buildcache_fetch_url_signed_json)
            specfile_is_signed = True
        except (URLError, web_util.SpackWebError, HTTPError) as url_err:
            try:
                _, _, fs = web_util.read_from_url(buildcache_fetch_url_json)
            except (URLError, web_util.SpackWebError, HTTPError) as url_err_x:
                try:
                    _, _, fs = web_util.read_from_url(buildcache_fetch_url_yaml)
                    specfile_is_json = False
                except (URLError, web_util.SpackWebError, HTTPError) as url_err_y:
                    tty.debug('Did not find {0} on {1}'.format(
                        specfile_name, buildcache_fetch_url_signed_json), url_err)
                    tty.debug('Did not find {0} on {1}'.format(
                        specfile_name, buildcache_fetch_url_json), url_err_x)
                    tty.debug('Did not find {0} on {1}'.format(
                        specfile_name, buildcache_fetch_url_yaml), url_err_y)
                    continue
        specfile_contents = codecs.getreader('utf-8')(fs).read()

        # read the spec from the build cache file. All specs in build caches
        # are concrete (as they are built) so we need to mark this spec
        # concrete on read-in.
        if specfile_is_signed:
            specfile_json = Spec.extract_json_from_clearsig(specfile_contents)
            fetched_spec = Spec.from_dict(specfile_json)
        elif specfile_is_json:
            fetched_spec = Spec.from_json(specfile_contents)
        else:
            fetched_spec = Spec.from_yaml(specfile_contents)
        fetched_spec._mark_concrete()

        # Do not recompute the full hash for the fetched spec, instead just
        # read the property.
        if lenient or fetched_spec._full_hash == spec_full_hash:
            found_specs.append({
                'mirror_url': mirror.fetch_url,
                'spec': fetched_spec,
            })

    return found_specs


def get_mirrors_for_spec(spec=None, full_hash_match=False,
                         mirrors_to_check=None, index_only=False):
    """
    Check if concrete spec exists on mirrors and return a list
    indicating the mirrors on which it can be found

    Args:
        spec (spack.spec.Spec): The spec to look for in binary mirrors
        full_hash_match (bool): If True, only includes mirrors where the spec
            full hash matches the locally computed full hash of the ``spec``
            argument.  If False, any mirror which has a matching DAG hash
            is included in the results.
        mirrors_to_check (dict): Optionally override the configured mirrors
            with the mirrors in this dictionary.
        index_only (bool): Do not attempt direct fetching of ``spec.json``
            files from remote mirrors, only consider the indices.

    Return:
        A list of objects, each containing a ``mirror_url`` and ``spec`` key
            indicating all mirrors where the spec can be found.
    """
    if spec is None:
        return []

    if not spack.mirror.MirrorCollection(mirrors=mirrors_to_check):
        tty.debug("No Spack mirrors are currently configured")
        return {}

    results = []
    lenient = not full_hash_match
    spec_full_hash = spec.full_hash()

    def filter_candidates(candidate_list):
        filtered_candidates = []
        for candidate in candidate_list:
            candidate_full_hash = candidate['spec']._full_hash
            if lenient or spec_full_hash == candidate_full_hash:
                filtered_candidates.append(candidate)
        return filtered_candidates

    candidates = binary_index.find_built_spec(spec)
    if candidates:
        results = filter_candidates(candidates)

    # Maybe we just didn't have the latest information from the mirror, so
    # try to fetch directly, unless we are only considering the indices.
    if not results and not index_only:
        results = try_direct_fetch(spec,
                                   full_hash_match=full_hash_match,
                                   mirrors=mirrors_to_check)

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
    """Get pgp public keys available on mirror with suffix .pub
    """
    mirror_collection = (mirrors or spack.mirror.MirrorCollection())

    if not mirror_collection:
        tty.die("Please add a spack mirror to allow " +
                "download of build caches.")

    for mirror in mirror_collection.values():
        fetch_url = mirror.fetch_url
        keys_url = url_util.join(fetch_url,
                                 _build_cache_relative_path,
                                 _build_cache_keys_relative_path)
        keys_index = url_util.join(keys_url, 'index.json')

        tty.debug('Finding public keys in {0}'.format(
            url_util.format(fetch_url)))

        try:
            _, _, json_file = web_util.read_from_url(keys_index)
            json_index = sjson.load(codecs.getreader('utf-8')(json_file))
        except (URLError, web_util.SpackWebError) as url_err:
            if web_util.url_exists(keys_index):
                err_msg = [
                    'Unable to find public keys in {0},',
                    ' caught exception attempting to read from {1}.',
                ]

                tty.error(''.join(err_msg).format(
                    url_util.format(fetch_url),
                    url_util.format(keys_index)))

                tty.debug(url_err)

            continue

        for fingerprint, key_attributes in json_index['keys'].items():
            link = os.path.join(keys_url, fingerprint + '.pub')

            with Stage(link, name="build_cache", keep=True) as stage:
                if os.path.exists(stage.save_filename) and force:
                    os.remove(stage.save_filename)
                if not os.path.exists(stage.save_filename):
                    try:
                        stage.fetch()
                    except fs.FetchError:
                        continue

            tty.debug('Found key {0}'.format(fingerprint))
            if install:
                if trust:
                    spack.util.gpg.trust(stage.save_filename)
                    tty.debug('Added this key to trusted keys.')
                else:
                    tty.debug('Will not add this key to trusted keys.'
                              'Use -t to install all downloaded keys')


def push_keys(*mirrors, **kwargs):
    """
    Upload pgp public keys to the given mirrors
    """
    keys = kwargs.get('keys')
    regenerate_index = kwargs.get('regenerate_index', False)
    tmpdir = kwargs.get('tmpdir')
    remove_tmpdir = False

    keys = spack.util.gpg.public_keys(*(keys or []))

    try:
        for mirror in mirrors:
            push_url = getattr(mirror, 'push_url', mirror)
            keys_url = url_util.join(push_url,
                                     _build_cache_relative_path,
                                     _build_cache_keys_relative_path)
            keys_local = url_util.local_file_path(keys_url)

            verb = 'Writing' if keys_local else 'Uploading'
            tty.debug('{0} public keys to {1}'.format(
                verb, url_util.format(push_url)))

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
                tty.debug('    ' + fingerprint)
                filename = fingerprint + '.pub'

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
                        export_target,
                        url_util.join(keys_url, filename),
                        keep_original=False)

            if regenerate_index:
                if keys_local:
                    generate_key_index(keys_url)
                else:
                    generate_key_index(keys_url, tmpdir)
    finally:
        if remove_tmpdir:
            shutil.rmtree(tmpdir)


def needs_rebuild(spec, mirror_url, rebuild_on_errors=False):
    if not spec.concrete:
        raise ValueError('spec must be concrete to check against mirror')

    pkg_name = spec.name
    pkg_version = spec.version

    pkg_hash = spec.dag_hash()
    pkg_full_hash = spec.full_hash()

    tty.debug('Checking {0}-{1}, dag_hash = {2}, full_hash = {3}'.format(
        pkg_name, pkg_version, pkg_hash, pkg_full_hash))
    tty.debug(spec.tree())

    # Try to retrieve the specfile directly, based on the known
    # format of the name, in order to determine if the package
    # needs to be rebuilt.
    cache_prefix = build_cache_prefix(mirror_url)
    specfile_is_json = True
    specfile_name = tarball_name(spec, '.spec.json')
    deprecated_specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = os.path.join(cache_prefix, specfile_name)
    deprecated_specfile_path = os.path.join(cache_prefix,
                                            deprecated_specfile_name)

    result_of_error = 'Package ({0}) will {1}be rebuilt'.format(
        spec.short_spec, '' if rebuild_on_errors else 'not ')

    try:
        _, _, spec_file = web_util.read_from_url(specfile_path)
    except (URLError, web_util.SpackWebError) as url_err:
        try:
            _, _, spec_file = web_util.read_from_url(deprecated_specfile_path)
            specfile_is_json = False
        except (URLError, web_util.SpackWebError) as url_err_y:
            err_msg = [
                'Unable to determine whether {0} needs rebuilding,',
                ' caught exception attempting to read from {1} or {2}.',
            ]
            tty.error(''.join(err_msg).format(
                spec.short_spec,
                specfile_path,
                deprecated_specfile_path))
            tty.debug(url_err)
            tty.debug(url_err_y)
            tty.warn(result_of_error)
            return rebuild_on_errors

    spec_file_contents = codecs.getreader('utf-8')(spec_file).read()
    if not spec_file_contents:
        tty.error('Reading {0} returned nothing'.format(
            specfile_path if specfile_is_json else deprecated_specfile_path))
        tty.warn(result_of_error)
        return rebuild_on_errors

    spec_dict = (sjson.load(spec_file_contents)
                 if specfile_is_json else syaml.load(spec_file_contents))

    try:
        nodes = spec_dict['spec']['nodes']
    except KeyError:
        # Prior node dict format omitted 'nodes' key
        nodes = spec_dict['spec']
    name = spec.name

    # In the old format:
    # The "spec" key represents a list of objects, each with a single
    # key that is the package name.  While the list usually just contains
    # a single object, we iterate over the list looking for the object
    # with the name of this concrete spec as a key, out of an abundance
    # of caution.
    # In format version 2:
    # ['spec']['nodes'] is still a list of objects, but with a
    # multitude of keys. The list will commonly contain many objects, and in the
    # case of build specs, it is highly likely that the same name will occur
    # once as the actual package, and then again as the build provenance of that
    # same package. Hence format version 2 matches on the dag hash, not name.
    if nodes and 'name' not in nodes[0]:
        # old style
        cached_pkg_specs = [item[name] for item in nodes if name in item]
    elif nodes and spec_dict['spec']['_meta']['version'] == 2:
        cached_pkg_specs = [item for item in nodes
                            if item[ht.dag_hash.name] == spec.dag_hash()]
    cached_target = cached_pkg_specs[0] if cached_pkg_specs else None

    # If either the full_hash didn't exist in the specfile, or it
    # did, but didn't match the one we computed locally, then we should
    # just rebuild.  This can be simplified once the dag_hash and the
    # full_hash become the same thing.
    rebuild = False

    if not cached_target:
        reason = 'did not find spec in specfile contents'
        rebuild = True
    elif ht.full_hash.name not in cached_target:
        reason = 'full_hash was missing from remote specfile'
        rebuild = True
    else:
        full_hash = cached_target[ht.full_hash.name]
        if full_hash != pkg_full_hash:
            reason = 'hash mismatch, remote = {0}, local = {1}'.format(
                full_hash, pkg_full_hash)
            rebuild = True

    if rebuild:
        tty.msg('Rebuilding {0}, reason: {1}'.format(
            spec.short_spec, reason))
        tty.msg(spec.tree())

    return rebuild


def check_specs_against_mirrors(mirrors, specs, output_file=None,
                                rebuild_on_errors=False):
    """Check all the given specs against buildcaches on the given mirrors and
    determine if any of the specs need to be rebuilt.  Reasons for needing to
    rebuild include binary cache for spec isn't present on a mirror, or it is
    present but the full_hash has changed since last time spec was built.

    Arguments:
        mirrors (dict): Mirrors to check against
        specs (typing.Iterable): Specs to check against mirrors
        output_file (str): Path to output file to be written.  If provided,
            mirrors with missing or out-of-date specs will be formatted as a
            JSON object and written to this file.
        rebuild_on_errors (bool): Treat any errors encountered while
            checking specs as a signal to rebuild package.

    Returns: 1 if any spec was out-of-date on any mirror, 0 otherwise.

    """
    rebuilds = {}
    for mirror in spack.mirror.MirrorCollection(mirrors).values():
        tty.debug('Checking for built specs at {0}'.format(mirror.fetch_url))

        rebuild_list = []

        for spec in specs:
            if needs_rebuild(spec, mirror.fetch_url, rebuild_on_errors):
                rebuild_list.append({
                    'short_spec': spec.short_spec,
                    'hash': spec.dag_hash()
                })

        if rebuild_list:
            rebuilds[mirror.fetch_url] = {
                'mirrorName': mirror.name,
                'mirrorUrl': mirror.fetch_url,
                'rebuildSpecs': rebuild_list
            }

    if output_file:
        with open(output_file, 'w') as outf:
            outf.write(json.dumps(rebuilds))

    return 1 if rebuilds else 0


def _download_buildcache_entry(mirror_root, descriptions):
    for description in descriptions:
        path = description['path']
        mkdirp(path)
        fail_if_missing = description['required']
        for url in description['url']:
            description_url = os.path.join(mirror_root, url)
            stage = Stage(
                description_url, name="build_cache", path=path, keep=True)
            try:
                stage.fetch()
                break
            except fs.FetchError as e:
                tty.debug(e)
        else:
            if fail_if_missing:
                tty.error('Failed to download required url {0}'.format(
                    description_url))
                return False
    return True


def download_buildcache_entry(file_descriptions, mirror_url=None):
    if not mirror_url and not spack.mirror.MirrorCollection():
        tty.die("Please provide or add a spack mirror to allow " +
                "download of buildcache entries.")

    if mirror_url:
        mirror_root = os.path.join(
            mirror_url, _build_cache_relative_path)
        return _download_buildcache_entry(mirror_root, file_descriptions)

    for mirror in spack.mirror.MirrorCollection().values():
        mirror_root = os.path.join(
            mirror.fetch_url,
            _build_cache_relative_path)

        if _download_buildcache_entry(mirror_root, file_descriptions):
            return True
        else:
            continue

    return False


def download_single_spec(
        concrete_spec, destination, mirror_url=None
):
    """Download the buildcache files for a single concrete spec.

    Args:
        concrete_spec: concrete spec to be downloaded
        destination (str): path where to put the downloaded buildcache
        mirror_url (str): url of the mirror from which to download
    """
    tarfile_name = tarball_name(concrete_spec, '.spack')
    tarball_dir_name = tarball_directory_name(concrete_spec)
    tarball_path_name = os.path.join(tarball_dir_name, tarfile_name)
    local_tarball_path = os.path.join(destination, tarball_dir_name)

    files_to_fetch = [
        {
            'url': [tarball_path_name],
            'path': local_tarball_path,
            'required': True,
        }, {
            'url': [tarball_name(concrete_spec, '.spec.json'),
                    tarball_name(concrete_spec, '.spec.yaml')],
            'path': destination,
            'required': True,
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
        if spec.startswith('/'):
            # Matching a DAG hash
            query_hash = spec.replace('/', '')
            for candidate_spec in self.possible_specs:
                if candidate_spec.dag_hash().startswith(query_hash):
                    matches.append(candidate_spec)
        else:
            # Matching a spec constraint
            matches = [
                s for s in self.possible_specs if s.satisfies(spec)
            ]
        return matches
