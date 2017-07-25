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

# import argparse
# import spack.cmd.gpg as gpg
# import spack.util.gpg as gpg_util


@pytest.fixture(scope='function')
def install_mockery(tmpdir, config, builtin_mock):
    """Hooks a fake install directory and a fake db into Spack."""
#    old_gpg_path = gpg_util.GNUPGHOME
#    orig_gpg_keys_path = spack.gpg_keys_path
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
#    spack.gpg_keys_path = spack.mock_gpg_keys_path
#    gpg_util.GNUPGHOME = str(tmpdir.join('gpg'))
    yield
    # Turn checksumming back on
    spack.do_checksum = True
    # Restore Spack's layout.
    spack.store.layout = layout
    spack.store.db = db
#    spack.gpg_keys_path = orig_gpg_keys_path
#    gpg_util.GNUPGHOME = old_gpg_path
    spack.stage_path = old_stage_path


def fake_fetchify(url, pkg):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(url))
    pkg.fetcher = fetcher


# def has_gnupg2():
#    try:
#        gpg_util.Gpg.gpg()('--version', output=os.devnull)
#        return True
#    except Exception:
#        return False


@pytest.mark.usefixtures('install_mockery')
def test_packaging(mock_archive, tmpdir):
    # tweak patchelf to only do a download
    spec = Spec("patchelf")
    spec.concretize()
    pkg = spack.repo.get(spec)
    fake_fetchify(pkg.fetcher, pkg)

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

    mirror_root = join_path(tmpdir, 'test-mirror')
    specs = [spec]
    spack.mirror.create(
        mirror_root, specs, no_checksum=True
    )

    # Create a build cache without signing
    bindist.build_tarball(spec, mirror_root,
                          force=False, rel=False, yes_to_all=True, key=None)

    # Validate the relocation information
    buildinfo = bindist.read_buildinfo_file(spec)
    assert(buildinfo['relocate_textfiles'] == ['dummy.txt'])

    # Create a build cache without signing, making rpaths relative first
    # overwriting previous build cache
    bindist.build_tarball(spec, mirror_root,
                          force=True, rel=True, yes_to_all=True, key=None)

# Import the default key.
#    gpgparser = argparse.ArgumentParser()
#    gpg.setup_parser(gpgparser)
#    args = gpgparser.parse_args(['init'])
#    args.import_dir = spack.mock_gpg_keys_path
#    gpg.gpg(gpgparser, args)
# Create a key for use in the tests.
#    keypath = tmpdir.join('testing-1.key')
#    args = gpgparser.parse_args(['create',
#                                 '--comment', 'Spack testing key',
#                                 '--export', str(keypath),
#                                 'Spack testing 1',
#                                 'spack@googlegroups.com'])
#    gpg.gpg(gpgparser, args)
#    keyfp = gpg_util.Gpg.signing_keys()[0]
#
#    bindist.build_tarball(spec, mirror_root,
#                          force=True, rel=False, yes_to_all=False, key=None)
#
#    keypath = tmpdir.join('testing-2.key')
#    args = gpgparser.parse_args(['create',
#                                 '--comment', 'Spack testing key 2',
#                                 '--export', str(keypath),
#                                 'Spack testing 2',
#                                 'spack@googlegroups.com'])
#    gpg.gpg(gpgparser, args)
#
#    bindist.build_tarball(spec, mirror_root,
#                          force=True, rel=False, yes_to_all=False, key=None)
#
#    bindist.build_tarball(spec, mirror_root,
#                          force=True, rel=False, yes_to_all=False, key=keyfp)
#
    # register mirror with spack config
    mirrors = {'spack-mirror-test': 'file://' + mirror_root}
    spack.config.update_config('mirrors', mirrors)

    # Uninstall the package
    pkg.do_uninstall(force=True)

    bindist.get_specs()
    bindist.get_keys()

    file = bindist.download_tarball(spec)
    bindist.extract_tarball(spec, file, True, True)
