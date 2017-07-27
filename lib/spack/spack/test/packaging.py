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
from spack.database import Database
from spack.directory_layout import YamlDirectoryLayout
from spack.fetch_strategy import URLFetchStrategy, FetchStrategyComposite
from spack.spec import Spec
import spack.binary_distribution as bindist
from llnl.util.filesystem import *
import argparse
import spack.cmd.buildcache as buildcache
import spack.relocate as relocate
import platform
import os
import stat


@pytest.fixture(scope='function')
def install_mockery(tmpdir, config, builtin_mock):
    """Hooks a fake install directory and a fake db into Spack."""
    layout = spack.store.layout
    db = spack.store.db
    # Use a fake install directory to avoid conflicts bt/w
    # installed pkgs and mock packages.
    old_stage_path = spack.stage_path
    spack.store.layout = YamlDirectoryLayout(str(tmpdir))
    spack.store.db = Database(str(tmpdir))
    spack.stage_path = join_path(tmpdir, 'stage')
    # We use a fake package, so skip the checksum.
    spack.do_checksum = False
    yield
    # Turn checksumming back on
    spack.do_checksum = True
    # Restore Spack's layout.
    spack.store.layout = layout
    spack.store.db = db
    spack.stage_path = old_stage_path


def fake_fetchify(url, pkg):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(url))
    pkg.fetcher = fetcher


@pytest.mark.usefixtures('install_mockery')
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

    # Create a build cache without signing
    args = parser.parse_args(['create', '-d', mirror_path, '-y', str(spec)])
    buildcache.createtarball(args)

    # Validate the relocation information
    buildinfo = bindist.read_buildinfo_file(spec)
    assert(buildinfo['relocate_textfiles'] == ['dummy.txt'])

    # Create a build cache without signing, making rpaths relative first
    # overwriting previous build cache
    args = parser.parse_args(
        ['create', '-d', mirror_path, '-f', '-r', '-y', str(spec)])
    buildcache.createtarball(args)

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

    args = parser.parse_args(['list'])
    buildcache.listspecs(args)

    args = parser.parse_args(['list', 'trivial'])
    buildcache.listspecs(args)

    args = parser.parse_args(['keys'])
    buildcache.getkeys(args)

    relocate.needs_binary_relocation('relocatable')
    relocate.macho_make_paths_rel('/Users/Shared/spack',
                                  ('/Users/Shared/spack/pkgA/lib',
                                   '/Users/Shared/spack/pkgB/lib',
                                   '/usr/local/lib'),
                                  ('/Users/Shared/spack/pkgA/libA.dylib',
                                   '/Users/Shared/spack/pkgB/libB.dylib',
                                   '/usr/local/lib/libloco.dylib'),
                                  '/Users/Shared/spack/pkgC/lib/libC.dylib')
    relocate.macho_make_paths_rel('/Users/Shared/spack',
                                  ('/Users/Shared/spack/pkgA/lib',
                                   '/Users/Shared/spack/pkgB/lib',
                                   '/usr/local/lib'),
                                  ('/Users/Shared/spack/pkgA/libA.dylib',
                                   '/Users/Shared/spack/pkgB/libB.dylib',
                                   '/usr/local/lib/libloco.dylib'),
                                  None)
    relocate.macho_replace_paths('/Users/Shared/spack',
                                 '/Applications/spack',
                                 ('/Users/Shared/spack/pkgA/lib',
                                  '/Users/Shared/spack/pkgB/lib',
                                  '/usr/local/lib'),
                                 ('/Users/Shared/spack/pkgA/libA.dylib',
                                  '/Users/Shared/spack/pkgB/libB.dylib',
                                  '/usr/local/lib/libloco.dylib'),
                                 '/Users/Shared/spack/pkgC/lib/libC.dylib')
    relocate.macho_replace_paths('/Users/Shared/spack',
                                 '/Applications/spack',
                                 ('/Users/Shared/spack/pkgA/lib',
                                  '/Users/Shared/spack/pkgB/lib',
                                  '/usr/local/lib'),
                                 ('/Users/Shared/spack/pkgA/libA.dylib',
                                  '/Users/Shared/spack/pkgB/libB.dylib',
                                  '/usr/local/lib/libloco.dylib'),
                                 None)
    if platform.system() == 'Darwin':
        relocate.needs_binary_relocation('Mach-O')

    if platform.system() == 'Linux':
        relocate.needs_binary_relocation('ELF')
        relocate.get_relative_rpaths(
            '/usr/bin/test', '/usr',
            ('/usr/lib', '/usr/lib64', '/opt/local/lib'))
        relocate.substitute_rpath(
            ('/usr/lib', '/usr/lib64', '/opt/local/lib'), '/usr', '/opt')
        relocate.prelocate_binary(patchelfscr, '/opt/rh')
        relocate.relocate_binary(patchelfscr, '/usr', '/opt/rh/root/usr')
