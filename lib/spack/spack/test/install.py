##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import pytest
import spack
import spack.store
from spack.database import Database
from spack.directory_layout import YamlDirectoryLayout
from spack.fetch_strategy import URLFetchStrategy, FetchStrategyComposite
from spack.spec import Spec

import os


@pytest.fixture()
def install_mockery(tmpdir, config, builtin_mock):
    """Hooks a fake install directory and a fake db into Spack."""
    layout = spack.store.layout
    db = spack.store.db
    # Use a fake install directory to avoid conflicts bt/w
    # installed pkgs and mock packages.
    spack.store.layout = YamlDirectoryLayout(str(tmpdir))
    spack.store.db = Database(str(tmpdir))
    # We use a fake package, so skip the checksum.
    spack.do_checksum = False
    yield
    # Turn checksumming back on
    spack.do_checksum = True
    # Restore Spack's layout.
    spack.store.layout = layout
    spack.store.db = db


def fake_fetchify(url, pkg):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(url))
    pkg.fetcher = fetcher


@pytest.mark.usefixtures('install_mockery')
def test_install_and_uninstall(mock_archive):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    # Get the package
    pkg = spack.repo.get(spec)

    fake_fetchify(mock_archive.url, pkg)

    try:
        pkg.do_install()
        pkg.do_uninstall()
    except Exception:
        pkg.remove_prefix()
        raise


def mock_remove_prefix(*args):
    raise MockInstallError(
        "Intentional error",
        "Mock remove_prefix method intentionally fails")


@pytest.mark.usefixtures('install_mockery')
def test_partial_install(mock_archive):
    spec = Spec('canfail')
    spec.concretize()
    pkg = spack.repo.get(spec)
    fake_fetchify(mock_archive.url, pkg)
    remove_prefix = spack.package.Package.remove_prefix
    try:
        spack.package.Package.remove_prefix = mock_remove_prefix
        try:
            pkg.do_install()
        except MockInstallError:
            pass
        spack.package.Package.remove_prefix = remove_prefix
        setattr(pkg, 'succeed', True)
        pkg.do_install()
        assert pkg.installed
    finally:
        spack.package.Package.remove_prefix = remove_prefix
        try:
            delattr(pkg, 'succeed')
        except AttributeError:
            pass


@pytest.mark.usefixtures('install_mockery')
def test_partial_install_keep_prefix(mock_archive):
    spec = Spec('canfail')
    spec.concretize()
    pkg = spack.repo.get(spec)
    fake_fetchify(mock_archive.url, pkg)
    remove_prefix = spack.package.Package.remove_prefix
    try:
        spack.package.Package.remove_prefix = mock_remove_prefix
        try:
            pkg.do_install()
        except MockInstallError:
            pass
        # Don't repair remove_prefix at this point, set keep_prefix so that
        # Spack continues with a partial install
        setattr(pkg, 'succeed', True)
        pkg.do_install(keep_prefix=True)
        assert pkg.installed
    finally:
        spack.package.Package.remove_prefix = remove_prefix
        try:
            delattr(pkg, 'succeed')
        except AttributeError:
            pass


@pytest.mark.usefixtures('install_mockery')
def test_partial_install_keep_prefix_check_metadata(mock_archive):
    spec = Spec('canfail')
    spec.concretize()
    pkg = spack.repo.get(spec)
    fake_fetchify(mock_archive.url, pkg)
    remove_prefix = spack.package.Package.remove_prefix
    try:
        spack.package.Package.remove_prefix = mock_remove_prefix
        try:
            pkg.do_install()
        except MockInstallError:
            pass
        os.remove(spack.store.layout.spec_file_path(spec))
        spack.package.Package.remove_prefix = remove_prefix
        setattr(pkg, 'succeed', True)
        pkg.do_install(keep_prefix=True)
        assert pkg.installed
        spack.store.layout.check_metadata_consistency(spec)
    finally:
        spack.package.Package.remove_prefix = remove_prefix
        try:
            delattr(pkg, 'succeed')
        except AttributeError:
            pass


@pytest.mark.usefixtures('install_mockery')
def test_install_succeeds_but_db_add_fails(mock_archive):
    """If an installation succeeds but the database is not updated, make sure
       that the database is updated for a future install."""
    spec = Spec('cmake')
    spec.concretize()
    pkg = spack.repo.get(spec)
    fake_fetchify(mock_archive.url, pkg)
    remove_prefix = spack.package.Package.remove_prefix
    db_add = spack.store.db.add

    def mock_db_add(*args, **kwargs):
        raise MockInstallError(
            "Intentional error", "Mock db add method intentionally fails")

    try:
        spack.package.Package.remove_prefix = mock_remove_prefix
        spack.store.db.add = mock_db_add
        try:
            pkg.do_install()
        except MockInstallError:
            pass
        assert pkg.installed

        spack.package.Package.remove_prefix = remove_prefix
        spack.store.db.add = db_add
        pkg.do_install()
        assert spack.store.db.get_record(spec)
    except:
        spack.package.Package.remove_prefix = remove_prefix
        raise


@pytest.mark.usefixtures('install_mockery')
def test_store(mock_archive):
    spec = Spec('cmake-client').concretized()

    for s in spec.traverse():
        fake_fetchify(mock_archive.url, s.package)

    pkg = spec.package
    try:
        pkg.do_install()
    except Exception:
        pkg.remove_prefix()
        raise


@pytest.mark.usefixtures('install_mockery')
def test_failing_build(mock_archive):
    spec = Spec('failing-build').concretized()

    for s in spec.traverse():
        fake_fetchify(mock_archive.url, s.package)

    pkg = spec.package
    with pytest.raises(spack.build_environment.ChildError):
        pkg.do_install()


class MockInstallError(spack.error.SpackError):
    pass
