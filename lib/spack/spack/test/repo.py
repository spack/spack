# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import pytest

import spack.package_base
import spack.paths
import spack.repo


@pytest.fixture()
def extra_repo(tmpdir_factory):
    repo_namespace = "extra_test_repo"
    repo_dir = tmpdir_factory.mktemp(repo_namespace)
    repo_dir.ensure("packages", dir=True)

    with open(str(repo_dir.join("repo.yaml")), "w") as f:
        f.write(
            """
repo:
  namespace: extra_test_repo
"""
        )
    return spack.repo.Repo(str(repo_dir))


def test_repo_getpkg(mutable_mock_repo):
    mutable_mock_repo.get_pkg_class("a")
    mutable_mock_repo.get_pkg_class("builtin.mock.a")


def test_repo_multi_getpkg(mutable_mock_repo, extra_repo):
    mutable_mock_repo.put_first(extra_repo)
    mutable_mock_repo.get_pkg_class("a")
    mutable_mock_repo.get_pkg_class("builtin.mock.a")


def test_repo_multi_getpkgclass(mutable_mock_repo, extra_repo):
    mutable_mock_repo.put_first(extra_repo)
    mutable_mock_repo.get_pkg_class("a")
    mutable_mock_repo.get_pkg_class("builtin.mock.a")


def test_repo_pkg_with_unknown_namespace(mutable_mock_repo):
    with pytest.raises(spack.repo.UnknownNamespaceError):
        mutable_mock_repo.get_pkg_class("unknown.a")


def test_repo_unknown_pkg(mutable_mock_repo):
    with pytest.raises(spack.repo.UnknownPackageError):
        mutable_mock_repo.get_pkg_class("builtin.mock.nonexistentpackage")


@pytest.mark.maybeslow
def test_repo_last_mtime():
    latest_mtime = max(
        os.path.getmtime(p.module.__file__) for p in spack.repo.path.all_package_classes()
    )
    assert spack.repo.path.last_mtime() == latest_mtime


def test_repo_invisibles(mutable_mock_repo, extra_repo):
    with open(os.path.join(extra_repo.root, "packages", ".invisible"), "w"):
        pass
    extra_repo.all_package_names()


@pytest.mark.parametrize("attr_name,exists", [("cmake", True), ("__sphinx_mock__", False)])
@pytest.mark.regression("20661")
def test_namespace_hasattr(attr_name, exists, mutable_mock_repo):
    # Check that we don't fail on 'hasattr' checks because
    # of a custom __getattr__ implementation
    nms = spack.repo.SpackNamespace("spack.pkg.builtin.mock")
    assert hasattr(nms, attr_name) == exists


@pytest.mark.regression("24552")
def test_all_package_names_is_cached_correctly():
    assert "mpi" in spack.repo.all_package_names(include_virtuals=True)
    assert "mpi" not in spack.repo.all_package_names(include_virtuals=False)


@pytest.mark.regression("29203")
def test_use_repositories_doesnt_change_class():
    """Test that we don't create the same package module and class multiple times
    when swapping repositories.
    """
    zlib_cls_outer = spack.repo.path.get_pkg_class("zlib")
    current_paths = [r.root for r in spack.repo.path.repos]
    with spack.repo.use_repositories(*current_paths):
        zlib_cls_inner = spack.repo.path.get_pkg_class("zlib")
    assert id(zlib_cls_inner) == id(zlib_cls_outer)


def test_import_repo_prefixes_as_python_modules(mock_packages):
    import spack.pkg.builtin.mock

    assert isinstance(spack.pkg, spack.repo.SpackNamespace)
    assert isinstance(spack.pkg.builtin, spack.repo.SpackNamespace)
    assert isinstance(spack.pkg.builtin.mock, spack.repo.SpackNamespace)


def test_absolute_import_spack_packages_as_python_modules(mock_packages):
    import spack.pkg.builtin.mock.mpileaks

    assert hasattr(spack.pkg.builtin.mock, "mpileaks")
    assert hasattr(spack.pkg.builtin.mock.mpileaks, "Mpileaks")
    assert isinstance(spack.pkg.builtin.mock.mpileaks.Mpileaks, spack.package_base.PackageMeta)
    assert issubclass(spack.pkg.builtin.mock.mpileaks.Mpileaks, spack.package_base.PackageBase)


def test_relative_import_spack_packages_as_python_modules(mock_packages):
    from spack.pkg.builtin.mock.mpileaks import Mpileaks

    assert isinstance(Mpileaks, spack.package_base.PackageMeta)
    assert issubclass(Mpileaks, spack.package_base.PackageBase)


def test_all_virtual_packages_have_default_providers():
    """All virtual packages must have a default provider explicitly set."""
    defaults = spack.config.get("packages", scope="defaults")
    default_providers = defaults["all"]["providers"]
    providers = spack.repo.path.provider_index.providers
    default_providers_filename = spack.config.config.scopes["defaults"].get_section_filename(
        "packages"
    )
    for provider in providers:
        assert provider in default_providers, (
            "all providers must have a default in %s" % default_providers_filename
        )


def test_get_all_mock_packages(mock_packages):
    """Get the mock packages once each too."""
    for name in mock_packages.all_package_names():
        mock_packages.get_pkg_class(name)


def test_repo_path_handles_package_removal(tmpdir, mock_packages):
    builder = spack.repo.MockRepositoryBuilder(tmpdir, namespace="removal")
    builder.add_package("c")
    with spack.repo.use_repositories(builder.root, override=False) as repos:
        r = repos.repo_for_pkg("c")
        assert r.namespace == "removal"

    builder.remove("c")
    with spack.repo.use_repositories(builder.root, override=False) as repos:
        r = repos.repo_for_pkg("c")
        assert r.namespace == "builtin.mock"
