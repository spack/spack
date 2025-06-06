# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test class methods on PackageBase objects.

This doesn't include methods on package *instances* (like do_patch(),
etc.).  Only methods like ``possible_dependencies()`` that deal with the
static DSL metadata for packages.
"""

import os
import shutil

import pytest

import llnl.util.filesystem as fs

import spack.binary_distribution
import spack.concretize
import spack.deptypes as dt
import spack.error
import spack.install_test
import spack.package_base
import spack.spec
import spack.store
import spack.subprocess_context
import spack.util.git
from spack.error import InstallError
from spack.package_base import PackageBase
from spack.solver.input_analysis import NoStaticAnalysis, StaticAnalysis


@pytest.fixture(scope="module")
def compiler_names(mock_packages_repo):
    return [spec.name for spec in mock_packages_repo.providers_for("c")]


@pytest.fixture()
def mpileaks_possible_deps(mock_packages, mpi_names, compiler_names):
    possible = {
        "callpath": set(["dyninst"] + mpi_names + compiler_names),
        "low-priority-provider": set(),
        "dyninst": set(["libdwarf", "libelf"] + compiler_names),
        "fake": set(),
        "gcc": set(compiler_names),
        "intel-parallel-studio": set(),
        "libdwarf": set(["libelf"] + compiler_names),
        "libelf": set(compiler_names),
        "llvm": {"gcc", "llvm"},
        "mpich": set(compiler_names),
        "mpich2": set(compiler_names),
        "mpileaks": set(["callpath"] + mpi_names + compiler_names),
        "multi-provider-mpi": set(),
        "zmpi": set(["fake"] + compiler_names),
    }
    return possible


@pytest.fixture(params=[NoStaticAnalysis, StaticAnalysis])
def mock_inspector(config, mock_packages, request):
    inspector_cls = request.param
    if inspector_cls is NoStaticAnalysis:
        return inspector_cls(configuration=config, repo=mock_packages)
    return inspector_cls(
        configuration=config,
        repo=mock_packages,
        store=spack.store.STORE,
        binary_index=spack.binary_distribution.BINARY_INDEX,
    )


@pytest.fixture
def mpi_names(mock_inspector):
    return [spec.name for spec in mock_inspector.providers_for("mpi")]


@pytest.mark.parametrize(
    "pkg_name,fn_kwargs,expected",
    [
        (
            "mpileaks",
            {"expand_virtuals": True, "allowed_deps": dt.ALL},
            {
                "fake",
                "mpileaks",
                "gcc",
                "llvm",
                "multi-provider-mpi",
                "callpath",
                "dyninst",
                "mpich2",
                "libdwarf",
                "zmpi",
                "low-priority-provider",
                "intel-parallel-studio",
                "mpich",
                "libelf",
            },
        ),
        (
            "mpileaks",
            {"expand_virtuals": False, "allowed_deps": dt.ALL},
            {"callpath", "dyninst", "libdwarf", "libelf", "mpileaks"},
        ),
        (
            "mpileaks",
            {"expand_virtuals": False, "allowed_deps": dt.ALL, "transitive": False},
            {"callpath", "mpileaks"},
        ),
        ("dtbuild1", {"allowed_deps": dt.LINK | dt.RUN}, {"dtbuild1", "dtrun2", "dtlink2"}),
        ("dtbuild1", {"allowed_deps": dt.BUILD}, {"dtbuild1", "dtbuild2", "dtlink2"}),
        ("dtbuild1", {"allowed_deps": dt.LINK}, {"dtbuild1", "dtlink2"}),
    ],
)
def test_possible_dependencies(pkg_name, fn_kwargs, expected, mock_inspector):
    """Tests possible nodes of mpileaks, under different scenarios."""
    result, *_ = mock_inspector.possible_dependencies(pkg_name, **fn_kwargs)
    assert expected == result


def test_possible_dependencies_virtual(mock_inspector, mock_packages, mpi_names):
    expected = set(mpi_names)
    for name in mpi_names:
        expected.update(
            dep
            for dep in mock_packages.get_pkg_class(name).dependencies_by_name()
            if not mock_packages.is_virtual(dep)
        )
    expected.update(s.name for s in mock_packages.providers_for("c"))

    real_pkgs, *_ = mock_inspector.possible_dependencies(
        "mpi", transitive=False, allowed_deps=dt.ALL
    )
    assert expected == real_pkgs


def test_possible_dependencies_missing(mock_inspector):
    result, *_ = mock_inspector.possible_dependencies("missing-dependency", allowed_deps=dt.ALL)
    assert "this-is-a-missing-dependency" not in result


def test_possible_dependencies_with_multiple_classes(
    mock_inspector, mock_packages, mpileaks_possible_deps
):
    pkgs = ["dt-diamond", "mpileaks"]
    expected = set(mpileaks_possible_deps)
    expected.update({"dt-diamond", "dt-diamond-left", "dt-diamond-right", "dt-diamond-bottom"})

    real_pkgs, *_ = mock_inspector.possible_dependencies(*pkgs, allowed_deps=dt.ALL)
    assert set(expected) == real_pkgs


def setup_install_test(source_paths, test_root):
    """
    Set up the install test by creating sources and install test roots.

    The convention used here is to create an empty file if the path name
    ends with an extension otherwise, a directory is created.
    """
    fs.mkdirp(test_root)
    for path in source_paths:
        if os.path.splitext(path)[1]:
            fs.touchp(path)
        else:
            fs.mkdirp(path)


@pytest.mark.parametrize(
    "spec,sources,extras,expect",
    [
        (
            "pkg-a",
            ["example/a.c"],  # Source(s)
            ["example/a.c"],  # Extra test source
            ["example/a.c"],
        ),  # Test install dir source(s)
        (
            "pkg-b",
            ["test/b.cpp", "test/b.hpp", "example/b.txt"],  # Source(s)
            ["test"],  # Extra test source
            ["test/b.cpp", "test/b.hpp"],
        ),  # Test install dir source
        (
            "pkg-c",
            ["examples/a.py", "examples/b.py", "examples/c.py", "tests/d.py"],
            ["examples/b.py", "tests"],
            ["examples/b.py", "tests/d.py"],
        ),
    ],
)
def test_cache_extra_sources(install_mockery, spec, sources, extras, expect):
    """Test the package's cache extra test sources helper function."""
    s = spack.concretize.concretize_one(spec)

    source_path = s.package.stage.source_path
    srcs = [fs.join_path(source_path, src) for src in sources]
    test_root = spack.install_test.install_test_root(s.package)
    setup_install_test(srcs, test_root)

    emsg_dir = "Expected {0} to be a directory"
    emsg_file = "Expected {0} to be a file"
    for src in srcs:
        assert os.path.exists(src), "Expected {0} to exist".format(src)
        if os.path.splitext(src)[1]:
            assert os.path.isfile(src), emsg_file.format(src)
        else:
            assert os.path.isdir(src), emsg_dir.format(src)

    spack.install_test.cache_extra_test_sources(s.package, extras)

    src_dests = [fs.join_path(test_root, src) for src in sources]
    exp_dests = [fs.join_path(test_root, e) for e in expect]
    poss_dests = set(src_dests) | set(exp_dests)

    msg = "Expected {0} to{1} exist"
    for pd in poss_dests:
        if pd in exp_dests:
            assert os.path.exists(pd), msg.format(pd, "")
            if os.path.splitext(pd)[1]:
                assert os.path.isfile(pd), emsg_file.format(pd)
            else:
                assert os.path.isdir(pd), emsg_dir.format(pd)
        else:
            assert not os.path.exists(pd), msg.format(pd, " not")

    # Perform a little cleanup
    shutil.rmtree(os.path.dirname(source_path))


def test_cache_extra_sources_fails(install_mockery):
    s = spack.concretize.concretize_one("pkg-a")

    with pytest.raises(InstallError) as exc_info:
        spack.install_test.cache_extra_test_sources(s.package, ["/a/b", "no-such-file"])

    errors = str(exc_info.value)
    assert "'/a/b') must be relative" in errors
    assert "'no-such-file') for the copy does not exist" in errors


def test_package_exes_and_libs():
    with pytest.raises(spack.error.SpackError, match="defines both"):

        class BadDetectablePackage(PackageBase):
            executables = ["findme"]
            libraries = ["libFindMe.a"]


def test_package_url_and_urls():
    UrlsPackage = type(
        "URLsPackage",
        (PackageBase,),
        {
            "__module__": "spack.pkg.builtin.urls_package",
            "url": "https://www.example.com/url-package-1.0.tgz",
            "urls": ["https://www.example.com/archive"],
        },
    )

    s = spack.spec.Spec("urls-package")
    with pytest.raises(ValueError, match="defines both"):
        UrlsPackage(s)


def test_package_license():
    LicensedPackage = type(
        "LicensedPackage", (PackageBase,), {"__module__": "spack.pkg.builtin.licensed_package"}
    )

    pkg = LicensedPackage(spack.spec.Spec("licensed-package"))
    assert pkg.global_license_file is None

    pkg.license_files = ["license.txt"]
    assert os.path.basename(pkg.global_license_file) == pkg.license_files[0]


class BaseTestPackage(PackageBase):
    extendees = None  # currently a required attribute for is_extension()


def test_package_version_fails():
    s = spack.spec.Spec("pkg-a")
    pkg = BaseTestPackage(s)
    with pytest.raises(ValueError, match="does not have a concrete version"):
        pkg.version()


def test_package_tester_fails():
    s = spack.spec.Spec("pkg-a")
    pkg = BaseTestPackage(s)
    with pytest.raises(ValueError, match="without concrete version"):
        pkg.tester()


def test_package_fetcher_fails():
    s = spack.spec.Spec("pkg-a")
    pkg = BaseTestPackage(s)
    with pytest.raises(ValueError, match="without concrete version"):
        pkg.fetcher


def test_package_test_no_compilers(mock_packages, monkeypatch, capfd):
    """Ensures that a test which needs the compiler, and build dependencies, to run, is skipped
    if no compiler is available.
    """
    s = spack.spec.Spec("pkg-a")
    pkg = BaseTestPackage(s)
    pkg.test_requires_compiler = True
    pkg.do_test()
    error = capfd.readouterr()[1]
    assert "Skipping tests for package" in error


def test_package_subscript(default_mock_concretization):
    """Tests that we can use the subscript notation on packages, and that it returns a package"""
    root = default_mock_concretization("mpileaks")
    root_pkg = root.package

    # Subscript of a virtual
    assert isinstance(root_pkg["mpi"], spack.package_base.PackageBase)

    # Subscript on concrete
    for d in root.traverse():
        assert isinstance(root_pkg[d.name], spack.package_base.PackageBase)


def test_deserialize_preserves_package_attribute(default_mock_concretization):
    x = default_mock_concretization("mpileaks").package
    assert x.spec._package is x

    y = spack.subprocess_context.deserialize(spack.subprocess_context.serialize(x))
    assert y.spec._package is y


@pytest.mark.parametrize("version", ("main", "tag"))
@pytest.mark.parametrize("pre_stage", (True, False))
@pytest.mark.require_provenance
@pytest.mark.disable_clean_stage_check
def test_binary_provenance_find_commit_ls_remote(
    git, mock_git_repository, mock_packages, config, monkeypatch, version, pre_stage
):
    repo_path = mock_git_repository.path
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", f"file://{repo_path}", raising=False
    )

    spec_str = f"git-test-commit@{version}"

    if pre_stage:
        spack.concretize.concretize_one(spec_str).package.do_stage(False)
    else:
        # explicitly disable ability to use stage or mirror, force url path
        monkeypatch.setattr(
            spack.package_base.PackageBase, "do_fetch", lambda *args, **kwargs: None
        )

    spec = spack.concretize.concretize_one(spec_str)

    if pre_stage:
        # confirmation that we actually had an expanded stage to query with ls-remote
        assert spec.package.stage.expanded

    vattrs = spec.package.versions[spec.version]
    git_ref = vattrs.get("tag") or vattrs.get("branch")
    actual_commit = git("-C", repo_path, "rev-parse", git_ref, output=str, error=str).strip()
    assert spec.variants["commit"].value == actual_commit


@pytest.mark.require_provenance
@pytest.mark.disable_clean_stage_check
def test_binary_provenance_cant_resolve_commit(mock_packages, monkeypatch, config, capsys):
    """Fail all attempts to resolve git commits"""
    monkeypatch.setattr(spack.package_base.PackageBase, "do_fetch", lambda *args, **kwargs: None)
    monkeypatch.setattr(spack.util.git, "get_commit_sha", lambda x, y: None, raising=False)
    spec = spack.concretize.concretize_one("git-ref-package@develop")
    captured = capsys.readouterr()
    assert "commit" not in spec.variants
    assert "Warning: Unable to resolve the git commit" in captured.err
