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
"""
This test checks the binary packaging infrastructure
"""
import os
import stat
import sys
import shutil
import pytest
import argparse

from llnl.util.filesystem import mkdirp

import spack.repo
import spack.store
import spack.binary_distribution as bindist
import spack.cmd.buildcache as buildcache
from spack.spec import Spec
from spack.paths import mock_gpg_keys_path
from spack.fetch_strategy import URLFetchStrategy, FetchStrategyComposite
from spack.util.executable import ProcessError
from spack.relocate import needs_binary_relocation, needs_text_relocation
from spack.relocate import strings_contains_installroot
from spack.relocate import get_patchelf, relocate_text
from spack.relocate import substitute_rpath, get_relative_rpaths
from spack.relocate import macho_replace_paths, macho_make_paths_relative
from spack.relocate import modify_macho_object, macho_get_paths


@pytest.fixture(scope='function')
def testing_gpg_directory(tmpdir):
    old_gpg_path = spack.util.gpg.GNUPGHOME
    spack.util.gpg.GNUPGHOME = str(tmpdir.join('gpg'))
    yield
    spack.util.gpg.GNUPGHOME = old_gpg_path


def has_gnupg2():
    try:
        spack.util.gpg.Gpg.gpg()('--version', output=os.devnull)
        return True
    except ProcessError:
        return False


def fake_fetchify(url, pkg):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(url))
    pkg.fetcher = fetcher


@pytest.mark.usefixtures('install_mockery', 'testing_gpg_directory')
def test_buildcache(mock_archive, tmpdir):
    # tweak patchelf to only do a download
    spec = Spec("patchelf")
    spec.concretize()
    pkg = spack.repo.get(spec)
    fake_fetchify(pkg.fetcher, pkg)
    mkdirp(os.path.join(pkg.prefix, "bin"))
    patchelfscr = os.path.join(pkg.prefix, "bin", "patchelf")
    f = open(patchelfscr, 'w')
    body = """#!/bin/bash
echo $PATH"""
    f.write(body)
    f.close()
    st = os.stat(patchelfscr)
    os.chmod(patchelfscr, st.st_mode | stat.S_IEXEC)

    # Install the test package
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    pkg = spec.package
    fake_fetchify(mock_archive.url, pkg)
    pkg.do_install()
    pkghash = '/' + spec.dag_hash(7)

    # Put some non-relocatable file in there
    filename = os.path.join(spec.prefix, "dummy.txt")
    with open(filename, "w") as script:
        script.write(spec.prefix)

    # Create the build cache  and
    # put it directly into the mirror

    mirror_path = os.path.join(str(tmpdir), 'test-mirror')
    spack.mirror.create(
        mirror_path, specs=[], no_checksum=True
    )

    # register mirror with spack config
    mirrors = {'spack-mirror-test': 'file://' + mirror_path}
    spack.config.set('mirrors', mirrors)

    stage = spack.stage.Stage(
        mirrors['spack-mirror-test'], name="build_cache", keep=True)
    stage.create()
    # setup argument parser
    parser = argparse.ArgumentParser()
    buildcache.setup_parser(parser)

    # Create a private key to sign package with if gpg2 available
    if has_gnupg2():
        spack.util.gpg.Gpg.create(name='test key 1', expires='0',
                                  email='spack@googlegroups.com',
                                  comment='Spack test key')
        # Create build cache with signing
        args = parser.parse_args(['create', '-d', mirror_path, str(spec)])
        buildcache.buildcache(parser, args)

        # Uninstall the package
        pkg.do_uninstall(force=True)

        # test overwrite install
        args = parser.parse_args(['install', '-f', str(pkghash)])
        buildcache.buildcache(parser, args)

        # create build cache with relative path and signing
        args = parser.parse_args(
            ['create', '-d', mirror_path, '-f', '-r', str(spec)])
        buildcache.buildcache(parser, args)

        # Uninstall the package
        pkg.do_uninstall(force=True)

        # install build cache with verification
        args = parser.parse_args(['install', str(spec)])
        buildcache.install_tarball(spec, args)

        # test overwrite install
        args = parser.parse_args(['install', '-f', str(pkghash)])
        buildcache.buildcache(parser, args)

    else:
        # create build cache without signing
        args = parser.parse_args(
            ['create', '-d', mirror_path, '-u', str(spec)])
        buildcache.buildcache(parser, args)

        # Uninstall the package
        pkg.do_uninstall(force=True)

        # install build cache without verification
        args = parser.parse_args(['install', '-u', str(spec)])
        buildcache.install_tarball(spec, args)

        # test overwrite install without verification
        args = parser.parse_args(['install', '-f', '-u', str(pkghash)])
        buildcache.buildcache(parser, args)

        # create build cache with relative path
        args = parser.parse_args(
            ['create', '-d', mirror_path, '-f', '-r', '-u', str(pkghash)])
        buildcache.buildcache(parser, args)

        # Uninstall the package
        pkg.do_uninstall(force=True)

        # install build cache
        args = parser.parse_args(['install', '-u', str(spec)])
        buildcache.install_tarball(spec, args)

        # test overwrite install
        args = parser.parse_args(['install', '-f', '-u', str(pkghash)])
        buildcache.buildcache(parser, args)

    # Validate the relocation information
    buildinfo = bindist.read_buildinfo_file(spec.prefix)
    assert(buildinfo['relocate_textfiles'] == ['dummy.txt'])

    args = parser.parse_args(['list'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['list', '-f'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['list', 'trivial'])
    buildcache.buildcache(parser, args)

    # Copy a key to the mirror to have something to download
    shutil.copyfile(mock_gpg_keys_path + '/external.key',
                    mirror_path + '/external.key')

    args = parser.parse_args(['keys'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['keys', '-f'])
    buildcache.buildcache(parser, args)

    # unregister mirror with spack config
    mirrors = {}
    spack.config.set('mirrors', mirrors)
    shutil.rmtree(mirror_path)
    stage.destroy()


def test_relocate_text(tmpdir):
    with tmpdir.as_cwd():
        # Validate the text path replacement
        old_dir = '/home/spack/opt/spack'
        filename = 'dummy.txt'
        with open(filename, "w") as script:
            script.write(old_dir)
            script.close()
        filenames = [filename]
        new_dir = '/opt/rh/devtoolset/'
        relocate_text(filenames, old_dir, new_dir)
        with open(filename, "r")as script:
            for line in script:
                assert(new_dir in line)
        assert(strings_contains_installroot(filename, old_dir) is False)


def test_needs_relocation():
    binary_type = (
        'ELF 64-bit LSB executable, x86-64, version 1 (SYSV),'
        ' dynamically linked (uses shared libs),'
        ' for GNU/Linux x.y.z, stripped')

    assert needs_binary_relocation(binary_type, os_id='Linux')
    assert not needs_binary_relocation('relocatable',
                                       os_id='Linux')
    assert not needs_binary_relocation('symbolic link to `foo\'',
                                       os_id='Linux')

    assert needs_text_relocation('ASCII text')
    assert not needs_text_relocation('symbolic link to `foo.text\'')

    macho_type = 'Mach-O 64-bit executable x86_64'
    assert needs_binary_relocation(macho_type, os_id='Darwin')


def test_macho_paths():

    out = macho_make_paths_relative('/Users/Shares/spack/pkgC/lib/libC.dylib',
                                    '/Users/Shared/spack',
                                    ('/Users/Shared/spack/pkgA/lib',
                                     '/Users/Shared/spack/pkgB/lib',
                                     '/usr/local/lib'),
                                    ('/Users/Shared/spack/pkgA/libA.dylib',
                                     '/Users/Shared/spack/pkgB/libB.dylib',
                                     '/usr/local/lib/libloco.dylib'),
                                    '/Users/Shared/spack/pkgC/lib/libC.dylib')
    assert out == (['@loader_path/../../../../Shared/spack/pkgA/lib',
                    '@loader_path/../../../../Shared/spack/pkgB/lib',
                    '/usr/local/lib'],
                   ['@loader_path/../../../../Shared/spack/pkgA/libA.dylib',
                    '@loader_path/../../../../Shared/spack/pkgB/libB.dylib',
                    '/usr/local/lib/libloco.dylib'],
                   '@rpath/libC.dylib')

    out = macho_make_paths_relative('/Users/Shared/spack/pkgC/bin/exeC',
                                    '/Users/Shared/spack',
                                    ('/Users/Shared/spack/pkgA/lib',
                                     '/Users/Shared/spack/pkgB/lib',
                                     '/usr/local/lib'),
                                    ('/Users/Shared/spack/pkgA/libA.dylib',
                                     '/Users/Shared/spack/pkgB/libB.dylib',
                                     '/usr/local/lib/libloco.dylib'), None)

    assert out == (['@loader_path/../../pkgA/lib',
                    '@loader_path/../../pkgB/lib',
                    '/usr/local/lib'],
                   ['@loader_path/../../pkgA/libA.dylib',
                    '@loader_path/../../pkgB/libB.dylib',
                    '/usr/local/lib/libloco.dylib'], None)

    out = macho_replace_paths('/Users/Shared/spack',
                              '/Applications/spack',
                              ('/Users/Shared/spack/pkgA/lib',
                               '/Users/Shared/spack/pkgB/lib',
                               '/usr/local/lib'),
                              ('/Users/Shared/spack/pkgA/libA.dylib',
                               '/Users/Shared/spack/pkgB/libB.dylib',
                               '/usr/local/lib/libloco.dylib'),
                              '/Users/Shared/spack/pkgC/lib/libC.dylib')
    assert out == (['/Applications/spack/pkgA/lib',
                    '/Applications/spack/pkgB/lib',
                    '/usr/local/lib'],
                   ['/Applications/spack/pkgA/libA.dylib',
                    '/Applications/spack/pkgB/libB.dylib',
                    '/usr/local/lib/libloco.dylib'],
                   '/Applications/spack/pkgC/lib/libC.dylib')

    out = macho_replace_paths('/Users/Shared/spack',
                              '/Applications/spack',
                              ('/Users/Shared/spack/pkgA/lib',
                               '/Users/Shared/spack/pkgB/lib',
                               '/usr/local/lib'),
                              ('/Users/Shared/spack/pkgA/libA.dylib',
                               '/Users/Shared/spack/pkgB/libB.dylib',
                               '/usr/local/lib/libloco.dylib'),
                              None)
    assert out == (['/Applications/spack/pkgA/lib',
                    '/Applications/spack/pkgB/lib',
                    '/usr/local/lib'],
                   ['/Applications/spack/pkgA/libA.dylib',
                    '/Applications/spack/pkgB/libB.dylib',
                    '/usr/local/lib/libloco.dylib'],
                   None)


def test_elf_paths():
    out = get_relative_rpaths(
        '/usr/bin/test', '/usr',
        ('/usr/lib', '/usr/lib64', '/opt/local/lib'))
    assert out == ['$ORIGIN/../lib', '$ORIGIN/../lib64', '/opt/local/lib']

    out = substitute_rpath(
        ('/usr/lib', '/usr/lib64', '/opt/local/lib'), '/usr', '/opt')
    assert out == ['/opt/lib', '/opt/lib64', '/opt/local/lib']


@pytest.mark.skipif(sys.platform != 'darwin',
                    reason="only works with Mach-o objects")
def test_relocate_macho(tmpdir):
    with tmpdir.as_cwd():

        get_patchelf()  # this does nothing on Darwin

        rpaths, deps, idpath = macho_get_paths('/bin/bash')
        nrpaths, ndeps, nid = macho_make_paths_relative('/bin/bash', '/usr',
                                                        rpaths, deps, idpath)
        shutil.copyfile('/bin/bash', 'bash')
        modify_macho_object('bash',
                            rpaths, deps, idpath,
                            nrpaths, ndeps, nid)

        rpaths, deps, idpath = macho_get_paths('/bin/bash')
        nrpaths, ndeps, nid = macho_replace_paths('/usr', '/opt',
                                                  rpaths, deps, idpath)
        shutil.copyfile('/bin/bash', 'bash')
        modify_macho_object('bash',
                            rpaths, deps, idpath,
                            nrpaths, ndeps, nid)

        path = '/usr/lib/libncurses.5.4.dylib'
        rpaths, deps, idpath = macho_get_paths(path)
        nrpaths, ndeps, nid = macho_make_paths_relative(path, '/usr',
                                                        rpaths, deps, idpath)
        shutil.copyfile(
            '/usr/lib/libncurses.5.4.dylib', 'libncurses.5.4.dylib')
        modify_macho_object('libncurses.5.4.dylib',
                            rpaths, deps, idpath,
                            nrpaths, ndeps, nid)

        rpaths, deps, idpath = macho_get_paths(path)
        nrpaths, ndeps, nid = macho_replace_paths('/usr', '/opt',
                                                  rpaths, deps, idpath)
        shutil.copyfile(
            '/usr/lib/libncurses.5.4.dylib', 'libncurses.5.4.dylib')
        modify_macho_object(
            'libncurses.5.4.dylib',
            rpaths, deps, idpath,
            nrpaths, ndeps, nid)
