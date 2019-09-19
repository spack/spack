# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import tarfile
import shutil
import tempfile
import hashlib
from contextlib import closing

import json

from six.moves.urllib.error import URLError

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, install_tree

import spack.cmd
import spack.fetch_strategy as fs
import spack.util.gpg as gpg_util
import spack.relocate as relocate
import spack.util.spack_yaml as syaml
from spack.spec import Spec
from spack.stage import Stage
from spack.util.gpg import Gpg
from spack.util.web import spider, read_from_url
from spack.util.executable import ProcessError

_build_cache_relative_path = 'build_cache'


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
    name = os.path.join(prefix, ".spack/binary_distribution")
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
    link_to_relocate = []
    blacklist = (".spack", "man")
    # Do this at during tarball creation to save time when tarball unpacked.
    # Used by make_package_relative to determine binaries to change.
    for root, dirs, files in os.walk(prefix, topdown=True):
        dirs[:] = [d for d in dirs if d not in blacklist]
        for filename in files:
            path_name = os.path.join(root, filename)
            m_type, m_subtype = relocate.mime_type(path_name)
            if os.path.islink(path_name):
                link = os.readlink(path_name)
                if os.path.isabs(link):
                    # Relocate absolute links into the spack tree
                    if link.startswith(spack.store.layout.root):
                        rel_path_name = os.path.relpath(path_name, prefix)
                        link_to_relocate.append(rel_path_name)
                    else:
                        msg = 'Absolute link %s to %s ' % (path_name, link)
                        msg += 'outside of stage %s ' % prefix
                        msg += 'cannot be relocated.'
                        tty.warn(msg)

            if relocate.needs_binary_relocation(m_type, m_subtype):
                if not filename.endswith('.o'):
                    rel_path_name = os.path.relpath(path_name, prefix)
                    binary_to_relocate.append(rel_path_name)
            if relocate.needs_text_relocation(m_type, m_subtype):
                rel_path_name = os.path.relpath(path_name, prefix)
                text_to_relocate.append(rel_path_name)

    # Create buildinfo data and write it to disk
    buildinfo = {}
    buildinfo['relative_rpaths'] = rel
    buildinfo['buildpath'] = spack.store.layout.root
    buildinfo['spackprefix'] = spack.paths.prefix
    buildinfo['relative_prefix'] = os.path.relpath(
        prefix, spack.store.layout.root)
    buildinfo['relocate_textfiles'] = text_to_relocate
    buildinfo['relocate_binaries'] = binary_to_relocate
    buildinfo['relocate_links'] = link_to_relocate
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


def _generate_html_index(path_list, output_path):
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


def generate_package_index(build_cache_dir):
    yaml_list = os.listdir(build_cache_dir)
    path_list = [os.path.join(build_cache_dir, l) for l in yaml_list]

    index_html_path_tmp = os.path.join(build_cache_dir, 'index.html.tmp')
    index_html_path = os.path.join(build_cache_dir, 'index.html')

    _generate_html_index(path_list, index_html_path_tmp)
    shutil.move(index_html_path_tmp, index_html_path)


def build_tarball(spec, outdir, force=False, rel=False, unsigned=False,
                  allow_root=False, key=None, regenerate_index=False):
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
    install_tree(spec.prefix, workdir, symlinks=True)

    # create info for later relocation and create tar
    write_buildinfo_file(spec.prefix, workdir, rel=rel)

    # optionally make the paths in the binaries relative to each other
    # in the spack install tree before creating tarball
    if rel:
        try:
            make_package_relative(workdir, spec, allow_root)
        except Exception as e:
            shutil.rmtree(workdir)
            shutil.rmtree(tarfile_dir)
            tty.die(e)
    else:
        try:
            make_package_placeholder(workdir, spec, allow_root)
        except Exception as e:
            shutil.rmtree(workdir)
            shutil.rmtree(tarfile_dir)
            tty.die(e)
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

    tty.debug('The full_hash ({0}) of {1} will be written into {2}'.format(
        spec_dict['full_hash'], spec.name, specfile_path))
    tty.debug(spec.tree())

    with open(specfile_path, 'w') as outfile:
        outfile.write(syaml.dump(spec_dict))

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

    # create an index.html for the build_cache directory so specs can be found
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
    for mirror_name, mirror_url in mirrors.items():
        url = mirror_url + '/' + _build_cache_relative_path + '/' + tarball
        # stage the tarball into standard place
        stage = Stage(url, name="build_cache", keep=True)
        try:
            stage.fetch()
            return stage.save_filename
        except fs.FetchError:
            continue
    return None


def make_package_relative(workdir, spec, allow_root):
    """
    Change paths in binaries to relative paths. Change absolute symlinks
    to relative symlinks.
    """
    prefix = spec.prefix
    buildinfo = read_buildinfo_file(workdir)
    old_path = buildinfo['buildpath']
    orig_path_names = list()
    cur_path_names = list()
    for filename in buildinfo['relocate_binaries']:
        orig_path_names.append(os.path.join(prefix, filename))
        cur_path_names.append(os.path.join(workdir, filename))
    if spec.architecture.platform == 'darwin':
        relocate.make_macho_binaries_relative(cur_path_names, orig_path_names,
                                              old_path, allow_root)
    else:
        relocate.make_elf_binaries_relative(cur_path_names, orig_path_names,
                                            old_path, allow_root)
    orig_path_names = list()
    cur_path_names = list()
    for filename in buildinfo.get('relocate_links', []):
        orig_path_names.append(os.path.join(prefix, filename))
        cur_path_names.append(os.path.join(workdir, filename))
    relocate.make_link_relative(cur_path_names, orig_path_names)


def make_package_placeholder(workdir, spec, allow_root):
    """
    Check if package binaries are relocatable.
    Change links to placeholder links.
    """
    prefix = spec.prefix
    buildinfo = read_buildinfo_file(workdir)
    cur_path_names = list()
    for filename in buildinfo['relocate_binaries']:
        cur_path_names.append(os.path.join(workdir, filename))
    relocate.check_files_relocatable(cur_path_names, allow_root)

    cur_path_names = list()
    for filename in buildinfo.get('relocate_links', []):
        cur_path_names.append(os.path.join(workdir, filename))
    relocate.make_link_placeholder(cur_path_names, workdir, prefix)


def relocate_package(workdir, spec, allow_root):
    """
    Relocate the given package
    """
    buildinfo = read_buildinfo_file(workdir)
    new_path = spack.store.layout.root
    new_prefix = spack.paths.prefix
    old_path = buildinfo['buildpath']
    old_prefix = buildinfo.get('spackprefix', '/not/in/buildinfo/dictionary')
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
    relocate.relocate_text(path_names, oldpath=old_path,
                           newpath=new_path, oldprefix=old_prefix,
                           newprefix=new_prefix)
    # If the binary files in the package were not edited to use
    # relative RPATHs, then the RPATHs need to be relocated
    if not rel:
        path_names = set()
        for filename in buildinfo['relocate_binaries']:
            path_name = os.path.join(workdir, filename)
            path_names.add(path_name)
        if spec.architecture.platform == 'darwin':
            relocate.relocate_macho_binaries(path_names, old_path,
                                             new_path, allow_root)
        else:
            relocate.relocate_elf_binaries(path_names, old_path,
                                           new_path, allow_root)
        path_names = set()
        for filename in buildinfo.get('relocate_links', []):
            path_name = os.path.join(workdir, filename)
            path_names.add(path_name)
        relocate.relocate_links(path_names, old_path, new_path)


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
                tty.die(e)
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
        relocate_package(workdir, spec, allow_root)
    except Exception as e:
        shutil.rmtree(workdir)
        tty.die(e)
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
    for mirror_name, mirror_url in mirrors.items():
        if mirror_url.startswith('file'):
            mirror = mirror_url.replace(
                'file://', '') + "/" + _build_cache_relative_path
            tty.msg("Finding buildcaches in %s" % mirror)
            if os.path.exists(mirror):
                files = os.listdir(mirror)
                for file in files:
                    if re.search('spec.yaml', file):
                        link = 'file://' + mirror + '/' + file
                        urls.add(link)
        else:
            tty.msg("Finding buildcaches on %s" % mirror_url)
            p, links = spider(mirror_url + "/" + _build_cache_relative_path)
            for link in links:
                if re.search("spec.yaml", link) and re.search(path, link):
                    urls.add(link)

    _cached_specs = []
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
                _cached_specs.append(spec)

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
    for mirror_name, mirror_url in mirrors.items():
        if mirror_url.startswith('file'):
            mirror = os.path.join(
                mirror_url.replace('file://', ''), _build_cache_relative_path)
            tty.msg("Finding public keys in %s" % mirror)
            files = os.listdir(mirror)
            for file in files:
                if re.search(r'\.key', file):
                    link = 'file://' + mirror + '/' + file
                    keys.add(link)
        else:
            tty.msg("Finding public keys on %s" % mirror_url)
            p, links = spider(mirror_url + "/build_cache", depth=1)
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

    # Try to retrieve the .spec.yaml directly, based on the known
    # format of the name, in order to determine if the package
    # needs to be rebuilt.
    build_cache_dir = build_cache_directory(mirror_url)
    spec_yaml_file_name = tarball_name(spec, '.spec.yaml')
    file_path = os.path.join(build_cache_dir, spec_yaml_file_name)

    result_of_error = 'Package ({0}) will {1}be rebuilt'.format(
        spec.short_spec, '' if rebuild_on_errors else 'not ')

    try:
        yaml_contents = read_from_url(file_path)
    except URLError as url_err:
        err_msg = [
            'Unable to determine whether {0} needs rebuilding,',
            ' caught URLError attempting to read from {1}.',
        ]
        tty.error(''.join(err_msg).format(spec.short_spec, file_path))
        tty.debug(url_err)
        tty.warn(result_of_error)
        return rebuild_on_errors

    if not yaml_contents:
        tty.error('Reading {0} returned nothing'.format(file_path))
        tty.warn(result_of_error)
        return rebuild_on_errors

    spec_yaml = syaml.load(yaml_contents)

    # If either the full_hash didn't exist in the .spec.yaml file, or it
    # did, but didn't match the one we computed locally, then we should
    # just rebuild.  This can be simplified once the dag_hash and the
    # full_hash become the same thing.
    if ('full_hash' not in spec_yaml or
            spec_yaml['full_hash'] != pkg_full_hash):
        if 'full_hash' in spec_yaml:
            reason = 'hash mismatch, remote = {0}, local = {1}'.format(
                spec_yaml['full_hash'], pkg_full_hash)
        else:
            reason = 'full_hash was missing from remote spec.yaml'
        tty.msg('Rebuilding {0}, reason: {1}'.format(
            spec.short_spec, reason))
        tty.msg(spec.tree())
        return True

    return False


def check_specs_against_mirrors(mirrors, specs, output_file=None,
                                rebuild_on_errors=False):
    """Check all the given specs against buildcaches on the given mirrors and
    determine if any of the specs need to be rebuilt.  Reasons for needing to
    rebuild include binary cache for spec isn't present on a mirror, or it is
    present but the full_hash has changed since last time spec was built.

    Arguments:
        mirrors (dict): Mirrors to check against
        specs (iterable): Specs to check against mirrors
        output_file (string): Path to output file to be written.  If provided,
            mirrors with missing or out-of-date specs will be formatted as a
            JSON object and written to this file.
        rebuild_on_errors (boolean): Treat any errors encountered while
            checking specs as a signal to rebuild package.

    Returns: 1 if any spec was out-of-date on any mirror, 0 otherwise.

    """
    rebuilds = {}
    for mirror_name, mirror_url in mirrors.items():
        tty.msg('Checking for built specs at %s' % mirror_url)

        rebuild_list = []

        for spec in specs:
            if needs_rebuild(spec, mirror_url, rebuild_on_errors):
                rebuild_list.append({
                    'short_spec': spec.short_spec,
                    'hash': spec.dag_hash()
                })

        if rebuild_list:
            rebuilds[mirror_url] = {
                'mirrorName': mirror_name,
                'mirrorUrl': mirror_url,
                'rebuildSpecs': rebuild_list
            }

    if output_file:
        with open(output_file, 'w') as outf:
            outf.write(json.dumps(rebuilds))

    return 1 if rebuilds else 0


def _download_buildcache_entry(mirror_root, descriptions):
    for description in descriptions:
        url = os.path.join(mirror_root, description['url'])
        path = description['path']
        fail_if_missing = description['required']

        mkdirp(path)

        stage = Stage(url, name="build_cache", path=path, keep=True)

        try:
            stage.fetch()
        except fs.FetchError as e:
            tty.debug(e)
            if fail_if_missing:
                tty.error('Failed to download required url {0}'.format(url))
                return False

    return True


def download_buildcache_entry(file_descriptions):
    mirrors = spack.config.get('mirrors')
    if len(mirrors) == 0:
        tty.die("Please add a spack mirror to allow " +
                "download of buildcache entries.")

    for mirror_name, mirror_url in mirrors.items():
        mirror_root = os.path.join(mirror_url, _build_cache_relative_path)

        if _download_buildcache_entry(mirror_root, file_descriptions):
            return True
        else:
            continue

    return False
