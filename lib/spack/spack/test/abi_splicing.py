# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
""" Test ABI-based splicing of dependencies """

import os

import py
import pytest

import archspec.cpu

from llnl.util.filesystem import copy_tree, mkdirp, touchp

import spack.config
import spack.package_base
import spack.paths
import spack.repo
import spack.solver.asp
import spack.spec
from spack.installer import PackageInstaller
from spack.spec import Spec


@pytest.fixture(scope="session")
def abi_splice_mock_repo_path():
    yield spack.repo.from_path(os.path.join(spack.paths.repos_path, "abi_splice.test"))


def _pkg_install_fn(pkg, spec, prefix):
    # sanity_check_prefix requires something in the install directory
    mkdirp(prefix.bin)
    if not os.path.exists(spec.package.install_log_path):
        touchp(spec.package.install_log_path)


@pytest.fixture
def abi_splice_mock_pkg_install(monkeypatch):
    monkeypatch.setattr(spack.package_base.PackageBase, "install", _pkg_install_fn, raising=False)


@pytest.fixture(scope="function")
def abi_splice_mock_packages(abi_splice_mock_repo_path, abi_splice_mock_pkg_install, request):
    if "abi_splice_config" in request.fixturenames:
        request.getfixturevalue("abi_splice_config")
    with spack.repo.use_repositories(abi_splice_mock_repo_path) as mock_repo:
        yield mock_repo


@pytest.fixture(scope="session")
def abi_splice_config_dir(tmpdir_factory, linux_os):
    """Copies mock configuration files in a temporary directory. Returns the
    directory path.
    """
    tmpdir = tmpdir_factory.mktemp("configurations")

    # <test_path>/data/config has mock config yaml files in it
    # copy these to the site config.
    test_config = py.path.local(spack.paths.test_path).join("data", "abi_splice_config")
    test_config.copy(tmpdir.join("site"))

    # Create temporary 'defaults', 'site' and 'user' folders
    tmpdir.ensure("user", dir=True)
    locks = True

    solver = os.environ.get("SPACK_TEST_SOLVER", "clingo")
    config_yaml = test_config.join("config.yaml")
    modules_root = tmpdir_factory.mktemp("share")
    tcl_root = modules_root.ensure("modules", dir=True)
    lmod_root = modules_root.ensure("lmod", dir=True)
    content = "".join(config_yaml.read()).format(solver, locks, str(tcl_root), str(lmod_root))
    t = tmpdir.join("site", "config.yaml")
    t.write(content)

    compilers_yaml = test_config.join("compilers.yaml")
    content = "".join(compilers_yaml.read()).format(
        linux_os=linux_os, target=str(archspec.cpu.host().family)
    )
    t = tmpdir.join("site", "compilers.yaml")
    t.write(content)
    yield tmpdir


def _create_mock_configuration_scopes(abi_splice_config_dir):
    """Create the configuration scopes used in `config` and `mutable_config`."""
    return [
        # spack.config.InternalConfigScope("_builtin", spack.config.CONFIG_DEFAULTS),
        spack.config.DirectoryConfigScope("site", str(abi_splice_config_dir.join("site"))),
        spack.config.DirectoryConfigScope("system", str(abi_splice_config_dir.join("system"))),
        spack.config.DirectoryConfigScope("user", str(abi_splice_config_dir.join("user"))),
        spack.config.InternalConfigScope("command_line"),
    ]


@pytest.fixture(scope="session")
def abi_splice_mock_config_scopes(abi_splice_config_dir):
    yield _create_mock_configuration_scopes(abi_splice_config_dir)


@pytest.fixture(scope="function")
def abi_splice_config(tmpdir_factory, abi_splice_config_dir):
    """Like config, but tests can modify the configuration."""
    mutable_dir = tmpdir_factory.mktemp("abi_splice_config").join("tmp")
    abi_splice_config_dir.copy(mutable_dir)

    scopes = _create_mock_configuration_scopes(mutable_dir)
    with spack.config.use_configuration(*scopes) as cfg:
        yield cfg


@pytest.fixture(scope="session")
def abi_splice_store_dir_and_cache(tmpdir_factory):
    """Returns the directory where to build the mock database and
    where to cache it.
    """
    store = tmpdir_factory.mktemp("abi_splice_mock_store")
    cache = tmpdir_factory.mktemp("abi_splice_mock_store_cache")
    return store, cache


@pytest.fixture(scope="session")
def abi_splice_mock_store(
    tmpdir_factory,
    abi_splice_mock_repo_path,
    abi_splice_mock_config_scopes,
    abi_splice_store_dir_and_cache,
):
    """Creates a read-only mock database with some packages installed note
    that the ref count for dyninst here will be 3, as it's recycled
    across each install.

    This does not actually activate the store for use by Spack -- see the
    ``database`` fixture for that.

    """
    store_path, store_cache = abi_splice_store_dir_and_cache

    # If the cache does not exist populate the store and create it
    if not os.path.exists(str(store_cache.join(".spack-db"))):
        with spack.config.use_configuration(*abi_splice_mock_config_scopes):
            with spack.store.use_store(str(store_path)) as _:
                with spack.repo.use_repositories(abi_splice_mock_repo_path):
                    None
        copy_tree(str(store_path), str(store_cache))

    store_path.join(".spack-db").chmod(mode=0o755, rec=1)
    yield store_path


@pytest.fixture(scope="function")
def abi_splice_database(
    abi_splice_mock_store, abi_splice_config, abi_splice_mock_packages, abi_splice_mock_pkg_install
):
    """This activates the mock store and config."""
    with spack.store.use_store(str(abi_splice_mock_store)) as store:
        yield store.db
        # Force reading the database again between tests
        store.db.last_seen_verifier = ""


def _mock_has_runtime_dependencies(_x):
    return True


def test_simple_reuse(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    foo = Spec("foo@1.0.0+compat").concretized()
    PackageInstaller([foo.package], fake=True, explicit=True).install()
    new_foo = Spec("foo").concretized()
    assert foo == new_foo
    foo.package.do_uninstall()


def test_simple_dep_reuse(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    foo = Spec("foo@1.0.0+compat").concretized()
    PackageInstaller([foo.package], fake=True, explicit=True).install()
    bar = Spec("bar@1").concretized()
    assert foo in bar.dependencies()
    foo.package.do_uninstall()


def test_splice_installed_hash(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    old_baz = Spec("baz@1 ^bar@1.0.0+compat ^foo@1.0.0+compat").concretized()
    new_bar = Spec("bar@1.0.2+compat").concretized()
    PackageInstaller([old_baz.package], fake=True, explicit=True).install()
    PackageInstaller([new_bar.package], fake=True, explicit=True).install()
    baz_config = {"baz": {"buildable": False}}
    spack.config.set("packages", baz_config)
    goal_spec = Spec("baz@1 ^bar@1.0.2+compat ^foo@1.0.0+compat")
    with pytest.raises(Exception):
        goal_spec.concretized()
    spack.config.set("concretizer:splice", True)
    goal_spec.concretized()
    old_baz.package.do_uninstall()
    new_bar.package.do_uninstall()
    assert True


def test_splice_build_dep(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    old_baz = Spec("baz@1 ^bar@1.0.0+compat ^foo@1.0.0+compat").concretized()
    PackageInstaller([old_baz.package], fake=True, explicit=True).install()
    baz_config = {"baz": {"buildable": False}}
    spack.config.set("packages", baz_config)
    goal_spec = Spec("baz@1 ^bar@1.0.2+compat ^foo@1.0.0+compat")
    with pytest.raises(Exception):
        goal_spec.concretized()
    spack.config.set("concretizer:splice", True)
    goal_spec.concretized()
    old_baz.package.do_uninstall()
    assert True


def test_mpi_splices(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    mpileaks_openmpi = Spec("mpileaks ^openmpi").concretized()
    mpileaks_mpich = Spec("mpileaks ^mpich").concretized()
    PackageInstaller([mpileaks_openmpi.package], fake=True, explicit=True).install()
    PackageInstaller([mpileaks_mpich.package], fake=True, explicit=True).install()
    mpileaks_config = {"mpileaks": {"buildable": False}}
    spack.config.set("packages", mpileaks_config)
    openmpi_goal_spec = Spec("mpileaks ^xmpi abi=openmpi")
    mpich_goal_spec = Spec("mpileaks ^xmpi abi=mpich")
    with pytest.raises(Exception):
        openmpi_goal_spec.concretized()
    with pytest.raises(Exception):
        mpich_goal_spec.concretized()
    spack.config.set("concretizer:splice", True)
    openmpi_goal_spec.concretized()
    mpich_goal_spec.concretized()
    mpileaks_openmpi.package.do_uninstall()
    mpileaks_mpich.package.do_uninstall()
    assert True


def test_double_splice(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [
        Spec("baz@1 ^bar@1.0.0+compat ^foo@1.0.0+compat"),
        Spec("bar@1.0.2+compat ^foo@1.0.1+compat"),
        Spec("foo@1.0.2+compat"),
    ]
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    freeze_builds_config = {
        "baz": {"buildable": False},
        "bar": {"buildable": False},
        "foo": {"buildable": False},
    }
    spack.config.set("packages", freeze_builds_config)
    goal_spec = Spec("baz@1 ^bar@1.0.2+compat ^foo@1.0.2+compat")
    with pytest.raises(Exception):
        goal_spec.concretized()
    spack.config.set("concretizer:splice", True)
    goal_spec.concretized()
    for s in cache:
        s.package.do_uninstall()


def test_manyvariant_star_matching_variant_splice(
    abi_splice_database, abi_splice_mock_packages, monkeypatch
):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [
        # can_splice("manyvariants@1.0.0", when="@1.0.1", match_variants="*")
        Spec("depends-on-manyvariants ^manyvariants@1.0.0+a+b c=v1 d=v2"),
        Spec("depends-on-manyvariants ^manyvariants@1.0.0~a~b c=v3 d=v3"),
    ]
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    goal_specs = [
        Spec("depends-on-manyvariants ^manyvariants@1.0.1+a+b c=v1 d=v2"),
        Spec("depends-on-manyvariants ^manyvariants@1.0.1~a~b c=v3 d=v3"),
    ]
    freeze_build_config = {"depends-on-manyvariants": {"buildable": False}}
    spack.config.set("packages", freeze_build_config)
    for goal in goal_specs:
        with pytest.raises(Exception):
            goal.concretized()
    spack.config.set("concretizer:splice", True)
    for goal in goal_specs:
        goal.concretized()

    for s in cache:
        s.package.do_uninstall()
    assert True


def test_manyvariant_limited_matching(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [
        # can_splice("manyvariants@2.0.0+a~b", when="@2.0.1~a+b", match_variants=["c", "d"])
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.0+a~b c=v3 d=v2"),
        # can_splice("manyvariants@2.0.0 c=v1 d=v1", when="@2.0.1+a+b")
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.0~a~b c=v1 d=v1"),
    ]
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    goal_specs = [
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.1~a+b c=v3 d=v2"),
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.1+a+b c=v3 d=v3"),
    ]
    freeze_build_config = {"depends-on-manyvariants": {"buildable": False}}
    spack.config.set("packages", freeze_build_config)
    for s in goal_specs:
        with pytest.raises(Exception):
            s.concretized()
    spack.config.set("concretizer:splice", True)
    for s in goal_specs:
        s.concretized()
    for s in cache:
        s.package.do_uninstall()

    assert True


def test_external_splice_same_name(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [Spec("bar@1.0.0 ^foo@1.0.0+compat"), Spec("baz@1.0 ^bar@1.0.1 ^foo@1.0.1+compat")]
    packages_yaml = {
        "foo": {"externals": [{"spec": "foo@1.0.2+compat", "prefix": "/usr"}], "buildable": True},
        "bar": {"buildable": True},
    }
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    spack.config.set("packages", packages_yaml)
    goal_specs = [Spec("bar@1.0.0 ^foo@1.0.2"), Spec("baz@1.0 ^bar@1.0.1 ^foo@1.0.2")]
    spack.config.set("concretizer:splice", True)
    for s in goal_specs:
        s.concretized()


def test_external_splice_mpi(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [Spec("bar@1.0.0 ^foo@1.0.0+compat"), Spec("baz@1.0 ^bar@1.0.1 ^foo@1.0.1+compat")]
    packages_yaml = {
        "foo": {"externals": [{"spec": "foo@1.0.2+compat", "prefix": "/usr"}], "buildable": True},
        "bar": {"buildable": True},
    }
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    spack.config.set("packages", packages_yaml)
    goal_specs = [Spec("bar@1.0.0 ^foo@1.0.2"), Spec("baz@1.0 ^bar@1.0.1 ^foo@1.0.2")]
    spack.config.set("concretizer:splice", True)
    for s in goal_specs:
        s.concretized()
