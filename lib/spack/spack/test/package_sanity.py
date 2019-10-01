# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This test does sanity checks on Spack's builtin package database."""
import re

import pytest

import spack.paths
import spack.repo
import spack.fetch_strategy


def check_repo():
    """Get all packages in the builtin repo to make sure they work."""
    for name in spack.repo.all_package_names():
        spack.repo.get(name)


@pytest.mark.maybeslow
def test_get_all_packages():
    """Get all packages once and make sure that works."""
    check_repo()


def test_get_all_mock_packages():
    """Get the mock packages once each too."""
    db = spack.repo.RepoPath(spack.paths.mock_packages_path)
    with spack.repo.swap(db):
        check_repo()


def test_all_versions_are_lowercase():
    """Spack package names must be lowercase, and use `-` instead of `_`."""
    errors = []
    for name in spack.repo.all_package_names():
        if re.search(r'[_A-Z]', name):
            errors.append(name)

    assert len(errors) == 0


def test_all_virtual_packages_have_default_providers():
    """All virtual packages must have a default provider explicitly set."""
    defaults = spack.config.get('packages', scope='defaults')
    default_providers = defaults['all']['providers']
    providers = spack.repo.path.provider_index.providers
    default_providers_filename = \
        spack.config.config.scopes['defaults'].get_section_filename('packages')
    for provider in providers:
        assert provider in default_providers, \
            "all providers must have a default in %s" \
            % default_providers_filename


def test_package_version_consistency():
    """Make sure all versions on builtin packages produce a fetcher."""
    for name in spack.repo.all_package_names():
        pkg = spack.repo.get(name)
        spack.fetch_strategy.check_pkg_attributes(pkg)
        for version in pkg.versions:
            assert spack.fetch_strategy.for_package_version(pkg, version)


def test_no_fixme():
    """Packages should not contain any boilerplate such as
       FIXME or example.com."""
    errors = []
    fixme_regexes = [
        r'remove this boilerplate',
        r'FIXME: Put',
        r'FIXME: Add',
        r'example.com',
    ]
    for name in spack.repo.all_package_names():
        filename = spack.repo.path.filename_for_package_name(name)
        with open(filename, 'r') as package_file:
            for i, line in enumerate(package_file):
                pattern = next((r for r in fixme_regexes
                                if re.search(r, line)), None)
                if pattern:
                    errors.append(
                        "%s:%d: boilerplate needs to be removed: %s" %
                        (filename, i, line.strip())
                    )
            assert [] == errors


def test_docstring():
    """Ensure that every package has a docstring."""

    for name in spack.repo.all_package_names():
        pkg = spack.repo.get(name)
        assert pkg.__doc__
