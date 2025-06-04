# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import importlib
import os
import pathlib
import sys

import pytest

import spack.concretize
import spack.directives
import spack.error
import spack.fetch_strategy
import spack.package_base
import spack.repo
from spack.paths import mock_packages_path
from spack.spec import Spec
from spack.util.naming import pkg_name_to_class_name
from spack.version import VersionChecksumError


class MyPrependFileLoader(spack.repo._PrependFileLoader):
    """Skip explicit prepending of 'spack_repo.builtin.build_systems' import."""

    def __init__(self, fullname, repo, package_name):
        super().__init__(fullname, repo, package_name)
        self.prepend = b""


def pkg_factory(name):
    """Return a package object tied to an abstract spec"""
    pkg_cls = spack.repo.PATH.get_pkg_class(name)
    return pkg_cls(Spec(name))


@pytest.mark.usefixtures("config", "mock_packages")
class TestPackage:
    def test_load_package(self):
        spack.repo.PATH.get_pkg_class("mpich")

    def test_package_name(self):
        pkg_cls = spack.repo.PATH.get_pkg_class("mpich")
        assert pkg_cls.name == "mpich"

    def test_package_filename(self):
        repo = spack.repo.from_path(mock_packages_path)
        filename = repo.filename_for_package_name("mpich")
        assert filename == os.path.join(mock_packages_path, "packages", "mpich", "package.py")

    def test_nonexisting_package_filename(self):
        repo = spack.repo.from_path(mock_packages_path)
        filename = repo.filename_for_package_name("some-nonexisting-package")
        assert filename == os.path.join(
            mock_packages_path, "packages", "some_nonexisting_package", "package.py"
        )

    def test_package_class_names(self):
        assert "Mpich" == pkg_name_to_class_name("mpich")
        assert "PmgrCollective" == pkg_name_to_class_name("pmgr_collective")
        assert "PmgrCollective" == pkg_name_to_class_name("pmgr-collective")
        assert "Pmgrcollective" == pkg_name_to_class_name("PmgrCollective")
        assert "_3db" == pkg_name_to_class_name("3db")
        assert "_True" == pkg_name_to_class_name("true")  # reserved keyword
        assert "_False" == pkg_name_to_class_name("false")  # reserved keyword
        assert "_None" == pkg_name_to_class_name("none")  # reserved keyword
        assert "Finally" == pkg_name_to_class_name("finally")  # `Finally` is not reserved

    # Below tests target direct imports of spack packages from the spack.pkg namespace
    def test_import_package(self, tmp_path: pathlib.Path, monkeypatch):
        monkeypatch.setattr(spack.repo, "_PrependFileLoader", MyPrependFileLoader)
        root, _ = spack.repo.create_repo(str(tmp_path), "testing_repo", package_api=(1, 0))
        pkg_path = pathlib.Path(root) / "packages" / "mpich" / "package.py"
        pkg_path.parent.mkdir(parents=True)
        pkg_path.write_text("foo = 1")

        with spack.repo.use_repositories(root):
            importlib.import_module("spack.pkg.testing_repo")
            assert importlib.import_module("spack.pkg.testing_repo.mpich").foo == 1

        del sys.modules["spack.pkg.testing_repo"]
        del sys.modules["spack.pkg.testing_repo.mpich"]

    def test_inheritance_of_directives(self):
        pkg_cls = spack.repo.PATH.get_pkg_class("simple-inheritance")

        # Check dictionaries that should have been filled by directives
        dependencies = pkg_cls.dependencies_by_name()
        assert len(dependencies) == 4
        assert "cmake" in dependencies
        assert "openblas" in dependencies
        assert "mpi" in dependencies
        assert len(pkg_cls.provided) == 2

        # Check that Spec instantiation behaves as we expect
        s = spack.concretize.concretize_one("simple-inheritance")
        assert "^cmake" in s
        assert "^openblas" in s
        assert "+openblas" in s
        assert "mpi" in s

        s = spack.concretize.concretize_one("simple-inheritance~openblas")
        assert "^cmake" in s
        assert "^openblas" not in s
        assert "~openblas" in s
        assert "mpi" in s

    @pytest.mark.regression("11844")
    def test_inheritance_of_patches(self):
        # Will error if inheritor package cannot find inherited patch files
        _ = spack.concretize.concretize_one("patch-inheritance")


@pytest.mark.regression("2737")
def test_urls_for_versions(mock_packages, config):
    """Version directive without a 'url' argument should use default url."""
    for spec_str in ("url-override@0.9.0", "url-override@1.0.0"):
        s = spack.concretize.concretize_one(spec_str)
        url = s.package.url_for_version("0.9.0")
        assert url == "http://www.anothersite.org/uo-0.9.0.tgz"

        url = s.package.url_for_version("1.0.0")
        assert url == "http://www.doesnotexist.org/url_override-1.0.0.tar.gz"

        url = s.package.url_for_version("0.8.1")
        assert url == "http://www.doesnotexist.org/url_override-0.8.1.tar.gz"


def test_url_for_version_with_no_urls(mock_packages, config):
    spec = Spec("git-test")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    with pytest.raises(spack.error.NoURLError):
        pkg_cls(spec).url_for_version("1.0")

    with pytest.raises(spack.error.NoURLError):
        pkg_cls(spec).url_for_version("1.1")


@pytest.mark.skip(reason="spack.build_systems moved out of spack/spack")
def test_custom_cmake_prefix_path(mock_packages, config):
    pass
    # spec = spack.concretize.concretize_one("depends-on-define-cmake-prefix-paths")
    # assert spack.build_systems.cmake.get_cmake_prefix_path(spec.package) == [
    #     spec["define-cmake-prefix-paths"].prefix.test
    # ]


def test_url_for_version_with_only_overrides(mock_packages, config):
    s = spack.concretize.concretize_one("url-only-override")

    # these exist and should just take the URL provided in the package
    assert s.package.url_for_version("1.0.0") == "http://a.example.com/url_override-1.0.0.tar.gz"
    assert s.package.url_for_version("0.9.0") == "http://b.example.com/url_override-0.9.0.tar.gz"
    assert s.package.url_for_version("0.8.1") == "http://c.example.com/url_override-0.8.1.tar.gz"

    # these don't exist but should still work, even if there are only overrides
    assert s.package.url_for_version("1.0.5") == "http://a.example.com/url_override-1.0.5.tar.gz"
    assert s.package.url_for_version("0.9.5") == "http://b.example.com/url_override-0.9.5.tar.gz"
    assert s.package.url_for_version("0.8.5") == "http://c.example.com/url_override-0.8.5.tar.gz"
    assert s.package.url_for_version("0.7.0") == "http://c.example.com/url_override-0.7.0.tar.gz"


def test_url_for_version_with_only_overrides_with_gaps(mock_packages, config):
    s = spack.concretize.concretize_one("url-only-override-with-gaps")

    # same as for url-only-override -- these are specific
    assert s.package.url_for_version("1.0.0") == "http://a.example.com/url_override-1.0.0.tar.gz"
    assert s.package.url_for_version("0.9.0") == "http://b.example.com/url_override-0.9.0.tar.gz"
    assert s.package.url_for_version("0.8.1") == "http://c.example.com/url_override-0.8.1.tar.gz"

    # these don't have specific URLs, but should still work by extrapolation
    assert s.package.url_for_version("1.0.5") == "http://a.example.com/url_override-1.0.5.tar.gz"
    assert s.package.url_for_version("0.9.5") == "http://b.example.com/url_override-0.9.5.tar.gz"
    assert s.package.url_for_version("0.8.5") == "http://c.example.com/url_override-0.8.5.tar.gz"
    assert s.package.url_for_version("0.7.0") == "http://c.example.com/url_override-0.7.0.tar.gz"


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "spec_str,expected_type,expected_url",
    [
        (
            "git-top-level",
            spack.fetch_strategy.GitFetchStrategy,
            "https://example.com/some/git/repo",
        ),
        (
            "svn-top-level",
            spack.fetch_strategy.SvnFetchStrategy,
            "https://example.com/some/svn/repo",
        ),
        ("hg-top-level", spack.fetch_strategy.HgFetchStrategy, "https://example.com/some/hg/repo"),
    ],
)
def test_fetcher_url(spec_str, expected_type, expected_url):
    """Ensure that top-level git attribute can be used as a default."""
    fetcher = spack.fetch_strategy.for_package_version(pkg_factory(spec_str), "1.0")
    assert isinstance(fetcher, expected_type)
    assert fetcher.url == expected_url


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "spec_str,version_str,exception_type",
    [
        # Non-url-package
        ("git-top-level", "1.1", spack.fetch_strategy.ExtrapolationError),
        # Two VCS specified together
        ("git-url-svn-top-level", "1.0", spack.fetch_strategy.FetcherConflict),
        ("git-svn-top-level", "1.0", spack.fetch_strategy.FetcherConflict),
    ],
)
def test_fetcher_errors(spec_str, version_str, exception_type):
    """Verify that we can't extrapolate versions for non-URL packages."""
    with pytest.raises(exception_type):
        spack.fetch_strategy.for_package_version(pkg_factory(spec_str), version_str)


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "version_str,expected_url,digest",
    [
        ("2.0", "https://example.com/some/tarball-2.0.tar.gz", "20"),
        ("2.1", "https://example.com/some/tarball-2.1.tar.gz", "21"),
        ("2.2", "https://www.example.com/foo2.2.tar.gz", "22"),
        ("2.3", "https://www.example.com/foo2.3.tar.gz", "23"),
    ],
)
def test_git_url_top_level_url_versions(version_str, expected_url, digest):
    """Test URL fetch strategy inference when url is specified with git."""
    # leading 62 zeros of sha256 hash
    leading_zeros = "0" * 62

    fetcher = spack.fetch_strategy.for_package_version(
        pkg_factory("git-url-top-level"), version_str
    )
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.url == expected_url
    assert fetcher.digest == leading_zeros + digest


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "version_str,tag,commit,branch",
    [
        ("3.0", "v3.0", None, None),
        ("3.1", "v3.1", "abc31", None),
        ("3.2", None, None, "releases/v3.2"),
        ("3.3", None, "abc33", "releases/v3.3"),
        ("3.4", None, "abc34", None),
        ("submodules", None, None, None),
        ("develop", None, None, "develop"),
    ],
)
def test_git_url_top_level_git_versions(version_str, tag, commit, branch):
    """Test git fetch strategy inference when url is specified with git."""
    fetcher = spack.fetch_strategy.for_package_version(
        pkg_factory("git-url-top-level"), version_str
    )
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert fetcher.url == "https://example.com/some/git/repo"
    assert fetcher.tag == tag
    assert fetcher.commit == commit
    assert fetcher.branch == branch
    assert fetcher.url == pkg_factory("git-url-top-level").git


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize("version_str", ["1.0", "1.1", "1.2", "1.3"])
def test_git_url_top_level_conflicts(version_str):
    """Test git fetch strategy inference when url is specified with git."""
    with pytest.raises(spack.fetch_strategy.FetcherConflict):
        spack.fetch_strategy.for_package_version(pkg_factory("git-url-top-level"), version_str)


def test_rpath_args(mutable_database):
    """Test a package's rpath_args property."""

    rec = mutable_database.get_record("mpich")

    rpath_args = rec.spec.package.rpath_args
    assert "-rpath" in rpath_args
    assert "mpich" in rpath_args


def test_bundle_version_checksum(mock_directive_bundle, clear_directive_functions):
    """Test raising exception on a version checksum with a bundle package."""
    with pytest.raises(VersionChecksumError, match="Checksums not allowed"):
        version = spack.directives.version("1.0", checksum="1badpkg")
        version(mock_directive_bundle)


def test_bundle_patch_directive(mock_directive_bundle, clear_directive_functions):
    """Test raising exception on a patch directive with a bundle package."""
    with pytest.raises(
        spack.directives.UnsupportedPackageDirective, match="Patches are not allowed"
    ):
        patch = spack.directives.patch("mock/patch.txt")
        patch(mock_directive_bundle)


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "version_str,digest_end,extra_options",
    [
        ("1.0", "10", {"timeout": 42, "cookie": "foobar"}),
        ("1.1", "11", {"timeout": 65}),
        ("1.2", "12", {"cookie": "baz"}),
    ],
)
def test_fetch_options(version_str, digest_end, extra_options):
    """Test fetch options inference."""
    leading_zeros = "000000000000000000000000000000"
    fetcher = spack.fetch_strategy.for_package_version(pkg_factory("fetch-options"), version_str)
    assert isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy)
    assert fetcher.digest == leading_zeros + digest_end
    assert fetcher.extra_options == extra_options


def test_package_deprecated_version(mock_packages, mock_fetch, mock_stage):
    spec = Spec("deprecated-versions")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)

    assert spack.package_base.deprecated_version(pkg_cls, "1.1.0")
    assert not spack.package_base.deprecated_version(pkg_cls, "1.0.0")


def test_package_can_have_sparse_checkout_properties(mock_packages, mock_fetch, mock_stage):
    spec = Spec("git-sparsepaths-pkg")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    assert hasattr(pkg_cls, "git_sparse_paths")

    fetcher = spack.fetch_strategy.for_package_version(pkg_cls(spec), "1.0")
    assert isinstance(fetcher, spack.fetch_strategy.GitFetchStrategy)
    assert hasattr(fetcher, "git_sparse_paths")
    assert fetcher.git_sparse_paths == pkg_cls.git_sparse_paths


def test_package_can_depend_on_commit_of_dependency(mock_packages, config):
    spec = spack.concretize.concretize_one(Spec("git-ref-commit-dep@1.0.0"))
    assert spec.satisfies(f"^git-ref-package commit={'a' * 40}")
    assert "surgical" not in spec["git-ref-package"].variants


def test_package_condtional_variants_may_depend_on_commit(mock_packages, config):
    spec = spack.concretize.concretize_one(Spec("git-ref-commit-dep@develop"))
    assert spec.satisfies(f"^git-ref-package commit={'b' * 40}")
    conditional_variant = spec["git-ref-package"].variants.get("surgical", None)
    assert conditional_variant
    assert conditional_variant.value


def test_commit_variant_finds_matches_for_commit_versions(mock_packages, config):
    """
    test conditional dependence on `when='commit=<sha>'`
    git-ref-commit-dep variant commit-selector depends on a specific commit of git-ref-package
    that commit is associated with the stable version of git-ref-package
    """
    spec = spack.concretize.concretize_one(Spec("git-ref-commit-dep+commit-selector"))
    assert spec.satisfies(f"^git-ref-package commit={'c' * 40}")


def test_pkg_name_can_only_be_derived_when_package_module():
    """When the module prefix is not spack_repo (or legacy spack.pkg) we cannot derive
    a package name."""
    ExamplePackage = type(
        "ExamplePackage",
        (spack.package_base.PackageBase,),
        {"__module__": "not.a.spack.repo.packages.example_package.package"},
    )

    with pytest.raises(ValueError, match="Package ExamplePackage is not a known Spack package"):
        ExamplePackage.name
