import os

import py
import pytest

import archspec.cpu

from llnl.util.filesystem import copy_tree, mkdirp, touchp

import spack.abi
import spack.config
import spack.package_base
import spack.paths
import spack.repo
import spack.solver.asp
import spack.spec
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


def test_simple_reuse(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(spack.solver.asp, "_has_runtime_dependencies", lambda x: True)
    foo = Spec("foo@1.0.0+compat").concretized()
    foo.package.do_install(fake=True, explicit=True)
    new_foo = Spec("foo").concretized()
    assert foo == new_foo
    foo.package.do_uninstall()


def test_simple_dep_reuse(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(spack.solver.asp, "_has_runtime_dependencies", lambda x: True)
    foo = Spec("foo@1.0.0+compat").concretized()
    foo.package.do_install(fake=True, explicit=True)
    bar = Spec("bar@1").concretized()
    assert foo in bar.dependencies()
    foo.package.do_uninstall()


def test_splice_installed_hash(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(spack.solver.asp, "_has_runtime_dependencies", lambda x: True)
    old_baz = Spec("baz@1 ^bar@1.0.0+compat ^foo@1.0.0+compat").concretized()
    new_bar = Spec("bar@1.0.2+compat").concretized()
    old_baz.package.do_install(fake=True, explicit=True)
    new_bar.package.do_install(fake=True, explicit=True)
    baz_config = {"baz": {"buildable": False}}
    spack.config.set("packages", baz_config)
    Spec("baz@1 ^bar@1.0.2+compat ^foo@1.0.0+compat").concretized()
    old_baz.package.do_uninstall()
    new_bar.package.do_uninstall()
    assert True


def test_splice_build_dep(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(spack.solver.asp, "_has_runtime_dependencies", lambda x: True)
    old_baz = Spec("baz@1 ^bar@1.0.0+compat ^foo@1.0.0+compat").concretized()
    old_baz.package.do_install(fake=True, explicit=True)
    baz_config = {"baz": {"buildable": False}}
    spack.config.set("packages", baz_config)
    Spec("baz@1 ^bar@1.0.2+compat ^foo@1.0.0+compat").concretized()
    old_baz.package.do_uninstall()
    assert True


def test_mpi_splices(abi_splice_database, abi_splice_mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(spack.solver.asp, "_has_runtime_dependencies", lambda x: True)
    mpileaks_openmpi = Spec("mpileaks ^openmpi").concretized()
    mpileaks_mpich = Spec("mpileaks ^mpich").concretized()
    mpileaks_openmpi.package.do_install(fake=True, explicit=True)
    mpileaks_mpich.package.do_install(fake=True, explicit=True)
    mpileaks_config = {"mpileaks": {"buildable": False}}
    spack.config.set("packages", mpileaks_config)
    Spec("mpileaks ^xmpi abi=openmpi").concretized()
    Spec("mpileaks ^xmpi abi=mpich").concretized()
    mpileaks_openmpi.package.do_uninstall()
    mpileaks_mpich.package.do_uninstall()
    assert True
