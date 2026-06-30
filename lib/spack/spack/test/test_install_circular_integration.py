# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
Integration tests for actual installation with circular run dependencies.
"""

import pytest

import spack.concretize
import spack.repo
import spack.store
from spack.new_installer import PackageInstaller
from spack.test.conftest import RepoBuilder


@pytest.mark.usefixtures("install_mockery", "mock_fetch")
class TestInstallCircularIntegration:
    """Integration tests for installing packages with circular run dependencies."""

    def test_install_simple_circular_run_deps(self, repo_builder: RepoBuilder):
        """Test actual installation with A↔B circular run dependencies."""
        repo_builder.add_package("install-circ-a", dependencies=[("install-circ-b", "run", None)])
        repo_builder.add_package("install-circ-b", dependencies=[("install-circ-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("install-circ-a")

            # Attempt installation
            installer = PackageInstaller([spec.package])
            installer.install()

            # Verify both were installed
            assert spec.installed
            assert spec["install-circ-b"].installed

            # Verify both in database
            db = spack.store.STORE.db
            found_a = db.query_one("install-circ-a")
            found_b = db.query_one("install-circ-b")

            assert found_a is not None
            assert found_b is not None

    def test_install_mixed_circular_deps(self, repo_builder: RepoBuilder):
        """Test A→B (link), B→A (run) - should install B first, then A."""
        repo_builder.add_package("mixed-inst-a", dependencies=[("mixed-inst-b", "link", None)])
        repo_builder.add_package("mixed-inst-b", dependencies=[("mixed-inst-a", "run", None)])

        with spack.repo.use_repositories(repo_builder.root):
            spec = spack.concretize.concretize_one("mixed-inst-a")

            installer = PackageInstaller([spec.package])
            installer.install()

            # Both should be installed
            assert spec.installed
            assert spec["mixed-inst-b"].installed

            # Verify in database
            db = spack.store.STORE.db
            assert db.query_one("mixed-inst-a") is not None
            assert db.query_one("mixed-inst-b") is not None
