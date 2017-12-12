##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import yaml
import shutil
import platform

import llnl.util.tty as tty
from spack.util.gpg import Gpg
from llnl.util.filesystem import mkdirp, join_path, install_tree
from spack.util.web import spider
import spack.cmd
import spack
from spack.stage import Stage
import spack.fetch_strategy as fs
from contextlib import closing
import spack.util.gpg as gpg_util
import hashlib
from spack.util.executable import ProcessError
import spack.relocate as relocate


class NoOverwriteException(Exception):
    pass


class NoGpgException(Exception):
    pass


class PickKeyException(Exception):
    pass


class NoKeyException(Exception):
    pass


class NoVerifyException(Exception):
    pass


class NoChecksumException(Exception):
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
            filetype = relocate.get_filetype(path_name)
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
    BLOCKSIZE = 65536
    hasher = hashlib.sha256()
    with open(file, 'rb') as tfile:
        buf = tfile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = tfile.read(BLOCKSIZE)
    return hasher.hexdigest()


def sign_tarball(yes_to_all, key, force, specfile_path):
    # Sign the packages if keys available
    if not has_gnupg2():
        raise NoGpgException()
    else:
        if key is None:
            keys = Gpg.signing_keys()
            if len(keys) == 1:
                key = keys[0]
            if len(keys) > 1:
                raise PickKeyException()
            if len(keys) == 0:
                raise NoKeyException()
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


def build_tarball(spec, outdir, force=False, rel=False, yes_to_all=False,
                  key=None):
    """
    Build a tarball from given spec and put it into the directory structure
    used at the mirror (following <tarball_directory_name>).
    """
    # set up some paths
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_dir = join_path(outdir, "build_cache",
                            tarball_directory_name(spec))
    tarfile_path = join_path(tarfile_dir, tarfile_name)
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
    spec_file = join_path(spec.prefix, ".spack", "spec.yaml")
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = os.path.realpath(
        join_path(outdir, "build_cache", specfile_name))
    indexfile_path = join_path(outdir, "build_cache", "index.html")
    if os.path.exists(specfile_path):
        if force:
            os.remove(specfile_path)
        else:
            raise NoOverwriteException(str(specfile_path))
    # make a copy of the install directory to work with
    workdir = join_path(outdir, os.path.basename(spec.prefix))
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    install_tree(spec.prefix, workdir, symlinks=True)

    # create info for later relocation and create tar
    write_buildinfo_file(spec.prefix, workdir, rel=rel)

    # optinally make the paths in the binaries relative to each other
    # in the spack install tree before creating tarball
    if rel:
        make_package_relative(workdir, spec.prefix)
    # create compressed tarball of the install prefix
    with closing(tarfile.open(tarfile_path, 'w:gz')) as tar:
        tar.add(name='%s' % workdir,
                arcname='%s' % os.path.basename(workdir))
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
    with open(specfile_path, 'w') as outfile:
        outfile.write(yaml.dump(spec_dict))
    signed = False
    if not yes_to_all:
        # sign the tarball and spec file with gpg
        try:
            sign_tarball(yes_to_all, key, force, specfile_path)
            signed = True
        except NoGpgException:
            raise NoGpgException()
        except PickKeyException:
            raise PickKeyException()
        except NoKeyException():
            raise NoKeyException()
    # put tarball, spec and signature files in .spack archive
    with closing(tarfile.open(spackfile_path, 'w')) as tar:
        tar.add(name='%s' % tarfile_path, arcname='%s' % tarfile_name)
        tar.add(name='%s' % specfile_path, arcname='%s' % specfile_name)
        if signed:
            tar.add(name='%s.asc' % specfile_path,
                    arcname='%s.asc' % specfile_name)

    # cleanup file moved to archive
    os.remove(tarfile_path)
    if signed:
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
    mirrors = spack.config.get_config('mirrors')
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


def make_package_relative(workdir, prefix):
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
                                      old_path)


def relocate_package(prefix):
    """
    Relocate the given package
    """
    buildinfo = read_buildinfo_file(prefix)
    new_path = spack.store.layout.root
    old_path = buildinfo['buildpath']
    rel = buildinfo.get('relative_rpaths', False)
    if new_path == old_path and not rel:
        return

    tty.msg("Relocating package from",
            "%s to %s." % (old_path, new_path))
    path_names = set()
    for filename in buildinfo['relocate_textfiles']:
        path_name = os.path.join(prefix, filename)
        # Don't add backup files generated by filter_file during install step.
        if not path_name.endswith('~'):
            path_names.add(path_name)
    relocate.relocate_text(path_names, old_path, new_path)
    # If the binary files in the package were not edited to use
    # relative RPATHs, then the RPATHs need to be relocated
    if not rel:
        path_names = set()
        for filename in buildinfo['relocate_binaries']:
            path_name = os.path.join(prefix, filename)
            path_names.add(path_name)
        relocate.relocate_binary(path_names, old_path, new_path)


def extract_tarball(spec, filename, yes_to_all=False, force=False):
    """
    extract binary tarball for given package into install area
    """
    installpath = spec.prefix
    if os.path.exists(installpath):
        if force:
            shutil.rmtree(installpath)
        else:
            raise NoOverwriteException(str(installpath))
    stagepath = os.path.dirname(filename)
    spackfile_name = tarball_name(spec, '.spack')
    spackfile_path = os.path.join(stagepath, spackfile_name)
    tarfile_name = tarball_name(spec, '.tar.gz')
    tarfile_path = os.path.join(stagepath, tarfile_name)
    specfile_name = tarball_name(spec, '.spec.yaml')
    specfile_path = os.path.join(stagepath, specfile_name)

    with closing(tarfile.open(spackfile_path, 'r')) as tar:
        tar.extractall(stagepath)

    if not yes_to_all:
        if os.path.exists('%s.asc' % specfile_path):
            Gpg.verify('%s.asc' % specfile_path, specfile_path)
            os.remove(specfile_path + '.asc')
        else:
            raise NoVerifyException()

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
        raise NoChecksumException()

    # delay creating installpath until verification is complete
    mkdirp(installpath)
    with closing(tarfile.open(tarfile_path, 'r')) as tar:
        tar.extractall(path=join_path(installpath, '..'))

    os.remove(tarfile_path)
    os.remove(specfile_path)
    relocate_package(installpath)


def get_specs(force=False):
    """
    Get spec.yaml's for build caches available on mirror
    """
    if spack.binary_cache_retrieved_specs:
        tty.debug("Using previously-retrieved specs")
        previously_retrieved = spack.binary_cache_retrieved_specs
        return previously_retrieved

    mirrors = spack.config.get_config('mirrors')
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

    specs = set()
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
                specs.add(spec)

    spack.binary_cache_retrieved_specs = specs
    return specs


def get_keys(install=False, yes_to_all=False, force=False):
    """
    Get pgp public keys available on mirror
    """
    mirrors = spack.config.get_config('mirrors')
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
                if yes_to_all:
                    Gpg.trust(stage.save_filename)
                    tty.msg('Added this key to trusted keys.')
                else:
                    tty.msg('Will not add this key to trusted keys.'
                            'Use -y to override')
