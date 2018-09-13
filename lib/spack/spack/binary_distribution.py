##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import re
import tarfile
import shutil
import platform
import tempfile
import hashlib
from contextlib import closing

import ruamel.yaml as yaml

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, install_tree, get_filetype

import spack.cmd
import spack.fetch_strategy as fs
import spack.util.gpg as gpg_util
import spack.relocate as relocate
from spack.stage import Stage
from spack.util.gpg import Gpg
from spack.util.web import spider
from spack.util.executable import ProcessError


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
        buildinfo = yaml.load(content)
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
        outfile.write(yaml.dump(buildinfo, default_flow_style=True))


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


def generate_index(outdir, indexfile_path):
    f = open(indexfile_path, 'w')
    header = """<html>\n
<head>\n</head>\n
<list>\n"""
    footer = "</list>\n</html>\n"
    paths = os.listdir(outdir + '/build_cache')
    f.write(header)
    for path in paths:
        rel = os.path.basename(path)
        f.write('<li><a href="%s"> %s</a>\n' % (rel, rel))
    f.write(footer)
    f.close()


def build_tarball(spec, outdir, force=False, rel=False, unsigned=False,
                  allow_root=False, key=None):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).
    """
    # set up some paths
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_dir = os.path.join(outdir, "build_cache",
                               tarball_directory_name(spec))
    tarfile_path = os.path.join(tarfile_dir, tarfile_name)
    mkdirp(tarfile_dir)
    spackfile_path = os.path.join(
        outdir, "build_cache", tarball_path_name(spec, '.spack'))
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
        os.path.join(outdir, "build_cache", specfile_name))
    indexfile_path = os.path.join(outdir, "build_cache", "index.html")
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
        spec_dict = yaml.load(content)
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
    with open(specfile_path, 'w') as outfile:
        outfile.write(yaml.dump(spec_dict))
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
    if os.path.exists(indexfile_path):
        os.remove(indexfile_path)
    generate_index(outdir, indexfile_path)
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
        url = mirrors[key] + "/build_cache/" + tarball
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
        spec_dict = yaml.load(content)
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
                spec = spack.spec.Spec.from_yaml(f)
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
                if re.search('\.key', file):
                    link = 'file://' + mirror + '/' + file
                    keys.add(link)
        else:
            tty.msg("Finding public keys on %s" % url)
            p, links = spider(url + "/build_cache", depth=1)
            for link in links:
                if re.search("\.key", link):
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
