# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import errno
import re
import ssl
import tarfile
import shutil
import platform
import tempfile
import hashlib
import traceback
from contextlib import closing

from jsonschema import validate
import json

from six.moves.urllib.error import URLError

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, install_tree, get_filetype

import spack.cmd
import spack.fetch_strategy as fs
import spack.util.gpg as gpg_util
import spack.relocate as relocate
import spack.util.spack_yaml as syaml
from spack.schema.buildcache_index import schema
from spack.spec import Spec
from spack.stage import Stage
from spack.util.gpg import Gpg
from spack.util.web import spider, read_from_url
from spack.util.executable import ProcessError


_build_cache_relative_path = 'build_cache'
_meta_yaml_regex = re.compile(
    '[\d\.]+-([\w\d\-]+)-([\w\d\.]+)-([\w\d]{32})\.spec\.yaml$')


class NoOverwriteException(Exception):
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
    pass


class NoKeyException(spack.error.SpackError):
    """
    Raised when gpg has no default key added.
    """
    pass


class PickKeyException(spack.error.SpackError):
    """
    Raised when multiple keys can be used to sign.
    """
    def __init__(self, keys):
        err_msg = "Multi keys available for signing\n%s\n" % keys
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
    pass


def has_gnupg2():
    try:
        gpg_util.Gpg.gpg()('--version', output=os.devnull)
        return True
    except ProcessError:
        return False


def build_cache_relative_path():
    return _build_cache_relative_path


def build_cache_directory(prefix):
    return os.path.join(prefix, build_cache_relative_path())


def buildinfo_file_name(prefix):
    """
    Filename of the binary package meta-data file
    """
    name = prefix + "/.spack/binary_distribution"
    return name


def read_buildinfo_file(prefix):
    """
    Read buildinfo file
    """
    filename = buildinfo_file_name(prefix)
    with open(filename, 'r') as inputfile:
        content = inputfile.read()
        buildinfo = syaml.load(content)
    return buildinfo


def write_buildinfo_file(prefix, workdir, rel=False):
    """
    Create a cache file containing information
    required for the relocation
    """
    text_to_relocate = []
    binary_to_relocate = []
    blacklist = (".spack", "man")
    os_id = platform.system()
    # Do this at during tarball creation to save time when tarball unpacked.
    # Used by make_package_relative to determine binaries to change.
    for root, dirs, files in os.walk(prefix, topdown=True):
        dirs[:] = [d for d in dirs if d not in blacklist]
        for filename in files:
            path_name = os.path.join(root, filename)
            try:
                os.stat(path_name)
            except OSError, e:
                if e.errno == errno.ENOENT:
                    tty.warn("{0} does not exist, or is a broken symlink"
                             .format(path_name))
                    continue
                else:
                    raise e
            #  Check if the file contains a string with the installroot.
            #  This cuts down on the number of files added to the list
            #  of files potentially needing relocation
            if relocate.strings_contains_installroot(
                    path_name, spack.store.layout.root):
                filetype = get_filetype(path_name)
                if relocate.needs_binary_relocation(filetype, os_id):
                    rel_path_name = os.path.relpath(path_name, prefix)
                    binary_to_relocate.append(rel_path_name)
                elif relocate.needs_text_relocation(filetype):
                    rel_path_name = os.path.relpath(path_name, prefix)
                    text_to_relocate.append(rel_path_name)

    # Create buildinfo data and write it to disk
    buildinfo = {}
    buildinfo['relative_rpaths'] = rel
    buildinfo['buildpath'] = spack.store.layout.root
    buildinfo['relative_prefix'] = os.path.relpath(
        prefix, spack.store.layout.root)
    buildinfo['relocate_textfiles'] = text_to_relocate
    buildinfo['relocate_binaries'] = binary_to_relocate
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


def sign_tarball(key, force, specfile_path):
    # Sign the packages if keys available
    if not has_gnupg2():
        raise NoGpgException(
            "gpg2 is not available in $PATH .\n"
            "Use spack install gnupg and spack load gnupg.")
    else:
        if key is None:
            keys = Gpg.signing_keys()
            if len(keys) == 1:
                key = keys[0]
            if len(keys) > 1:
                raise PickKeyException(str(keys))
            if len(keys) == 0:
                msg = "No default key available for signing.\n"
                msg += "Use spack gpg init and spack gpg create"
                msg += " to create a default key."
                raise NoKeyException(msg)
    if os.path.exists('%s.asc' % specfile_path):
        if force:
            os.remove('%s.asc' % specfile_path)
        else:
            raise NoOverwriteException('%s.asc' % specfile_path)
    Gpg.sign(key, specfile_path, '%s.asc' % specfile_path)


def generate_html_index(path_list, output_path):
    f = open(output_path, 'w')
    header = """<html>\n
<head>\n</head>\n
<list>\n"""
    footer = "</list>\n</html>\n"
    f.write(header)
    for path in path_list:
        rel = os.path.basename(path)
        f.write('<li><a href="%s"> %s</a>\n' % (rel, rel))
    f.write(footer)
    f.close()


def generate_json_index(path_list, output_path):
    """Read all the .spec.yaml files generated by build_tarball and
       create an index from them."""
    index_object = {}

    for path in path_list:
        m = _meta_yaml_regex.search(path)

        if not m:
            # Expecting that some things won't match because they're not a spec
            # yaml file (like the index files written on a previous pass, or
            # the directories containing tarballs).  Just skip those.
            continue

        pkg_name = m.group(1)
        pkg_version = m.group(2)
        pkg_dag_hash = m.group(3)

        with open(path, 'r') as yaml_in:
            yaml_str = yaml_in.read()
            yaml_obj = syaml.load(yaml_str)

            entry = {
                'name': pkg_name,
                'version': pkg_version
            }

            if 'full_hash' in yaml_obj:
                entry['full_hash'] = yaml_obj['full_hash']

            index_object[pkg_dag_hash] = entry

    validate(index_object, schema)

    with open(output_path, 'w') as f:
        f.write(json.dumps(index_object))


def generate_package_index(build_cache_dir):
    yaml_list = os.listdir(build_cache_dir)
    path_list = [os.path.join(build_cache_dir, l) for l in yaml_list]

    index_html_path_tmp = os.path.join(build_cache_dir, 'index.html.tmp')
    index_html_path = os.path.join(build_cache_dir, 'index.html')

    index_json_path_tmp = os.path.join(build_cache_dir, 'index.json.tmp')
    index_json_path = os.path.join(build_cache_dir, 'index.json')

    generate_html_index(path_list, index_html_path_tmp)
    generate_json_index(path_list, index_json_path_tmp)

    shutil.move(index_html_path_tmp, index_html_path)
    shutil.move(index_json_path_tmp, index_json_path)


def build_tarball(spec, outdir, force=False, rel=False, unsigned=False,
                  allow_root=False, key=None, regenerate_index=False,
                  cdash_build_id=None):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).
    """
    if not spec.concrete:
        raise ValueError('spec must be concrete to build tarball')

    # set up some paths
    build_cache_dir = build_cache_directory(outdir)

    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_dir = os.path.join(build_cache_dir,
                               tarball_directory_name(spec))
    tarfile_path = os.path.join(tarfile_dir, tarfile_name)
    mkdirp(tarfile_dir)
    spackfile_path = os.path.join(
        build_cache_dir, tarball_path_name(spec, '.spack'))
    if os.path.exists(spackfile_path):
        if force:
            os.remove(spackfile_path)
        else:
            raise NoOverwriteException(str(spackfile_path))
    # need to copy the spec file so the build cache can be downloaded
    # without concretizing with the current spack packages
    # and preferences
    spec_file = os.path.join(spec.prefix, ".spack", "spec.yaml")
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = os.path.realpath(
        os.path.join(build_cache_dir, specfile_name))

    if os.path.exists(specfile_path):
        if force:
            os.remove(specfile_path)
        else:
            raise NoOverwriteException(str(specfile_path))
    # make a copy of the install directory to work with
    workdir = os.path.join(tempfile.mkdtemp(), os.path.basename(spec.prefix))
    # set symlinks=False here to avoid broken symlinks when archiving and
    # moving the package
    install_tree(spec.prefix, workdir, symlinks=False)

    # create info for later relocation and create tar
    write_buildinfo_file(spec.prefix, workdir, rel=rel)

    # optinally make the paths in the binaries relative to each other
    # in the spack install tree before creating tarball
    if rel:
        try:
            make_package_relative(workdir, spec.prefix, allow_root)
        except Exception as e:
            shutil.rmtree(workdir)
            shutil.rmtree(tarfile_dir)
            tty.die(str(e))
    else:
        try:
            make_package_placeholder(workdir, allow_root)
        except Exception as e:
            shutil.rmtree(workdir)
            shutil.rmtree(tarfile_dir)
            tty.die(str(e))
    # create compressed tarball of the install prefix
    with closing(tarfile.open(tarfile_path, 'w:gz')) as tar:
        tar.add(name='%s' % workdir,
                arcname='%s' % os.path.basename(spec.prefix))
    # remove copy of install directory
    shutil.rmtree(workdir)

    # get the sha256 checksum of the tarball
    checksum = checksum_tarball(tarfile_path)

    # add sha256 checksum to spec.yaml
    spec_dict = {}
    with open(spec_file, 'r') as inputfile:
        content = inputfile.read()
        spec_dict = syaml.load(content)
    bchecksum = {}
    bchecksum['hash_algorithm'] = 'sha256'
    bchecksum['hash'] = checksum
    spec_dict['binary_cache_checksum'] = bchecksum
    # Add original install prefix relative to layout root to spec.yaml.
    # This will be used to determine is the directory layout has changed.
    buildinfo = {}
    buildinfo['relative_prefix'] = os.path.relpath(
        spec.prefix, spack.store.layout.root)
    spec_dict['buildinfo'] = buildinfo
    spec_dict['full_hash'] = spec.full_hash()

    print('The full_hash ({0}) of {1} will be written into {2}'.format(
        spec_dict['full_hash'], spec.name, specfile_path))
    print(spec.tree())

    with open(specfile_path, 'w') as outfile:
        outfile.write(syaml.dump(spec_dict))

    # Write the .cdashid file if we were asked to do so
    if cdash_build_id:
        cdashidfile_name = tarball_name(spec, '.cdashid')
        cdashidfile_path = os.path.realpath(
            os.path.join(build_cache_dir, cdashidfile_name))
        if not os.path.exists(cdashidfile_path):
            with open(cdashidfile_path, 'w') as outfile:
                outfile.write('{0}\n'.format(cdash_build_id))

    # sign the tarball and spec file with gpg
    if not unsigned:
        sign_tarball(key, force, specfile_path)
    # put tarball, spec and signature files in .spack archive
    with closing(tarfile.open(spackfile_path, 'w')) as tar:
        tar.add(name='%s' % tarfile_path, arcname='%s' % tarfile_name)
        tar.add(name='%s' % specfile_path, arcname='%s' % specfile_name)
        if not unsigned:
            tar.add(name='%s.asc' % specfile_path,
                    arcname='%s.asc' % specfile_name)

    # cleanup file moved to archive
    os.remove(tarfile_path)
    if not unsigned:
        os.remove('%s.asc' % specfile_path)

    # create an index.html as well as index.json for the build_cache directory
    # so specs can be found
    if regenerate_index:
        generate_package_index(build_cache_dir)

    return None


def download_tarball(spec):
    """
    Download binary tarball for given package into stage area
    Return True if successful
    """
    mirrors = spack.config.get('mirrors')
    if len(mirrors) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of pre-compiled packages.")
    tarball = tarball_path_name(spec, '.spack')
    for key in mirrors:
        url = mirrors[key] + "/" + _build_cache_relative_path + "/" + tarball
        # stage the tarball into standard place
        stage = Stage(url, name="build_cache", keep=True)
        try:
            stage.fetch()
            return stage.save_filename
        except fs.FetchError:
            continue
    return None


def make_package_relative(workdir, prefix, allow_root):
    """
    Change paths in binaries to relative paths
    """
    buildinfo = read_buildinfo_file(workdir)
    old_path = buildinfo['buildpath']
    orig_path_names = list()
    cur_path_names = list()
    for filename in buildinfo['relocate_binaries']:
        orig_path_names.append(os.path.join(prefix, filename))
        cur_path_names.append(os.path.join(workdir, filename))
    relocate.make_binary_relative(cur_path_names, orig_path_names,
                                  old_path, allow_root)


def make_package_placeholder(workdir, allow_root):
    """
    Change paths in binaries to placeholder paths
    """
    buildinfo = read_buildinfo_file(workdir)
    cur_path_names = list()
    for filename in buildinfo['relocate_binaries']:
        cur_path_names.append(os.path.join(workdir, filename))
    relocate.make_binary_placeholder(cur_path_names, allow_root)


def relocate_package(workdir, allow_root):
    """
    Relocate the given package
    """
    buildinfo = read_buildinfo_file(workdir)
    new_path = spack.store.layout.root
    old_path = buildinfo['buildpath']
    rel = buildinfo.get('relative_rpaths', False)
    if rel:
        return

    tty.msg("Relocating package from",
            "%s to %s." % (old_path, new_path))
    path_names = set()
    for filename in buildinfo['relocate_textfiles']:
        path_name = os.path.join(workdir, filename)
        # Don't add backup files generated by filter_file during install step.
        if not path_name.endswith('~'):
            path_names.add(path_name)
    relocate.relocate_text(path_names, old_path, new_path)
    # If the binary files in the package were not edited to use
    # relative RPATHs, then the RPATHs need to be relocated
    if not rel:
        path_names = set()
        for filename in buildinfo['relocate_binaries']:
            path_name = os.path.join(workdir, filename)
            path_names.add(path_name)
        relocate.relocate_binary(path_names, old_path, new_path,
                                 allow_root)


def extract_tarball(spec, filename, allow_root=False, unsigned=False,
                    force=False):
    """
    extract binary tarball for given package into install area
    """
    if os.path.exists(spec.prefix):
        if force:
            shutil.rmtree(spec.prefix)
        else:
            raise NoOverwriteException(str(spec.prefix))

    tmpdir = tempfile.mkdtemp()
    stagepath = os.path.dirname(filename)
    spackfile_name = tarball_name(spec, '.spack')
    spackfile_path = os.path.join(stagepath, spackfile_name)
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_path = os.path.join(tmpdir, tarfile_name)
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = os.path.join(tmpdir, specfile_name)

    with closing(tarfile.open(spackfile_path, 'r')) as tar:
        tar.extractall(tmpdir)
    if not unsigned:
        if os.path.exists('%s.asc' % specfile_path):
            try:
                Gpg.verify('%s.asc' % specfile_path, specfile_path)
            except Exception as e:
                shutil.rmtree(tmpdir)
                tty.die(str(e))
        else:
            shutil.rmtree(tmpdir)
            raise NoVerifyException(
                "Package spec file failed signature verification.\n"
                "Use spack buildcache keys to download "
                "and install a key for verification from the mirror.")
    # get the sha256 checksum of the tarball
    checksum = checksum_tarball(tarfile_path)

    # get the sha256 checksum recorded at creation
    spec_dict = {}
    with open(specfile_path, 'r') as inputfile:
        content = inputfile.read()
        spec_dict = syaml.load(content)
    bchecksum = spec_dict['binary_cache_checksum']

    # if the checksums don't match don't install
    if bchecksum['hash'] != checksum:
        shutil.rmtree(tmpdir)
        raise NoChecksumException(
            "Package tarball failed checksum verification.\n"
            "It cannot be installed.")

    new_relative_prefix = str(os.path.relpath(spec.prefix,
                                              spack.store.layout.root))
    # if the original relative prefix is in the spec file use it
    buildinfo = spec_dict.get('buildinfo', {})
    old_relative_prefix = buildinfo.get('relative_prefix', new_relative_prefix)
    # if the original relative prefix and new relative prefix differ the
    # directory layout has changed and the  buildcache cannot be installed
    if old_relative_prefix != new_relative_prefix:
        shutil.rmtree(tmpdir)
        msg = "Package tarball was created from an install "
        msg += "prefix with a different directory layout.\n"
        msg += "It cannot be relocated."
        raise NewLayoutException(msg)

    # extract the tarball in a temp directory
    with closing(tarfile.open(tarfile_path, 'r')) as tar:
        tar.extractall(path=tmpdir)
    # the base of the install prefix is used when creating the tarball
    # so the pathname should be the same now that the directory layout
    # is confirmed
    workdir = os.path.join(tmpdir, os.path.basename(spec.prefix))

    # cleanup
    os.remove(tarfile_path)
    os.remove(specfile_path)

    try:
        relocate_package(workdir, allow_root)
    except Exception as e:
        shutil.rmtree(workdir)
        tty.die(str(e))
    # Delay creating spec.prefix until verification is complete
    # and any relocation has been done.
    else:
        install_tree(workdir, spec.prefix, symlinks=True)
    finally:
        shutil.rmtree(tmpdir)


#: Internal cache for get_specs
_cached_specs = None


def get_specs(force=False):
    """
    Get spec.yaml's for build caches available on mirror
    """
    global _cached_specs

    if _cached_specs:
        tty.debug("Using previously-retrieved specs")
        return _cached_specs

    mirrors = spack.config.get('mirrors')
    if len(mirrors) == 0:
        tty.warn("No Spack mirrors are currently configured")
        return {}

    path = str(spack.architecture.sys_type())
    urls = set()
    for key in mirrors:
        url = mirrors[key]
        if url.startswith('file'):
            mirror = url.replace('file://', '') + '/build_cache'
            tty.msg("Finding buildcaches in %s" % mirror)
            files = os.listdir(mirror)
            for file in files:
                if re.search('spec.yaml', file):
                    link = 'file://' + mirror + '/' + file
                    urls.add(link)
        else:
            tty.msg("Finding buildcaches on %s" % url)
            p, links = spider(url + "/build_cache")
            for link in links:
                if re.search("spec.yaml", link) and re.search(path, link):
                    urls.add(link)

    _cached_specs = set()
    for link in urls:
        with Stage(link, name="build_cache", keep=True) as stage:
            if force and os.path.exists(stage.save_filename):
                os.remove(stage.save_filename)
            if not os.path.exists(stage.save_filename):
                try:
                    stage.fetch()
                except fs.FetchError:
                    continue
            with open(stage.save_filename, 'r') as f:
                # read the spec from the build cache file. All specs
                # in build caches are concrete (as they are built) so
                # we need to mark this spec concrete on read-in.
                spec = Spec.from_yaml(f)
                spec._mark_concrete()
                _cached_specs.add(spec)

    return _cached_specs


def get_keys(install=False, trust=False, force=False):
    """
    Get pgp public keys available on mirror
    """
    mirrors = spack.config.get('mirrors')
    if len(mirrors) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of build caches.")

    keys = set()
    for key in mirrors:
        url = mirrors[key]
        if url.startswith('file'):
            mirror = url.replace('file://', '') + '/build_cache'
            tty.msg("Finding public keys in %s" % mirror)
            files = os.listdir(mirror)
            for file in files:
                if re.search(r'\.key', file):
                    link = 'file://' + mirror + '/' + file
                    keys.add(link)
        else:
            tty.msg("Finding public keys on %s" % url)
            p, links = spider(url + "/build_cache", depth=1)
            for link in links:
                if re.search(r'\.key', link):
                    keys.add(link)
        for link in keys:
            with Stage(link, name="build_cache", keep=True) as stage:
                if os.path.exists(stage.save_filename) and force:
                    os.remove(stage.save_filename)
                if not os.path.exists(stage.save_filename):
                    try:
                        stage.fetch()
                    except fs.FetchError:
                        continue
            tty.msg('Found key %s' % link)
            if install:
                if trust:
                    Gpg.trust(stage.save_filename)
                    tty.msg('Added this key to trusted keys.')
                else:
                    tty.msg('Will not add this key to trusted keys.'
                            'Use -t to install all downloaded keys')


def needs_rebuild(spec, mirror_url, buildcache_index):
    if not spec.concrete:
        raise ValueError('spec must be concrete to check against mirror')

    pkg_name = spec.name
    pkg_version = spec.version

    pkg_hash = spec.dag_hash()
    pkg_full_hash = spec.full_hash()

    # tty.msg('Checking {0}-{1}'.format(pkg_name, pkg_version))
    tty.msg('Checking {0}-{1}, dag_hash = {2}, full_hash = {3}'.format(
        pkg_name, pkg_version, pkg_hash, pkg_full_hash))
    print(spec.tree())

    if buildcache_index:
        # just look in the index we already fetched
        if pkg_hash in buildcache_index:
            # At least remote binary mirror knows about it, so if the
            # full_hash doesn't match (or remote end doesn't know about
            # the full_hash), then we trigger a rebuild.  This logic can
            # be simplified once the dag_hash and the full_hash are the same.
            remote_pkg_info = buildcache_index[pkg_hash]
            if ('full_hash' not in remote_pkg_info or
                remote_pkg_info['full_hash'] != pkg_full_hash):
                    return True
    else:
        # retrieve the .spec.yaml and look there instead
        build_cache_dir = build_cache_directory(mirror_url)
        spec_yaml_file_name = tarball_name(spec, '.spec.yaml')
        file_path = os.path.join(build_cache_dir, spec_yaml_file_name)

        try:
            yaml_contents = read_from_url(file_path)
        except URLError as e:
            tty.debug(e)

            if hasattr(e, 'reason') and isinstance(e.reason, ssl.SSLError):
                tty.warn("Spack was unable to fetch url list due to a "
                         "certificate verification problem. You can try "
                         "running spack -k, which will not check SSL "
                         "certificates. Use this at your own risk.")

            return True

        except Exception as e:
            tty.warn("Error in needs_rebuild: %s:%s" % (type(e), e),
                     traceback.format_exc())
            return True

        if not yaml_contents:
            tty.warn('reading {0} returned nothing, rebuilding {1}'.format(
                file_path, spec.short_spec))
            return True

        spec_yaml = syaml.load(yaml_contents)

        # If either the full_hash didn't exist in the .spec.yaml file, or it
        # did, but didn't match the one we computed locally, then we should
        # just rebuild.  This can be simplified once the dag_hash and the
        # full_hash become the same thing.
        if ('full_hash' not in spec_yaml or
            spec_yaml['full_hash'] != pkg_full_hash):
                if 'full_hash' in spec_yaml:
                    tty.msg('hashes did not match, remote = {0}, local = {1}'.format(
                        spec_yaml['full_hash'], pkg_full_hash))
                else:
                    tty.msg('full_hash missing from remote spec.yaml')
                print(spec.tree())
                return True

    return False


def get_remote_index(mirror_url):
    build_cache_dir = build_cache_directory(mirror_url)

    # First fetch the index.json
    index_path = os.path.join(build_cache_dir, 'index.json')
    index_contents = read_from_url(index_path)

    return json.loads(index_contents)


def check_specs_against_mirrors(mirrors, specs, no_index=False,
                                output_file=None):
    rebuilds = {}
    for mirror in mirrors.keys():
        mirror_url = mirrors[mirror]
        tty.msg('Checking for built specs at %s' % mirror_url)

        rebuild_list = []
        remote_pkg_index = None
        if not no_index:
            remote_pkg_index = get_remote_index(mirror_url)

        for spec in specs:
            if needs_rebuild(spec, mirror_url, remote_pkg_index):
                rebuild_list.append({
                    'short_spec': spec.short_spec,
                    'hash': spec.dag_hash()
                })

        if rebuild_list:
            rebuilds[mirror_url] = {
                'mirrorName': mirror,
                'mirrorUrl': mirror_url,
                'rebuildSpecs': rebuild_list
            }

    if output_file:
        with open(output_file, 'w') as outf:
            outf.write(json.dumps(rebuilds))

    return 1 if rebuilds else 0


def download_buildcache_entry(spec, path):
    if not spec.concrete:
        raise ValueError('spec must be concrete to download buildcache entry')

    mirrors = spack.config.get('mirrors')
    if len(mirrors) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of buildcache entries.")

    tarfile_name = tarball_name(spec, '.spack')
    specfile_name = tarball_name(spec, '.spec.yaml')
    cdashidfile_name = tarball_name(spec, '.cdashid')
    tarball_dir_name = tarball_directory_name(spec)
    tarball_path_name = os.path.join(tarball_dir_name, tarfile_name)

    local_tarball_path = os.path.join(path, tarball_dir_name)
    mkdirp(local_tarball_path)

    for key in mirrors:
        mirror_root = mirrors[key] + "/" + _build_cache_relative_path
        tarball_url = mirror_root + "/" + tarball_path_name
        stage = Stage(tarball_url, name="build_cache",
                      path=local_tarball_path, keep=True)
        try:
            stage.fetch()

            specfile_url = mirror_root + "/" + specfile_name
            stage2 = Stage(specfile_url, name="build_cache", path=path, keep=True)
            try:
                stage2.fetch()

                # Since we got the .spec.yaml file successfully, we're going
                # to break and not try any more mirrors.  Before we do though,
                # we'll try to fetch a .cdashid file associated with the
                # buildcache entry.  If we don't get one, it's not any kind of
                # error, as buildcache entries are not required to have them.
                cdashidfile_url = mirror_root + "/" + cdashidfile_name
                stage3 = Stage(cdashidfile_url, name="build_cache",
                               path=path, keep=True)
                try:
                    stage3.fetch()
                except:
                    tty.msg('No .cdashid file associated with {0}'.format(
                        specfile_name))

                break
            except fs.FetchError:
                continue
        except fs.FetchError:
            continue
