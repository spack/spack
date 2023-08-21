# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.store
from spack.database import InstallStatuses
from spack.main import SpackCommand

install = SpackCommand("install")
uninstall = SpackCommand("uninstall")
deprecate = SpackCommand("deprecate")
find = SpackCommand("find")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


def test_deprecate(mock_packages, mock_archive, mock_fetch, install_mockery):
    install("libelf@0.8.13")
    install("libelf@0.8.10")

    all_installed = spack.store.STORE.db.query()
    assert len(all_installed) == 2

    deprecate("-y", "libelf@0.8.10", "libelf@0.8.13")

    non_deprecated = spack.store.STORE.db.query()
    all_available = spack.store.STORE.db.query(installed=any)
    assert all_available == all_installed
    assert non_deprecated == spack.store.STORE.db.query("libelf@0.8.13")


def test_deprecate_fails_no_such_package(mock_packages, mock_archive, mock_fetch, install_mockery):
    """Tests that deprecating a spec that is not installed fails.

    Tests that deprecating without the ``-i`` option in favor of a spec that
    is not installed fails."""
    output = deprecate("-y", "libelf@0.8.10", "libelf@0.8.13", fail_on_error=False)
    assert "Spec 'libelf@0.8.10' matches no installed packages" in output

    install("libelf@0.8.10")

    output = deprecate("-y", "libelf@0.8.10", "libelf@0.8.13", fail_on_error=False)
    assert "Spec 'libelf@0.8.13' matches no installed packages" in output


def test_deprecate_install(mock_packages, mock_archive, mock_fetch, install_mockery):
    """Tests that the ```-i`` option allows us to deprecate in favor of a spec
    that is not yet installed."""
    install("libelf@0.8.10")

    to_deprecate = spack.store.STORE.db.query()
    assert len(to_deprecate) == 1

    deprecate("-y", "-i", "libelf@0.8.10", "libelf@0.8.13")

    non_deprecated = spack.store.STORE.db.query()
    deprecated = spack.store.STORE.db.query(installed=InstallStatuses.DEPRECATED)
    assert deprecated == to_deprecate
    assert len(non_deprecated) == 1
    assert non_deprecated[0].satisfies("libelf@0.8.13")


def test_deprecate_deps(mock_packages, mock_archive, mock_fetch, install_mockery):
    """Test that the deprecate command deprecates all dependencies properly."""
    install("libdwarf@20130729 ^libelf@0.8.13")
    install("libdwarf@20130207 ^libelf@0.8.10")

    new_spec = spack.spec.Spec("libdwarf@20130729^libelf@0.8.13").concretized()
    old_spec = spack.spec.Spec("libdwarf@20130207^libelf@0.8.10").concretized()

    all_installed = spack.store.STORE.db.query()

    deprecate("-y", "-d", "libdwarf@20130207", "libdwarf@20130729")

    non_deprecated = spack.store.STORE.db.query()
    all_available = spack.store.STORE.db.query(installed=any)
    deprecated = spack.store.STORE.db.query(installed=InstallStatuses.DEPRECATED)

    assert all_available == all_installed
    assert sorted(all_available) == sorted(deprecated + non_deprecated)

    assert sorted(non_deprecated) == sorted(list(new_spec.traverse()))
    assert sorted(deprecated) == sorted(list(old_spec.traverse()))


def test_uninstall_deprecated(mock_packages, mock_archive, mock_fetch, install_mockery):
    """Tests that we can still uninstall deprecated packages."""
    install("libelf@0.8.13")
    install("libelf@0.8.10")

    deprecate("-y", "libelf@0.8.10", "libelf@0.8.13")

    non_deprecated = spack.store.STORE.db.query()

    uninstall("-y", "libelf@0.8.10")

    assert spack.store.STORE.db.query() == spack.store.STORE.db.query(installed=any)
    assert spack.store.STORE.db.query() == non_deprecated


def test_deprecate_already_deprecated(mock_packages, mock_archive, mock_fetch, install_mockery):
    """Tests that we can re-deprecate a spec to change its deprecator."""
    install("libelf@0.8.13")
    install("libelf@0.8.12")
    install("libelf@0.8.10")

    deprecated_spec = spack.spec.Spec("libelf@0.8.10").concretized()

    deprecate("-y", "libelf@0.8.10", "libelf@0.8.12")

    deprecator = spack.store.STORE.db.deprecator(deprecated_spec)
    assert deprecator == spack.spec.Spec("libelf@0.8.12").concretized()

    deprecate("-y", "libelf@0.8.10", "libelf@0.8.13")

    non_deprecated = spack.store.STORE.db.query()
    all_available = spack.store.STORE.db.query(installed=any)
    assert len(non_deprecated) == 2
    assert len(all_available) == 3

    deprecator = spack.store.STORE.db.deprecator(deprecated_spec)
    assert deprecator == spack.spec.Spec("libelf@0.8.13").concretized()


def test_deprecate_deprecator(mock_packages, mock_archive, mock_fetch, install_mockery):
    """Tests that when a deprecator spec is deprecated, its deprecatee specs
    are updated to point to the new deprecator."""
    install("libelf@0.8.13")
    install("libelf@0.8.12")
    install("libelf@0.8.10")

    first_deprecated_spec = spack.spec.Spec("libelf@0.8.10").concretized()
    second_deprecated_spec = spack.spec.Spec("libelf@0.8.12").concretized()
    final_deprecator = spack.spec.Spec("libelf@0.8.13").concretized()

    deprecate("-y", "libelf@0.8.10", "libelf@0.8.12")

    deprecator = spack.store.STORE.db.deprecator(first_deprecated_spec)
    assert deprecator == second_deprecated_spec

    deprecate("-y", "libelf@0.8.12", "libelf@0.8.13")

    non_deprecated = spack.store.STORE.db.query()
    all_available = spack.store.STORE.db.query(installed=any)
    assert len(non_deprecated) == 1
    assert len(all_available) == 3

    first_deprecator = spack.store.STORE.db.deprecator(first_deprecated_spec)
    assert first_deprecator == final_deprecator
    second_deprecator = spack.store.STORE.db.deprecator(second_deprecated_spec)
    assert second_deprecator == final_deprecator


def test_concretize_deprecated(mock_packages, mock_archive, mock_fetch, install_mockery):
    """Tests that the concretizer throws an error if we concretize to a
    deprecated spec"""
    install("libelf@0.8.13")
    install("libelf@0.8.10")

    deprecate("-y", "libelf@0.8.10", "libelf@0.8.13")

    spec = spack.spec.Spec("libelf@0.8.10")
    with pytest.raises(spack.spec.SpecDeprecatedError):
        spec.concretize()
