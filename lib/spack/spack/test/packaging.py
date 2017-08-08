##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import pytest
import spack
import spack.store
from spack.fetch_strategy import URLFetchStrategy, FetchStrategyComposite
from spack.spec import Spec
import spack.binary_distribution as bindist
from llnl.util.filesystem import join_path, mkdirp
import argparse
import spack.cmd.buildcache as buildcache
from spack.relocate import *
import os
import stat
import sys


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
    except Exception:
        return False


def fake_fetchify(url, pkg):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(url))
    pkg.fetcher = fetcher


@pytest.mark.usefixtures('install_mockery', 'testing_gpg_directory')
def test_packaging(mock_archive, tmpdir):
    # tweak patchelf to only do a download
    spec = Spec("patchelf")
    spec.concretize()
    pkg = spack.repo.get(spec)
    fake_fetchify(pkg.fetcher, pkg)
    mkdirp(join_path(pkg.prefix, "bin"))
    patchelfscr = join_path(pkg.prefix, "bin", "patchelf")
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
    pkg = spack.repo.get(spec)
    fake_fetchify(mock_archive.url, pkg)
    pkg.do_install()

    # Put some non-relocatable file in there
    filename = join_path(spec.prefix, "dummy.txt")
    with open(filename, "w") as script:
        script.write(spec.prefix)

    # Create the build cache  and
    # put it directly into the mirror

    mirror_path = join_path(tmpdir, 'test-mirror')
    specs = [spec]
    spack.mirror.create(
        mirror_path, specs, no_checksum=True
    )

    parser = argparse.ArgumentParser()
    buildcache.setup_parser(parser)

    # Create a private key to sign package with if gpg2 available
    if has_gnupg2():
        spack.util.gpg.Gpg.create(name='test key 1', expires='0',
                                  email='spack@googlegroups.com',
                                  comment='Spack test key')
    # Create a build cache with signing
    args = parser.parse_args(['create', '-d', mirror_path, '-y', str(spec)])
    buildcache.buildcache(parser, args)

    # Validate the relocation information
    buildinfo = bindist.read_buildinfo_file(spec)
    assert(buildinfo['relocate_textfiles'] == ['dummy.txt'])

    # Create a build cache without signing, making rpaths relative first
    # overwriting previous build cache
    args = parser.parse_args(
        ['create', '-d', mirror_path, '-f', '-r', '-y', str(spec)])
    buildcache.buildcache(parser, args)

    # register mirror with spack config
    mirrors = {'spack-mirror-test': 'file://' + mirror_path}
    spack.config.update_config('mirrors', mirrors)

    # Uninstall the package
    pkg.do_uninstall(force=True)

    # download and install tarball
    file = bindist.download_tarball(spec)
    bindist.extract_tarball(spec, file, True, True)
    bindist.relocate_package(spec)
    spack.store.db.reindex(spack.store.layout)

    args = parser.parse_args(['install', '-f', '-y', str(spec)])
    buildcache.install_tarball(spec, args)
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['list'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['list', 'trivial'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['keys'])
    buildcache.buildcache(parser, args)


def test_relocate():
    assert (needs_binary_relocation('relocatable') is False)

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

    out = get_relative_rpaths(
        '/usr/bin/test', '/usr',
        ('/usr/lib', '/usr/lib64', '/opt/local/lib'))
    assert out == ['$ORIGIN/../lib', '$ORIGIN/../lib64', '/opt/local/lib']

    out = substitute_rpath(
        ('/usr/lib', '/usr/lib64', '/opt/local/lib'), '/usr', '/opt')
    assert out == ['/opt/lib', '/opt/lib64', '/opt/local/lib']


@pytest.mark.skipif(sys.platform != 'darwin',
                    reason="only works with Mach-o objects")
def test_relocate_macho():
    get_patchelf()
    assert (needs_binary_relocation('Mach-O') is True)
    macho_get_paths('/bin/bash')


@pytest.mark.skipif(sys.platform != 'linux2',
                    reason="only works with Elf objects")
def test_relocate_elf():
    assert (needs_binary_relocation('ELF') is True)
