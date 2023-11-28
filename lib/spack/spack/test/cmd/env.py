# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import filecmp
import glob
import io
import os
import pathlib
import shutil
from argparse import Namespace

import pytest

import llnl.util.filesystem as fs
import llnl.util.link_tree
import llnl.util.tty as tty

import spack.cmd.env
import spack.config
import spack.environment as ev
import spack.environment.depfile as depfile
import spack.environment.environment
import spack.environment.shell
import spack.error
import spack.modules
import spack.package_base
import spack.paths
import spack.repo
import spack.util.spack_json as sjson
from spack.cmd.env import _env_create
from spack.main import SpackCommand, SpackCommandError
from spack.spec import Spec
from spack.stage import stage_prefix
from spack.util.executable import Executable
from spack.util.path import substitute_path_variables
from spack.version import Version

# TODO-27021
# everything here uses the mock_env_path
pytestmark = [
    pytest.mark.usefixtures("mutable_mock_env_path", "config", "mutable_mock_repo"),
    pytest.mark.maybeslow,
    pytest.mark.not_on_windows("Envs unsupported on Window"),
]

env = SpackCommand("env")
install = SpackCommand("install")
add = SpackCommand("add")
change = SpackCommand("change")
remove = SpackCommand("remove")
concretize = SpackCommand("concretize")
stage = SpackCommand("stage")
uninstall = SpackCommand("uninstall")
find = SpackCommand("find")
module = SpackCommand("module")

sep = os.sep


@pytest.fixture()
def environment_from_manifest(tmp_path):
    """Returns a new environment named 'test' from the content of a manifest file."""

    def _create(content):
        spack_yaml = tmp_path / ev.manifest_name
        spack_yaml.write_text(content)
        return _env_create("test", init_file=str(spack_yaml))

    return _create


def check_mpileaks_and_deps_in_view(viewdir):
    """Check that the expected install directories exist."""
    assert os.path.exists(str(viewdir.join(".spack", "mpileaks")))
    assert os.path.exists(str(viewdir.join(".spack", "libdwarf")))


def check_viewdir_removal(viewdir):
    """Check that the uninstall/removal worked."""
    assert not os.path.exists(str(viewdir.join(".spack"))) or os.listdir(
        str(viewdir.join(".spack"))
    ) == ["projections.yaml"]


def test_add():
    e = ev.create("test")
    e.add("mpileaks")
    assert Spec("mpileaks") in e.user_specs


def test_change_match_spec():
    env("create", "test")

    e = ev.read("test")
    with e:
        add("mpileaks@2.1")
        add("mpileaks@2.2")

        change("--match-spec", "mpileaks@2.2", "mpileaks@2.3")

    assert not any(x.intersects("mpileaks@2.2") for x in e.user_specs)
    assert any(x.intersects("mpileaks@2.3") for x in e.user_specs)


def test_change_multiple_matches():
    env("create", "test")

    e = ev.read("test")
    with e:
        add("mpileaks@2.1")
        add("mpileaks@2.2")
        add("libelf@0.8.12%clang")

        change("--match-spec", "mpileaks", "-a", "mpileaks%gcc")

    assert all(x.intersects("%gcc") for x in e.user_specs if x.name == "mpileaks")
    assert any(x.intersects("%clang") for x in e.user_specs if x.name == "libelf")


def test_env_add_virtual():
    env("create", "test")

    e = ev.read("test")
    e.add("mpi")
    e.concretize()

    hashes = e.concretized_order
    assert len(hashes) == 1
    spec = e.specs_by_hash[hashes[0]]
    assert spec.intersects("mpi")


def test_env_add_nonexistant_fails():
    env("create", "test")

    e = ev.read("test")
    with pytest.raises(ev.SpackEnvironmentError, match=r"no such package"):
        e.add("thispackagedoesnotexist")


def test_env_list(mutable_mock_env_path):
    env("create", "foo")
    env("create", "bar")
    env("create", "baz")

    out = env("list")

    assert "foo" in out
    assert "bar" in out
    assert "baz" in out

    # make sure `spack env list` skips invalid things in var/spack/env
    (mutable_mock_env_path / ".DS_Store").touch()
    out = env("list")

    assert "foo" in out
    assert "bar" in out
    assert "baz" in out
    assert ".DS_Store" not in out


def test_env_remove(capfd):
    env("create", "foo")
    env("create", "bar")

    out = env("list")
    assert "foo" in out
    assert "bar" in out

    foo = ev.read("foo")
    with foo:
        with pytest.raises(SpackCommandError):
            with capfd.disabled():
                env("remove", "-y", "foo")
        assert "foo" in env("list")

    env("remove", "-y", "foo")
    out = env("list")
    assert "foo" not in out
    assert "bar" in out

    env("remove", "-y", "bar")
    out = env("list")
    assert "foo" not in out
    assert "bar" not in out


def test_concretize():
    e = ev.create("test")
    e.add("mpileaks")
    e.concretize()
    env_specs = e._get_environment_specs()
    assert any(x.name == "mpileaks" for x in env_specs)


def test_env_specs_partition(install_mockery, mock_fetch):
    e = ev.create("test")
    e.add("cmake-client")
    e.concretize()

    # Single not installed root spec.
    roots_already_installed, roots_to_install = e._partition_roots_by_install_status()
    assert len(roots_already_installed) == 0
    assert len(roots_to_install) == 1
    assert roots_to_install[0].name == "cmake-client"

    # Single installed root.
    e.install_all()
    roots_already_installed, roots_to_install = e._partition_roots_by_install_status()
    assert len(roots_already_installed) == 1
    assert roots_already_installed[0].name == "cmake-client"
    assert len(roots_to_install) == 0

    # One installed root, one not installed root.
    e.add("mpileaks")
    e.concretize()
    roots_already_installed, roots_to_install = e._partition_roots_by_install_status()
    assert len(roots_already_installed) == 1
    assert len(roots_to_install) == 1
    assert roots_already_installed[0].name == "cmake-client"
    assert roots_to_install[0].name == "mpileaks"


def test_env_install_all(install_mockery, mock_fetch):
    e = ev.create("test")
    e.add("cmake-client")
    e.concretize()
    e.install_all()
    env_specs = e._get_environment_specs()
    spec = next(x for x in env_specs if x.name == "cmake-client")
    assert spec.installed


def test_env_install_single_spec(install_mockery, mock_fetch):
    env("create", "test")
    install = SpackCommand("install")

    e = ev.read("test")
    with e:
        install("--add", "cmake-client")

    e = ev.read("test")
    assert e.user_specs[0].name == "cmake-client"
    assert e.concretized_user_specs[0].name == "cmake-client"
    assert e.specs_by_hash[e.concretized_order[0]].name == "cmake-client"


def test_env_roots_marked_explicit(install_mockery, mock_fetch):
    install = SpackCommand("install")
    install("dependent-install")

    # Check one explicit, one implicit install
    dependent = spack.store.STORE.db.query(explicit=True)
    dependency = spack.store.STORE.db.query(explicit=False)
    assert len(dependent) == 1
    assert len(dependency) == 1

    env("create", "test")
    with ev.read("test") as e:
        # make implicit install a root of the env
        e.add(dependency[0].name)
        e.concretize()
        e.install_all()

    explicit = spack.store.STORE.db.query(explicit=True)
    assert len(explicit) == 2


def test_env_modifications_error_on_activate(install_mockery, mock_fetch, monkeypatch, capfd):
    env("create", "test")
    install = SpackCommand("install")

    e = ev.read("test")
    with e:
        install("--add", "cmake-client")

    def setup_error(pkg, env):
        raise RuntimeError("cmake-client had issues!")

    pkg = spack.repo.PATH.get_pkg_class("cmake-client")
    monkeypatch.setattr(pkg, "setup_run_environment", setup_error)

    spack.environment.shell.activate(e)

    _, err = capfd.readouterr()
    assert "cmake-client had issues!" in err
    assert "Warning: could not load runtime environment" in err


def test_activate_adds_transitive_run_deps_to_path(install_mockery, mock_fetch, monkeypatch):
    env("create", "test")
    install = SpackCommand("install")

    e = ev.read("test")
    with e:
        install("--add", "depends-on-run-env")

    env_variables = {}
    spack.environment.shell.activate(e).apply_modifications(env_variables)
    assert env_variables["DEPENDENCY_ENV_VAR"] == "1"


def test_env_install_same_spec_twice(install_mockery, mock_fetch):
    env("create", "test")

    e = ev.read("test")
    with e:
        # The first installation outputs the package prefix, updates the view
        out = install("--add", "cmake-client")
        assert "Updating view at" in out

        # The second installation reports all packages already installed
        out = install("cmake-client")
        assert "already installed" in out


def test_env_definition_symlink(install_mockery, mock_fetch, tmpdir):
    filepath = str(tmpdir.join("spack.yaml"))
    filepath_mid = str(tmpdir.join("spack_mid.yaml"))

    env("create", "test")
    e = ev.read("test")
    e.add("mpileaks")

    os.rename(e.manifest_path, filepath)
    os.symlink(filepath, filepath_mid)
    os.symlink(filepath_mid, e.manifest_path)

    e.concretize()
    e.write()

    assert os.path.islink(e.manifest_path)
    assert os.path.islink(filepath_mid)


def test_env_install_two_specs_same_dep(install_mockery, mock_fetch, tmpdir, capsys):
    """Test installation of two packages that share a dependency with no
    connection and the second specifying the dependency as a 'build'
    dependency.
    """
    path = tmpdir.join("spack.yaml")

    with tmpdir.as_cwd():
        with open(str(path), "w") as f:
            f.write(
                """\
spack:
  specs:
  - a
  - depb
"""
            )

        env("create", "test", "spack.yaml")

    with ev.read("test"):
        with capsys.disabled():
            out = install()

    # Ensure both packages reach install phase processing and are installed
    out = str(out)
    assert "depb: Executing phase:" in out
    assert "a: Executing phase:" in out

    depb = spack.store.STORE.db.query_one("depb", installed=True)
    assert depb, "Expected depb to be installed"

    a = spack.store.STORE.db.query_one("a", installed=True)
    assert a, "Expected a to be installed"


def test_remove_after_concretize():
    e = ev.create("test")

    e.add("mpileaks")
    e.concretize()

    e.add("python")
    e.concretize()

    e.remove("mpileaks")
    assert Spec("mpileaks") not in e.user_specs
    env_specs = e._get_environment_specs()
    assert any(s.name == "mpileaks" for s in env_specs)

    e.add("mpileaks")
    assert any(s.name == "mpileaks" for s in e.user_specs)

    e.remove("mpileaks", force=True)
    assert Spec("mpileaks") not in e.user_specs
    env_specs = e._get_environment_specs()
    assert not any(s.name == "mpileaks" for s in env_specs)


def test_remove_before_concretize():
    e = ev.create("test")
    e.unify = True

    e.add("mpileaks")
    e.concretize()

    e.remove("mpileaks")
    e.concretize()

    assert not list(e.concretized_specs())


def test_remove_command():
    env("create", "test")
    assert "test" in env("list")

    with ev.read("test"):
        add("mpileaks")
        assert "mpileaks" in find()
        assert "mpileaks@" not in find()
        assert "mpileaks@" not in find("--show-concretized")

    with ev.read("test"):
        remove("mpileaks")
        assert "mpileaks" not in find()
        assert "mpileaks@" not in find()
        assert "mpileaks@" not in find("--show-concretized")

    with ev.read("test"):
        add("mpileaks")
        assert "mpileaks" in find()
        assert "mpileaks@" not in find()
        assert "mpileaks@" not in find("--show-concretized")

    with ev.read("test"):
        concretize()
        assert "mpileaks" in find()
        assert "mpileaks@" not in find()
        assert "mpileaks@" in find("--show-concretized")

    with ev.read("test"):
        remove("mpileaks")
        assert "mpileaks" not in find()
        # removed but still in last concretized specs
        assert "mpileaks@" in find("--show-concretized")

    with ev.read("test"):
        concretize()
        assert "mpileaks" not in find()
        assert "mpileaks@" not in find()
        # now the lockfile is regenerated and it's gone.
        assert "mpileaks@" not in find("--show-concretized")


def test_environment_status(capsys, tmpdir):
    with tmpdir.as_cwd():
        with capsys.disabled():
            assert "No active environment" in env("status")

        with ev.create("test"):
            with capsys.disabled():
                assert "In environment test" in env("status")

        with ev.create_in_dir("local_dir"):
            with capsys.disabled():
                assert os.path.join(os.getcwd(), "local_dir") in env("status")

            e = ev.create_in_dir("myproject")
            e.write()
            with tmpdir.join("myproject").as_cwd():
                with e:
                    with capsys.disabled():
                        assert "in current directory" in env("status")


def test_env_status_broken_view(
    mutable_mock_env_path,
    mock_archive,
    mock_fetch,
    mock_custom_repository,
    install_mockery,
    tmp_path,
):
    with ev.create_in_dir(tmp_path):
        install("--add", "trivial-install-test-package")

    # switch to a new repo that doesn't include the installed package
    # test that Spack detects the missing package and warns the user
    with spack.repo.use_repositories(mock_custom_repository):
        with ev.Environment(tmp_path):
            output = env("status")
            assert "includes out of date packages or repos" in output

    # Test that the warning goes away when it's fixed
    with ev.Environment(tmp_path):
        output = env("status")
        assert "includes out of date packages or repos" not in output


def test_env_activate_broken_view(
    mutable_mock_env_path, mock_archive, mock_fetch, mock_custom_repository, install_mockery
):
    with ev.create("test"):
        install("--add", "trivial-install-test-package")

    # switch to a new repo that doesn't include the installed package
    # test that Spack detects the missing package and fails gracefully
    with spack.repo.use_repositories(mock_custom_repository):
        wrong_repo = env("activate", "--sh", "test")
        assert "Warning: could not load runtime environment" in wrong_repo
        assert "Unknown namespace: builtin.mock" in wrong_repo

    # test replacing repo fixes it
    normal_repo = env("activate", "--sh", "test")
    assert "Warning: could not load runtime environment" not in normal_repo
    assert "Unknown namespace: builtin.mock" not in normal_repo


def test_to_lockfile_dict():
    e = ev.create("test")
    e.add("mpileaks")
    e.concretize()
    context_dict = e._to_lockfile_dict()

    e_copy = ev.create("test_copy")

    e_copy._read_lockfile_dict(context_dict)
    assert e.specs_by_hash == e_copy.specs_by_hash


def test_env_repo():
    e = ev.create("test")
    e.add("mpileaks")
    e.write()

    with ev.read("test"):
        concretize()

    pkg_cls = e.repo.get_pkg_class("mpileaks")
    assert pkg_cls.name == "mpileaks"
    assert pkg_cls.namespace == "builtin.mock"


def test_user_removed_spec(environment_from_manifest):
    """Ensure a user can remove from any position in the spack.yaml file."""
    before = environment_from_manifest(
        """\
spack:
  specs:
  - mpileaks
  - hypre
  - libelf
"""
    )
    before.concretize()
    before.write()

    # user modifies yaml externally to spack and removes hypre
    with open(before.manifest_path, "w") as f:
        f.write(
            """\
spack:
  specs:
  - mpileaks
  - libelf
"""
        )

    after = ev.read("test")
    after.concretize()
    after.write()

    read = ev.read("test")
    env_specs = read._get_environment_specs()

    assert not any(x.name == "hypre" for x in env_specs)


def test_init_from_lockfile(environment_from_manifest):
    """Test that an environment can be instantiated from a lockfile."""
    e1 = environment_from_manifest(
        """
spack:
  specs:
  - mpileaks
  - hypre
  - libelf
"""
    )
    e1.concretize()
    e1.write()

    e2 = _env_create("test2", init_file=e1.lock_path)

    for s1, s2 in zip(e1.user_specs, e2.user_specs):
        assert s1 == s2

    for h1, h2 in zip(e1.concretized_order, e2.concretized_order):
        assert h1 == h2
        assert e1.specs_by_hash[h1] == e2.specs_by_hash[h2]

    for s1, s2 in zip(e1.concretized_user_specs, e2.concretized_user_specs):
        assert s1 == s2


def test_init_from_yaml(environment_from_manifest):
    """Test that an environment can be instantiated from a lockfile."""
    e1 = environment_from_manifest(
        """
spack:
  specs:
  - mpileaks
  - hypre
  - libelf
"""
    )
    e1.concretize()
    e1.write()

    e2 = _env_create("test2", init_file=e1.manifest_path)

    for s1, s2 in zip(e1.user_specs, e2.user_specs):
        assert s1 == s2

    assert not e2.concretized_order
    assert not e2.concretized_user_specs
    assert not e2.specs_by_hash


@pytest.mark.usefixtures("config")
def test_env_view_external_prefix(tmp_path, mutable_database, mock_packages):
    fake_prefix = tmp_path / "a-prefix"
    fake_bin = fake_prefix / "bin"
    fake_bin.mkdir(parents=True, exist_ok=False)

    manifest_dir = tmp_path / "environment"
    manifest_dir.mkdir(parents=True, exist_ok=False)
    manifest_file = manifest_dir / ev.manifest_name
    manifest_file.write_text(
        """\
spack:
  specs:
  - a
  view: true
"""
    )

    external_config = io.StringIO(
        """\
packages:
  a:
    externals:
    - spec: a@2.0
      prefix: {a_prefix}
    buildable: false
""".format(
            a_prefix=str(fake_prefix)
        )
    )
    external_config_dict = spack.util.spack_yaml.load_config(external_config)

    test_scope = spack.config.InternalConfigScope("env-external-test", data=external_config_dict)
    with spack.config.override(test_scope):
        e = ev.create("test", manifest_file)
        e.concretize()
        # Note: normally installing specs in a test environment requires doing
        # a fake install, but not for external specs since no actions are
        # taken to install them. The installation commands also include
        # post-installation functions like DB-registration, so are important
        # to do (otherwise the package is not considered installed).
        e.install_all()
        e.write()

        env_mod = spack.util.environment.EnvironmentModifications()
        e.add_view_to_env(env_mod, "default")
        env_variables = {}
        env_mod.apply_modifications(env_variables)
        assert str(fake_bin) in env_variables["PATH"]


def test_init_with_file_and_remove(tmpdir):
    """Ensure a user can remove from any position in the spack.yaml file."""
    path = tmpdir.join("spack.yaml")

    with tmpdir.as_cwd():
        with open(str(path), "w") as f:
            f.write(
                """\
spack:
  specs:
  - mpileaks
"""
            )

        env("create", "test", "spack.yaml")

    out = env("list")
    assert "test" in out

    with ev.read("test"):
        assert "mpileaks" in find()

    env("remove", "-y", "test")

    out = env("list")
    assert "test" not in out


def test_env_with_config(environment_from_manifest):
    e = environment_from_manifest(
        """
spack:
  specs:
  - mpileaks
  packages:
    mpileaks:
      version: ["2.2"]
"""
    )
    with e:
        e.concretize()

    assert any(x.intersects("mpileaks@2.2") for x in e._get_environment_specs())


def test_with_config_bad_include(environment_from_manifest):
    """Confirm missing include paths raise expected exception and error."""
    with pytest.raises(spack.config.ConfigFileError, match="2 missing include path"):
        e = environment_from_manifest(
            """
spack:
  include:
  - /no/such/directory
  - no/such/file.yaml
"""
        )
        with e:
            e.concretize()

    assert ev.active_environment() is None


def test_env_with_include_config_files_same_basename(tmp_path, environment_from_manifest):
    file1 = fs.join_path(tmp_path, "path", "to", "included-config.yaml")
    fs.mkdirp(os.path.dirname(file1))
    with open(file1, "w") as f:
        f.write(
            """\
        packages:
          libelf:
              version: ["0.8.10"]
        """
        )

    file2 = fs.join_path(tmp_path, "second", "path", "included-config.yaml")
    fs.mkdirp(os.path.dirname(file2))
    with open(file2, "w") as f:
        f.write(
            """\
        packages:
          mpileaks:
              version: ["2.2"]
        """
        )

    e = environment_from_manifest(
        f"""
spack:
  include:
  - {file1}
  - {file2}
  specs:
  - libelf
  - mpileaks
"""
    )

    with e:
        e.concretize()

    environment_specs = e._get_environment_specs(False)

    assert environment_specs[0].satisfies("libelf@0.8.10")
    assert environment_specs[1].satisfies("mpileaks@2.2")


@pytest.fixture(scope="function")
def packages_file(tmpdir):
    """Return the path to the packages configuration file."""
    raw_yaml = """
packages:
  mpileaks:
    version: ["2.2"]
"""
    filename = tmpdir.ensure("testconfig", "packages.yaml")
    filename.write(raw_yaml)
    yield filename


def mpileaks_env_config(include_path):
    """Return the contents of an environment that includes the provided
    path and lists mpileaks as the sole spec."""
    return """\
spack:
  include:
  - {0}
  specs:
  - mpileaks
""".format(
        include_path
    )


def test_env_with_included_config_file(mutable_mock_env_path, packages_file):
    """Test inclusion of a relative packages configuration file added to an
    existing environment.
    """
    env_root = mutable_mock_env_path
    fs.mkdirp(env_root)
    include_filename = "included-config.yaml"
    included_path = env_root / include_filename
    shutil.move(packages_file.strpath, included_path)

    spack_yaml = env_root / ev.manifest_name
    spack_yaml.write_text(
        f"""\
spack:
  include:
  - {os.path.join(".", include_filename)}
  specs:
  - mpileaks
"""
    )

    e = ev.Environment(env_root)
    with e:
        e.concretize()

    assert any(x.satisfies("mpileaks@2.2") for x in e._get_environment_specs())


def test_env_with_included_config_file_url(tmpdir, mutable_empty_config, packages_file):
    """Test configuration inclusion of a file whose path is a URL before
    the environment is concretized."""

    spack_yaml = tmpdir.join("spack.yaml")
    with spack_yaml.open("w") as f:
        f.write("spack:\n  include:\n    - file://{0}\n".format(packages_file))

    env = ev.Environment(tmpdir.strpath)
    ev.activate(env)
    scopes = env.included_config_scopes()
    assert len(scopes) == 1

    cfg = spack.config.get("packages")
    assert cfg["mpileaks"]["version"] == ["2.2"]


def test_env_with_included_config_missing_file(tmpdir, mutable_empty_config):
    """Test inclusion of a missing configuration file raises FetchError
    noting missing file."""

    spack_yaml = tmpdir.join("spack.yaml")
    missing_file = tmpdir.join("packages.yaml")
    with spack_yaml.open("w") as f:
        f.write("spack:\n  include:\n    - {0}\n".format(missing_file.strpath))

    with pytest.raises(spack.config.ConfigError, match="missing include path"):
        ev.Environment(tmpdir.strpath)


def test_env_with_included_config_scope(mutable_mock_env_path, packages_file):
    """Test inclusion of a package file from the environment's configuration
    stage directory. This test is intended to represent a case where a remote
    file has already been staged."""
    env_root = mutable_mock_env_path
    config_scope_path = env_root / "config"

    # Copy the packages.yaml file to the environment configuration
    # directory, so it is picked up during concretization. (Using
    # copy instead of rename in case the fixture scope changes.)
    fs.mkdirp(config_scope_path)
    include_filename = os.path.basename(packages_file.strpath)
    included_path = config_scope_path / include_filename
    fs.copy(packages_file.strpath, included_path)

    # Configure the environment to include file(s) from the environment's
    # remote configuration stage directory.
    spack_yaml = env_root / ev.manifest_name
    spack_yaml.write_text(mpileaks_env_config(config_scope_path))

    # Ensure the concretized environment reflects contents of the
    # packages.yaml file.
    e = ev.Environment(env_root)
    with e:
        e.concretize()

    assert any(x.satisfies("mpileaks@2.2") for x in e._get_environment_specs())


def test_env_with_included_config_var_path(tmpdir, packages_file):
    """Test inclusion of a package configuration file with path variables
    "staged" in the environment's configuration stage directory."""
    included_file = packages_file.strpath
    env_path = pathlib.PosixPath(tmpdir)
    config_var_path = os.path.join("$tempdir", "included-packages.yaml")

    spack_yaml = env_path / ev.manifest_name
    spack_yaml.write_text(mpileaks_env_config(config_var_path))

    config_real_path = substitute_path_variables(config_var_path)
    shutil.move(included_file, config_real_path)
    assert os.path.exists(config_real_path)

    e = ev.Environment(env_path)
    with e:
        e.concretize()

    assert any(x.satisfies("mpileaks@2.2") for x in e._get_environment_specs())


def test_env_with_included_config_precedence(tmp_path):
    """Test included scope and manifest precedence when including a package
    configuration file."""

    included_file = "included-packages.yaml"
    included_path = tmp_path / included_file
    with open(included_path, "w") as f:
        f.write(
            """\
packages:
  mpileaks:
    version: ["2.2"]
  libelf:
    version: ["0.8.10"]
"""
        )

    spack_yaml = tmp_path / ev.manifest_name
    spack_yaml.write_text(
        f"""\
spack:
  packages:
    libelf:
      version: ["0.8.12"]
  include:
  - {os.path.join(".", included_file)}
  specs:
  - mpileaks
"""
    )

    e = ev.Environment(tmp_path)
    with e:
        e.concretize()
    specs = e._get_environment_specs()

    # ensure included scope took effect
    assert any(x.satisfies("mpileaks@2.2") for x in specs)

    # ensure env file takes precedence
    assert any(x.satisfies("libelf@0.8.12") for x in specs)


def test_env_with_included_configs_precedence(tmp_path):
    """Test precendence of multiple included configuration files."""
    file1 = "high-config.yaml"
    file2 = "low-config.yaml"

    spack_yaml = tmp_path / ev.manifest_name
    spack_yaml.write_text(
        f"""\
spack:
  include:
  - {os.path.join(".", file1)} # this one should take precedence
  - {os.path.join(".", file2)}
  specs:
  - mpileaks
"""
    )

    with open(tmp_path / file1, "w") as f:
        f.write(
            """\
packages:
  libelf:
    version: ["0.8.10"]  # this should override libelf version below
"""
        )

    with open(tmp_path / file2, "w") as f:
        f.write(
            """\
packages:
  mpileaks:
    version: ["2.2"]
  libelf:
    version: ["0.8.12"]
"""
        )

    e = ev.Environment(tmp_path)
    with e:
        e.concretize()
    specs = e._get_environment_specs()

    # ensure included package spec took precedence over manifest spec
    assert any(x.satisfies("mpileaks@2.2") for x in specs)

    # ensure first included package spec took precedence over one from second
    assert any(x.satisfies("libelf@0.8.10") for x in specs)


@pytest.mark.regression("39248")
def test_bad_env_yaml_format_remove(mutable_mock_env_path):
    badenv = "badenv"
    env("create", badenv)
    filename = mutable_mock_env_path / "spack.yaml"
    with open(filename, "w") as f:
        f.write(
            """\
    - mpileaks
"""
        )

    assert badenv in env("list")
    env("remove", "-y", badenv)
    assert badenv not in env("list")


@pytest.mark.regression("39248")
@pytest.mark.parametrize(
    "error,message,contents",
    [
        (
            spack.config.ConfigFormatError,
            "not of type",
            """\
spack:
  specs: mpi@2.0
""",
        ),
        (
            ev.SpackEnvironmentConfigError,
            "duplicate key",
            """\
spack:
  packages:
    all:
      providers:
        mpi: [mvapich2]
        mpi: [mpich]
""",
        ),
        (
            spack.config.ConfigFormatError,
            "'specks' was unexpected",
            """\
spack:
  specks:
    - libdwarf
""",
        ),
    ],
)
def test_bad_env_yaml_create_fails(tmp_path, mutable_mock_env_path, error, message, contents):
    """Ensure creation with invalid yaml does NOT create or leave the environment."""
    filename = tmp_path / ev.manifest_name
    filename.write_text(contents)
    env_name = "bad_env"
    with pytest.raises(error, match=message):
        env("create", env_name, str(filename))

    assert env_name not in env("list")
    manifest = mutable_mock_env_path / env_name / ev.manifest_name
    assert not os.path.exists(str(manifest))


@pytest.mark.regression("39248")
@pytest.mark.parametrize("answer", ["-y", ""])
def test_multi_env_remove(mutable_mock_env_path, monkeypatch, answer):
    """Test removal (or not) of a valid and invalid environment"""
    remove_environment = answer == "-y"
    monkeypatch.setattr(tty, "get_yes_or_no", lambda prompt, default: remove_environment)

    environments = ["goodenv", "badenv"]
    for e in environments:
        env("create", e)

    # Ensure the bad environment contains invalid yaml
    filename = mutable_mock_env_path / environments[1] / ev.manifest_name
    filename.write_text(
        """\
    - libdwarf
"""
    )

    assert all(e in env("list") for e in environments)

    args = [answer] if answer else []
    args.extend(environments)
    output = env("remove", *args, fail_on_error=False)

    if remove_environment is True:
        # Successfully removed (and reported removal) of *both* environments
        assert not all(e in env("list") for e in environments)
        assert output.count("Successfully removed") == len(environments)
    else:
        # Not removing any of the environments
        assert all(e in env("list") for e in environments)


def test_env_loads(install_mockery, mock_fetch, mock_modules_root):
    env("create", "test")

    with ev.read("test"):
        add("mpileaks")
        concretize()
        install("--fake")
        module("tcl", "refresh", "-y")

    with ev.read("test"):
        env("loads")

    e = ev.read("test")

    loads_file = os.path.join(e.path, "loads")
    assert os.path.exists(loads_file)

    with open(loads_file) as f:
        contents = f.read()
        assert "module load mpileaks" in contents


@pytest.mark.disable_clean_stage_check
def test_stage(mock_stage, mock_fetch, install_mockery):
    env("create", "test")
    with ev.read("test"):
        add("mpileaks")
        add("zmpi")
        concretize()
        stage()

    root = str(mock_stage)

    def check_stage(spec):
        spec = Spec(spec).concretized()
        for dep in spec.traverse():
            stage_name = "{0}{1}-{2}-{3}".format(
                stage_prefix, dep.name, dep.version, dep.dag_hash()
            )
            assert os.path.isdir(os.path.join(root, stage_name))

    check_stage("mpileaks")
    check_stage("zmpi")


def test_env_commands_die_with_no_env_arg():
    # these fail in argparse when given no arg
    with pytest.raises(SystemExit):
        env("create")
    with pytest.raises(SystemExit):
        env("remove")

    # these have an optional env arg and raise errors via tty.die
    with pytest.raises(SpackCommandError):
        env("loads")

    # This should NOT raise an error with no environment
    # it just tells the user there isn't an environment
    env("status")


def test_env_blocks_uninstall(mock_stage, mock_fetch, install_mockery):
    env("create", "test")
    with ev.read("test"):
        add("mpileaks")
        install("--fake")

    out = uninstall("mpileaks", fail_on_error=False)
    assert uninstall.returncode == 1
    assert "The following environments still reference these specs" in out


def test_roots_display_with_variants():
    env("create", "test")
    with ev.read("test"):
        add("boost+shared")

    with ev.read("test"):
        out = find(output=str)

    assert "boost +shared" in out


def test_uninstall_keeps_in_env(mock_stage, mock_fetch, install_mockery):
    # 'spack uninstall' without --remove should not change the environment
    # spack.yaml file, just uninstall specs
    env("create", "test")
    with ev.read("test"):
        add("mpileaks")
        add("libelf")
        install("--fake")

    test = ev.read("test")
    # Save this spec to check later if it is still in the env
    (mpileaks_hash,) = list(x for x, y in test.specs_by_hash.items() if y.name == "mpileaks")
    orig_user_specs = test.user_specs
    orig_concretized_specs = test.concretized_order

    with ev.read("test"):
        uninstall("-ya")

    test = ev.read("test")
    assert test.concretized_order == orig_concretized_specs
    assert test.user_specs.specs == orig_user_specs.specs
    assert mpileaks_hash in test.specs_by_hash
    assert not test.specs_by_hash[mpileaks_hash].package.installed


def test_uninstall_removes_from_env(mock_stage, mock_fetch, install_mockery):
    # 'spack uninstall --remove' should update the environment
    env("create", "test")
    with ev.read("test"):
        add("mpileaks")
        add("libelf")
        install("--fake")

    with ev.read("test"):
        uninstall("-y", "-a", "--remove")

    test = ev.read("test")
    assert not test.specs_by_hash
    assert not test.concretized_order
    assert not test.user_specs


@pytest.mark.usefixtures("config")
def test_indirect_build_dep(tmp_path):
    """Simple case of X->Y->Z where Y is a build/link dep and Z is a
    build-only dep. Make sure this concrete DAG is preserved when writing the
    environment out and reading it back.
    """
    builder = spack.repo.MockRepositoryBuilder(tmp_path / "repo")
    builder.add_package("z")
    builder.add_package("y", dependencies=[("z", "build", None)])
    builder.add_package("x", dependencies=[("y", None, None)])

    with spack.repo.use_repositories(builder.root):
        x_spec = Spec("x")
        x_concretized = x_spec.concretized()

        _env_create("test", with_view=False)
        e = ev.read("test")
        e.add(x_spec)
        e.concretize()
        e.write()

        e_read = ev.read("test")
        (x_env_hash,) = e_read.concretized_order

        x_env_spec = e_read.specs_by_hash[x_env_hash]
        assert x_env_spec == x_concretized


@pytest.mark.usefixtures("config")
def test_store_different_build_deps(tmp_path):
    r"""Ensure that an environment can store two instances of a build-only
    dependency::

              x       y
             /| (l)   | (b)
        (b) | y       z2
             \| (b)
              z1

    """
    builder = spack.repo.MockRepositoryBuilder(tmp_path / "mirror")
    builder.add_package("z")
    builder.add_package("y", dependencies=[("z", "build", None)])
    builder.add_package("x", dependencies=[("y", None, None), ("z", "build", None)])

    with spack.repo.use_repositories(builder.root):
        y_spec = Spec("y ^z@3")
        y_concretized = y_spec.concretized()

        x_spec = Spec("x ^z@2")
        x_concretized = x_spec.concretized()

        # Even though x chose a different 'z', the y it chooses should be identical
        # *aside* from the dependency on 'z'.  The dag_hash() will show the difference
        # in build dependencies.
        assert x_concretized["y"].eq_node(y_concretized)
        assert x_concretized["y"].dag_hash() != y_concretized.dag_hash()

        _env_create("test", with_view=False)
        e = ev.read("test")
        e.add(y_spec)
        e.add(x_spec)
        e.concretize()
        e.write()

        e_read = ev.read("test")
        y_env_hash, x_env_hash = e_read.concretized_order

        y_read = e_read.specs_by_hash[y_env_hash]
        x_read = e_read.specs_by_hash[x_env_hash]

        # make sure the DAG hashes and build deps are preserved after
        # a round trip to/from the lockfile
        assert x_read["z"] != y_read["z"]
        assert x_read["z"].dag_hash() != y_read["z"].dag_hash()

        assert x_read["y"].eq_node(y_read)
        assert x_read["y"].dag_hash() != y_read.dag_hash()


def test_env_updates_view_install(tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    with ev.read("test"):
        add("mpileaks")
        install("--fake")

    check_mpileaks_and_deps_in_view(view_dir)


def test_env_view_fails(tmpdir, mock_packages, mock_stage, mock_fetch, install_mockery):
    # We currently ignore file-file conflicts for the prefix merge,
    # so in principle there will be no errors in this test. But
    # the .spack metadata dir is handled separately and is more strict.
    # It also throws on file-file conflicts. That's what we're checking here
    # by adding the same package twice to a view.
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    with ev.read("test"):
        add("libelf")
        add("libelf cflags=-g")
        with pytest.raises(
            ev.SpackEnvironmentViewError, match="two specs project to the same prefix"
        ):
            install("--fake")


def test_env_view_fails_dir_file(tmpdir, mock_packages, mock_stage, mock_fetch, install_mockery):
    # This environment view fails to be created because a file
    # and a dir are in the same path. Test that it mentions the problematic path.
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    with ev.read("test"):
        add("view-dir-file")
        add("view-dir-dir")
        with pytest.raises(
            llnl.util.link_tree.MergeConflictSummary, match=os.path.join("bin", "x")
        ):
            install()


def test_env_view_succeeds_symlinked_dir_file(
    tmpdir, mock_packages, mock_stage, mock_fetch, install_mockery
):
    # A symlinked dir and an ordinary dir merge happily
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    with ev.read("test"):
        add("view-dir-symlinked-dir")
        add("view-dir-dir")
        install()
        x_dir = os.path.join(str(view_dir), "bin", "x")
        assert os.path.exists(os.path.join(x_dir, "file_in_dir"))
        assert os.path.exists(os.path.join(x_dir, "file_in_symlinked_dir"))


def test_env_without_view_install(tmpdir, mock_stage, mock_fetch, install_mockery):
    # Test enabling a view after installing specs
    env("create", "--without-view", "test")

    test_env = ev.read("test")
    with pytest.raises(ev.SpackEnvironmentError):
        test_env.default_view

    view_dir = tmpdir.join("view")

    with ev.read("test"):
        add("mpileaks")
        install("--fake")

        env("view", "enable", str(view_dir))

    # After enabling the view, the specs should be linked into the environment
    # view dir
    check_mpileaks_and_deps_in_view(view_dir)


def test_env_config_view_default(
    environment_from_manifest, mock_stage, mock_fetch, install_mockery
):
    # This config doesn't mention whether a view is enabled
    environment_from_manifest(
        """
spack:
  specs:
  - mpileaks
"""
    )

    with ev.read("test"):
        install("--fake")

    e = ev.read("test")

    # Check that metadata folder for this spec exists
    assert os.path.isdir(os.path.join(e.default_view.view()._root, ".spack", "mpileaks"))


def test_env_updates_view_install_package(tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    with ev.read("test"):
        install("--fake", "--add", "mpileaks")

    assert os.path.exists(str(view_dir.join(".spack/mpileaks")))


def test_env_updates_view_add_concretize(tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    install("--fake", "mpileaks")
    with ev.read("test"):
        add("mpileaks")
        concretize()

    check_mpileaks_and_deps_in_view(view_dir)


def test_env_updates_view_uninstall(tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    with ev.read("test"):
        install("--fake", "--add", "mpileaks")

    check_mpileaks_and_deps_in_view(view_dir)

    with ev.read("test"):
        uninstall("-ay")

    check_viewdir_removal(view_dir)


def test_env_updates_view_uninstall_referenced_elsewhere(
    tmpdir, mock_stage, mock_fetch, install_mockery
):
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    install("--fake", "mpileaks")
    with ev.read("test"):
        add("mpileaks")
        concretize()

    check_mpileaks_and_deps_in_view(view_dir)

    with ev.read("test"):
        uninstall("-ay")

    check_viewdir_removal(view_dir)


def test_env_updates_view_remove_concretize(tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    install("--fake", "mpileaks")
    with ev.read("test"):
        add("mpileaks")
        concretize()

    check_mpileaks_and_deps_in_view(view_dir)

    with ev.read("test"):
        remove("mpileaks")
        concretize()

    check_viewdir_removal(view_dir)


def test_env_updates_view_force_remove(tmpdir, mock_stage, mock_fetch, install_mockery):
    view_dir = tmpdir.join("view")
    env("create", "--with-view=%s" % view_dir, "test")
    with ev.read("test"):
        install("--add", "--fake", "mpileaks")

    check_mpileaks_and_deps_in_view(view_dir)

    with ev.read("test"):
        remove("-f", "mpileaks")

    check_viewdir_removal(view_dir)


def test_env_activate_view_fails(tmpdir, mock_stage, mock_fetch, install_mockery):
    """Sanity check on env activate to make sure it requires shell support"""
    out = env("activate", "test")
    assert "To set up shell support" in out


def test_stack_yaml_definitions(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        test = ev.read("test")

        assert Spec("mpileaks") in test.user_specs
        assert Spec("callpath") in test.user_specs


def test_stack_yaml_definitions_as_constraints(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - mpis: [mpich, openmpi]
  specs:
    - matrix:
      - [$packages]
      - [$^mpis]
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        test = ev.read("test")

        assert Spec("mpileaks^mpich") in test.user_specs
        assert Spec("callpath^mpich") in test.user_specs
        assert Spec("mpileaks^openmpi") in test.user_specs
        assert Spec("callpath^openmpi") in test.user_specs


def test_stack_yaml_definitions_as_constraints_on_matrix(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - mpis:
      - matrix:
        - [mpich]
        - ['@3.0.4', '@3.0.3']
  specs:
    - matrix:
      - [$packages]
      - [$^mpis]
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        test = ev.read("test")

        assert Spec("mpileaks^mpich@3.0.4") in test.user_specs
        assert Spec("callpath^mpich@3.0.4") in test.user_specs
        assert Spec("mpileaks^mpich@3.0.3") in test.user_specs
        assert Spec("callpath^mpich@3.0.3") in test.user_specs


@pytest.mark.regression("12095")
def test_stack_yaml_definitions_write_reference(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - indirect: [$packages]
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")

        with ev.read("test"):
            concretize()
        test = ev.read("test")

        assert Spec("mpileaks") in test.user_specs
        assert Spec("callpath") in test.user_specs


def test_stack_yaml_add_to_list(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            add("-l", "packages", "libelf")

        test = ev.read("test")

        assert Spec("libelf") in test.user_specs
        assert Spec("mpileaks") in test.user_specs
        assert Spec("callpath") in test.user_specs


def test_stack_yaml_remove_from_list(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            remove("-l", "packages", "mpileaks")

        test = ev.read("test")

        assert Spec("mpileaks") not in test.user_specs
        assert Spec("callpath") in test.user_specs


def test_stack_yaml_remove_from_list_force(tmp_path):
    spack_yaml = tmp_path / ev.manifest_name
    spack_yaml.write_text(
        """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
  specs:
    - matrix:
        - [$packages]
        - [^mpich, ^zmpi]
"""
    )

    env("create", "test", str(spack_yaml))
    with ev.read("test"):
        concretize()
        remove("-f", "-l", "packages", "mpileaks")
        find_output = find("-c")

    assert "mpileaks" not in find_output

    test = ev.read("test")
    assert len(test.user_specs) == 2
    assert Spec("callpath ^zmpi") in test.user_specs
    assert Spec("callpath ^mpich") in test.user_specs


def test_stack_yaml_remove_from_matrix_no_effect(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages:
        - matrix:
            - [mpileaks, callpath]
            - [target=be]
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test") as e:
            before = e.user_specs.specs
            remove("-l", "packages", "mpileaks")
            after = e.user_specs.specs

            assert before == after


def test_stack_yaml_force_remove_from_matrix(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages:
        - matrix:
            - [mpileaks, callpath]
            - [target=be]
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test") as e:
            e.concretize()

            before_user = e.user_specs.specs
            before_conc = e.concretized_user_specs

            remove("-f", "-l", "packages", "mpileaks")

            after_user = e.user_specs.specs
            after_conc = e.concretized_user_specs

            assert before_user == after_user

            mpileaks_spec = Spec("mpileaks target=be")
            assert mpileaks_spec in before_conc
            assert mpileaks_spec not in after_conc


def test_stack_concretize_extraneous_deps(tmpdir, config, mock_packages):
    # FIXME: The new concretizer doesn't handle yet soft
    # FIXME: constraints for stacks
    # FIXME: This now works for statically-determinable invalid deps
    # FIXME: But it still does not work for dynamically determined invalid deps
    # if spack.config.get('config:concretizer') == 'clingo':
    #    pytest.skip('Clingo concretizer does not support soft constraints')

    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - install:
        - matrix:
            - [$packages]
            - ['^zmpi', '^mpich']
  specs:
    - $install
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            concretize()

        test = ev.read("test")

        for user, concrete in test.concretized_specs():
            assert concrete.concrete
            assert not user.concrete
            if user.name == "libelf":
                assert not concrete.satisfies("^mpi")
            elif user.name == "mpileaks":
                assert concrete.satisfies("^mpi")


def test_stack_concretize_extraneous_variants(tmpdir, config, mock_packages):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - install:
        - matrix:
            - [$packages]
            - ['~shared', '+shared']
  specs:
    - $install
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            concretize()

        test = ev.read("test")

        for user, concrete in test.concretized_specs():
            assert concrete.concrete
            assert not user.concrete
            if user.name == "libelf":
                assert "shared" not in concrete.variants
            if user.name == "mpileaks":
                assert concrete.variants["shared"].value == user.variants["shared"].value


def test_stack_concretize_extraneous_variants_with_dash(tmpdir, config, mock_packages):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - install:
        - matrix:
            - [$packages]
            - ['shared=False', '+shared-libs']
  specs:
    - $install
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            concretize()

        ev.read("test")

        # Regression test for handling of variants with dashes in them
        # will fail before this point if code regresses
        assert True


def test_stack_definition_extension(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")

        test = ev.read("test")

        assert Spec("libelf") in test.user_specs
        assert Spec("mpileaks") in test.user_specs
        assert Spec("callpath") in test.user_specs


def test_stack_definition_conditional_false(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: 'False'
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")

        test = ev.read("test")

        assert Spec("libelf") in test.user_specs
        assert Spec("mpileaks") in test.user_specs
        assert Spec("callpath") not in test.user_specs


def test_stack_definition_conditional_true(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: 'True'
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")

        test = ev.read("test")

        assert Spec("libelf") in test.user_specs
        assert Spec("mpileaks") in test.user_specs
        assert Spec("callpath") in test.user_specs


def test_stack_definition_conditional_with_variable(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: platform == 'test'
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")

        test = ev.read("test")

        assert Spec("libelf") in test.user_specs
        assert Spec("mpileaks") in test.user_specs
        assert Spec("callpath") in test.user_specs


def test_stack_definition_conditional_with_satisfaction(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
      when: arch.satisfies('platform=foo')  # will be "test" when testing
    - packages: [callpath]
      when: arch.satisfies('platform=test')
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")

        test = ev.read("test")

        assert Spec("libelf") not in test.user_specs
        assert Spec("mpileaks") not in test.user_specs
        assert Spec("callpath") in test.user_specs


def test_stack_definition_complex_conditional(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: re.search(r'foo', hostname) and env['test'] == 'THISSHOULDBEFALSE'
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")

        test = ev.read("test")

        assert Spec("libelf") in test.user_specs
        assert Spec("mpileaks") in test.user_specs
        assert Spec("callpath") not in test.user_specs


def test_stack_definition_conditional_invalid_variable(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: bad_variable == 'test'
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        with pytest.raises(NameError):
            env("create", "test", "./spack.yaml")


def test_stack_definition_conditional_add_write(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - packages: [callpath]
      when: platform == 'test'
  specs:
    - $packages
"""
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            add("-l", "packages", "zmpi")

        test = ev.read("test")

        packages_lists = list(
            filter(lambda x: "packages" in x, test.manifest["spack"]["definitions"])
        )

        assert len(packages_lists) == 2
        assert "callpath" not in packages_lists[0]["packages"]
        assert "callpath" in packages_lists[1]["packages"]
        assert "zmpi" in packages_lists[0]["packages"]
        assert "zmpi" not in packages_lists[1]["packages"]


def test_stack_combinatorial_view(
    tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery
):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      projections:
        'all': '{name}/{version}-{compiler.name}'"""
            % viewdir
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        test = ev.read("test")
        for spec in test._get_environment_specs():
            assert os.path.exists(
                os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
            )


def test_stack_view_select(tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      select: ['%%gcc']
      projections:
        'all': '{name}/{version}-{compiler.name}'"""
            % viewdir
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        test = ev.read("test")
        for spec in test._get_environment_specs():
            if spec.satisfies("%gcc"):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )


def test_stack_view_exclude(tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      exclude: [callpath]
      projections:
        'all': '{name}/{version}-{compiler.name}'"""
            % viewdir
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        test = ev.read("test")
        for spec in test._get_environment_specs():
            if not spec.satisfies("callpath"):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )


def test_stack_view_select_and_exclude(
    tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery
):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      select: ['%%gcc']
      exclude: [callpath]
      projections:
        'all': '{name}/{version}-{compiler.name}'"""
            % viewdir
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        test = ev.read("test")
        for spec in test._get_environment_specs():
            if spec.satisfies("%gcc") and not spec.satisfies("callpath"):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )


def test_view_link_roots(tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      select: ['%%gcc']
      exclude: [callpath]
      link: 'roots'
      projections:
        'all': '{name}/{version}-{compiler.name}'"""
            % viewdir
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        test = ev.read("test")
        for spec in test._get_environment_specs():
            if spec in test.roots() and (
                spec.satisfies("%gcc") and not spec.satisfies("callpath")
            ):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )


def test_view_link_run(tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery):
    yaml = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    envdir = str(tmpdir)
    with open(yaml, "w") as f:
        f.write(
            """
spack:
  specs:
  - dttop

  view:
    combinatorial:
      root: %s
      link: run
      projections:
        all: '{name}'"""
            % viewdir
        )

    with ev.Environment(envdir):
        install()

    # make sure transitive run type deps are in the view
    for pkg in ("dtrun1", "dtrun3"):
        assert os.path.exists(os.path.join(viewdir, pkg))

    # and non-run-type deps are not.
    for pkg in (
        "dtlink1",
        "dtlink2",
        "dtlink3",
        "dtlink4",
        "dtlink5" "dtbuild1",
        "dtbuild2",
        "dtbuild3",
    ):
        assert not os.path.exists(os.path.join(viewdir, pkg))


@pytest.mark.parametrize("link_type", ["hardlink", "copy", "symlink"])
def test_view_link_type(
    link_type, tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery
):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  specs:
    - mpileaks
  view:
    default:
      root: %s
      link_type: %s"""
            % (viewdir, link_type)
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        test = ev.read("test")

        for spec in test.roots():
            file_path = test.default_view.view()._root
            file_to_test = os.path.join(file_path, spec.name)
            assert os.path.isfile(file_to_test)
            assert os.path.islink(file_to_test) == (link_type == "symlink")


def test_view_link_all(tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, callpath]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    combinatorial:
      root: %s
      select: ['%%gcc']
      exclude: [callpath]
      link: 'all'
      projections:
        'all': '{name}/{version}-{compiler.name}'"""
            % viewdir
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        test = ev.read("test")
        for spec in test._get_environment_specs():
            if spec.satisfies("%gcc") and not spec.satisfies("callpath"):
                assert os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )
            else:
                assert not os.path.exists(
                    os.path.join(viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name))
                )


def test_stack_view_activate_from_default(
    tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery
):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, cmake]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    default:
      root: %s
      select: ['%%gcc']"""
            % viewdir
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        shell = env("activate", "--sh", "test")

        assert "PATH" in shell
        assert os.path.join(viewdir, "bin") in shell
        assert "FOOBAR=mpileaks" in shell


def test_stack_view_no_activate_without_default(
    tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery
):
    filename = str(tmpdir.join("spack.yaml"))
    viewdir = str(tmpdir.join("view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, cmake]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    not-default:
      root: %s
      select: ['%%gcc']"""
            % viewdir
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        shell = env("activate", "--sh", "test")
        assert "PATH" not in shell
        assert viewdir not in shell


def test_stack_view_multiple_views(
    tmpdir, mock_fetch, mock_packages, mock_archive, install_mockery
):
    filename = str(tmpdir.join("spack.yaml"))
    default_viewdir = str(tmpdir.join("default-view"))
    combin_viewdir = str(tmpdir.join("combinatorial-view"))
    with open(filename, "w") as f:
        f.write(
            """\
spack:
  definitions:
    - packages: [mpileaks, cmake]
    - compilers: ['%%gcc', '%%clang']
  specs:
    - matrix:
        - [$packages]
        - [$compilers]

  view:
    default:
      root: %s
      select: ['%%gcc']
    combinatorial:
      root: %s
      exclude: [callpath %%gcc]
      projections:
        'all': '{name}/{version}-{compiler.name}'"""
            % (default_viewdir, combin_viewdir)
        )
    with tmpdir.as_cwd():
        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            install()

        shell = env("activate", "--sh", "test")
        assert "PATH" in shell
        assert os.path.join(default_viewdir, "bin") in shell

        test = ev.read("test")
        for spec in test._get_environment_specs():
            if not spec.satisfies("callpath%gcc"):
                assert os.path.exists(
                    os.path.join(
                        combin_viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name)
                    )
                )
            else:
                assert not os.path.exists(
                    os.path.join(
                        combin_viewdir, spec.name, "%s-%s" % (spec.version, spec.compiler.name)
                    )
                )


def test_env_activate_sh_prints_shell_output(tmpdir, mock_stage, mock_fetch, install_mockery):
    """Check the shell commands output by ``spack env activate --sh``.

    This is a cursory check; ``share/spack/qa/setup-env-test.sh`` checks
    for correctness.
    """
    env("create", "test")

    out = env("activate", "--sh", "test")
    assert "export SPACK_ENV=" in out
    assert "export PS1=" not in out
    assert "alias despacktivate=" in out

    out = env("activate", "--sh", "--prompt", "test")
    assert "export SPACK_ENV=" in out
    assert "export PS1=" in out
    assert "alias despacktivate=" in out


def test_env_activate_csh_prints_shell_output(tmpdir, mock_stage, mock_fetch, install_mockery):
    """Check the shell commands output by ``spack env activate --csh``."""
    env("create", "test")

    out = env("activate", "--csh", "test")
    assert "setenv SPACK_ENV" in out
    assert "setenv set prompt" not in out
    assert "alias despacktivate" in out

    out = env("activate", "--csh", "--prompt", "test")
    assert "setenv SPACK_ENV" in out
    assert "set prompt=" in out
    assert "alias despacktivate" in out


@pytest.mark.regression("12719")
def test_env_activate_default_view_root_unconditional(mutable_mock_env_path):
    """Check that the root of the default view in the environment is added
    to the shell unconditionally."""
    env("create", "test")

    with ev.read("test") as e:
        viewdir = e.default_view.root

    out = env("activate", "--sh", "test")
    viewdir_bin = os.path.join(viewdir, "bin")

    assert (
        "export PATH={0}".format(viewdir_bin) in out
        or "export PATH='{0}".format(viewdir_bin) in out
        or 'export PATH="{0}'.format(viewdir_bin) in out
    )


def test_env_activate_custom_view(tmp_path: pathlib.Path, mock_packages):
    """Check that an environment can be activated with a non-default view."""
    env_template = tmp_path / "spack.yaml"
    default_dir = tmp_path / "defaultdir"
    nondefaultdir = tmp_path / "nondefaultdir"
    with open(env_template, "w") as f:
        f.write(
            f"""\
spack:
  specs: [a]
  view:
    default:
      root: {default_dir}
    nondefault:
      root: {nondefaultdir}"""
        )
    env("create", "test", str(env_template))
    shell = env("activate", "--sh", "--with-view", "nondefault", "test")
    assert os.path.join(nondefaultdir, "bin") in shell


def test_concretize_user_specs_together():
    e = ev.create("coconcretization")
    e.unify = True

    # Concretize a first time using 'mpich' as the MPI provider
    e.add("mpileaks")
    e.add("mpich")
    e.concretize()

    assert all("mpich" in spec for _, spec in e.concretized_specs())
    assert all("mpich2" not in spec for _, spec in e.concretized_specs())

    # Concretize a second time using 'mpich2' as the MPI provider
    e.remove("mpich")
    e.add("mpich2")

    exc_cls = spack.error.SpackError
    if spack.config.get("config:concretizer") == "clingo":
        exc_cls = spack.error.UnsatisfiableSpecError

    # Concretizing without invalidating the concrete spec for mpileaks fails
    with pytest.raises(exc_cls):
        e.concretize()
    e.concretize(force=True)

    assert all("mpich2" in spec for _, spec in e.concretized_specs())
    assert all("mpich" not in spec for _, spec in e.concretized_specs())

    # Concretize again without changing anything, check everything
    # stays the same
    e.concretize()

    assert all("mpich2" in spec for _, spec in e.concretized_specs())
    assert all("mpich" not in spec for _, spec in e.concretized_specs())


def test_cant_install_single_spec_when_concretizing_together():
    e = ev.create("coconcretization")
    e.unify = True

    with pytest.raises(ev.SpackEnvironmentError, match=r"cannot install"):
        e.concretize_and_add("zlib")
        e.install_all()


def test_duplicate_packages_raise_when_concretizing_together():
    e = ev.create("coconcretization")
    e.unify = True

    e.add("mpileaks+opt")
    e.add("mpileaks~opt")
    e.add("mpich")

    exc_cls, match = spack.error.SpackError, None
    if spack.config.get("config:concretizer") == "clingo":
        exc_cls = spack.error.UnsatisfiableSpecError
        match = r"You could consider setting `concretizer:unify`"

    with pytest.raises(exc_cls, match=match):
        e.concretize()


def test_env_write_only_non_default():
    env("create", "test")

    e = ev.read("test")
    with open(e.manifest_path, "r") as f:
        yaml = f.read()

    assert yaml == ev.default_manifest_yaml()


@pytest.mark.regression("20526")
def test_env_write_only_non_default_nested(tmpdir):
    # setup an environment file
    # the environment includes configuration because nested configs proved the
    # most difficult to avoid writing.
    filename = "spack.yaml"
    filepath = str(tmpdir.join(filename))
    contents = """\
spack:
  specs:
  - matrix:
    - [mpileaks]
  packages:
    all:
      compiler: [gcc]
  view: true
"""

    # create environment with some structure
    with open(filepath, "w") as f:
        f.write(contents)
    env("create", "test", filepath)

    # concretize
    with ev.read("test") as e:
        concretize()
        e.write()

        with open(e.manifest_path, "r") as f:
            manifest = f.read()

    assert manifest == contents


@pytest.mark.regression("18147")
def test_can_update_attributes_with_override(tmpdir):
    spack_yaml = """
spack:
  mirrors::
    test: /foo/bar
  packages:
    cmake:
      paths:
        cmake@3.18.1: /usr
  specs:
  - hdf5
"""
    abspath = tmpdir.join("spack.yaml")
    abspath.write(spack_yaml)

    # Check that an update does not raise
    env("update", "-y", str(abspath.dirname))


@pytest.mark.regression("18338")
def test_newline_in_commented_sequence_is_not_an_issue(tmpdir):
    spack_yaml = """
spack:
  specs:
  - dyninst
  packages:
    libelf:
      externals:
      - spec: libelf@0.8.13
        modules:
        - libelf/3.18.1

  concretizer:
    unify: false
"""
    abspath = tmpdir.join("spack.yaml")
    abspath.write(spack_yaml)

    def extract_dag_hash(environment):
        _, dyninst = next(iter(environment.specs_by_hash.items()))
        return dyninst["libelf"].dag_hash()

    # Concretize a first time and create a lockfile
    with ev.Environment(str(tmpdir)) as e:
        concretize()
        libelf_first_hash = extract_dag_hash(e)

    # Check that a second run won't error
    with ev.Environment(str(tmpdir)) as e:
        concretize()
        libelf_second_hash = extract_dag_hash(e)

    assert libelf_first_hash == libelf_second_hash


@pytest.mark.regression("18441")
def test_lockfile_not_deleted_on_write_error(tmpdir, monkeypatch):
    raw_yaml = """
spack:
  specs:
  - dyninst
  packages:
    libelf:
      externals:
      - spec: libelf@0.8.13
        prefix: /usr
"""
    spack_yaml = tmpdir.join("spack.yaml")
    spack_yaml.write(raw_yaml)
    spack_lock = tmpdir.join("spack.lock")

    # Concretize a first time and create a lockfile
    with ev.Environment(str(tmpdir)):
        concretize()
    assert os.path.exists(str(spack_lock))

    # If I run concretize again and there's an error during write,
    # the spack.lock file shouldn't disappear from disk
    def _write_helper_raise(self):
        raise RuntimeError("some error")

    monkeypatch.setattr(
        spack.environment.environment.EnvironmentManifestFile, "flush", _write_helper_raise
    )
    with ev.Environment(str(tmpdir)) as e:
        e.concretize(force=True)
        with pytest.raises(RuntimeError):
            e.clear()
            e.write()
    assert os.path.exists(str(spack_lock))


def _setup_develop_packages(tmpdir):
    """Sets up a structure ./init_env/spack.yaml, ./build_folder, ./dest_env
    where spack.yaml has a relative develop path to build_folder"""
    init_env = tmpdir.join("init_env")
    build_folder = tmpdir.join("build_folder")
    dest_env = tmpdir.join("dest_env")

    fs.mkdirp(str(init_env))
    fs.mkdirp(str(build_folder))
    fs.mkdirp(str(dest_env))

    raw_yaml = """
spack:
  specs: ['mypkg1', 'mypkg2']
  develop:
    mypkg1:
      path: ../build_folder
      spec: mypkg@main
    mypkg2:
      path: /some/other/path
      spec: mypkg@main
"""
    spack_yaml = init_env.join("spack.yaml")
    spack_yaml.write(raw_yaml)

    return init_env, build_folder, dest_env, spack_yaml


def test_rewrite_rel_dev_path_new_dir(tmpdir):
    """Relative develop paths should be rewritten for new environments in
    a different directory from the original manifest file"""
    _, build_folder, dest_env, spack_yaml = _setup_develop_packages(tmpdir)

    env("create", "-d", str(dest_env), str(spack_yaml))
    with ev.Environment(str(dest_env)) as e:
        assert e.dev_specs["mypkg1"]["path"] == str(build_folder)
        assert e.dev_specs["mypkg2"]["path"] == sep + os.path.join("some", "other", "path")


def test_rewrite_rel_dev_path_named_env(tmpdir):
    """Relative develop paths should by default be rewritten for new named
    environment"""
    _, build_folder, _, spack_yaml = _setup_develop_packages(tmpdir)
    env("create", "named_env", str(spack_yaml))
    with ev.read("named_env") as e:
        assert e.dev_specs["mypkg1"]["path"] == str(build_folder)
        assert e.dev_specs["mypkg2"]["path"] == sep + os.path.join("some", "other", "path")


def test_does_not_rewrite_rel_dev_path_when_keep_relative_is_set(tmpdir):
    """Relative develop paths should not be rewritten when --keep-relative is
    passed to create"""
    _, _, _, spack_yaml = _setup_develop_packages(tmpdir)
    env("create", "--keep-relative", "named_env", str(spack_yaml))
    with ev.read("named_env") as e:
        assert e.dev_specs["mypkg1"]["path"] == "../build_folder"
        assert e.dev_specs["mypkg2"]["path"] == "/some/other/path"


@pytest.mark.regression("23440")
def test_custom_version_concretize_together(tmpdir):
    # Custom versions should be permitted in specs when
    # concretizing together
    e = ev.create("custom_version")
    e.unify = True

    # Concretize a first time using 'mpich' as the MPI provider
    e.add("hdf5@=myversion")
    e.add("mpich")
    e.concretize()

    assert any(spec.satisfies("hdf5@myversion") for _, spec in e.concretized_specs())


def test_modules_relative_to_views(environment_from_manifest, install_mockery, mock_fetch):
    environment_from_manifest(
        """
spack:
  specs:
  - trivial-install-test-package
  modules:
    default:
      enable:: [tcl]
      use_view: true
      roots:
        tcl: modules
"""
    )

    with ev.read("test") as e:
        install()

        spec = e.specs_by_hash[e.concretized_order[0]]
        view_prefix = e.default_view.get_projection_for_spec(spec)
        modules_glob = "%s/modules/**/*/*" % e.path
        modules = glob.glob(modules_glob)
        assert len(modules) == 1
        module = modules[0]

    with open(module, "r") as f:
        contents = f.read()

    assert view_prefix in contents
    assert spec.prefix not in contents


def test_multiple_modules_post_env_hook(environment_from_manifest, install_mockery, mock_fetch):
    environment_from_manifest(
        """
spack:
  specs:
  - trivial-install-test-package
  modules:
    default:
      enable:: [tcl]
      use_view: true
      roots:
        tcl: modules
    full:
      enable:: [tcl]
      roots:
        tcl: full_modules
"""
    )

    with ev.read("test") as e:
        install()

        spec = e.specs_by_hash[e.concretized_order[0]]
        view_prefix = e.default_view.get_projection_for_spec(spec)
        modules_glob = "%s/modules/**/*/*" % e.path
        modules = glob.glob(modules_glob)
        assert len(modules) == 1
        module = modules[0]

        full_modules_glob = "%s/full_modules/**/*/*" % e.path
        full_modules = glob.glob(full_modules_glob)
        assert len(full_modules) == 1
        full_module = full_modules[0]

    with open(module, "r") as f:
        contents = f.read()

    with open(full_module, "r") as f:
        full_contents = f.read()

    assert view_prefix in contents
    assert spec.prefix not in contents

    assert view_prefix not in full_contents
    assert spec.prefix in full_contents


@pytest.mark.regression("24148")
def test_virtual_spec_concretize_together(tmpdir):
    # An environment should permit to concretize "mpi"
    e = ev.create("virtual_spec")
    e.unify = True

    e.add("mpi")
    e.concretize()

    assert any(s.package.provides("mpi") for _, s in e.concretized_specs())


def test_query_develop_specs():
    """Test whether a spec is develop'ed or not"""
    env("create", "test")
    with ev.read("test") as e:
        e.add("mpich")
        e.add("mpileaks")
        e.develop(Spec("mpich@=1"), "here", clone=False)

        assert e.is_develop(Spec("mpich"))
        assert not e.is_develop(Spec("mpileaks"))


@pytest.mark.parametrize("method", [spack.cmd.env.env_activate, spack.cmd.env.env_deactivate])
@pytest.mark.parametrize(
    "env,no_env,env_dir", [("b", False, None), (None, True, None), (None, False, "path/")]
)
def test_activation_and_deactiviation_ambiguities(method, env, no_env, env_dir, capsys):
    """spack [-e x | -E | -D x/]  env [activate | deactivate] y are ambiguous"""
    args = Namespace(shell="sh", activate_env="a", env=env, no_env=no_env, env_dir=env_dir)
    with pytest.raises(SystemExit):
        method(args)
    _, err = capsys.readouterr()
    assert "is ambiguous" in err


@pytest.mark.regression("26548")
def test_custom_store_in_environment(mutable_config, tmpdir):
    spack_yaml = tmpdir.join("spack.yaml")
    install_root = tmpdir.join("store")
    spack_yaml.write(
        """
spack:
  specs:
  - libelf
  config:
    install_tree:
      root: {0}
""".format(
            install_root
        )
    )
    current_store_root = str(spack.store.STORE.root)
    assert str(current_store_root) != install_root
    with spack.environment.Environment(str(tmpdir)):
        assert str(spack.store.STORE.root) == install_root
    assert str(spack.store.STORE.root) == current_store_root


def test_activate_temp(monkeypatch, tmpdir):
    """Tests whether `spack env activate --temp` creates an environment in a
    temporary directory"""
    env_dir = lambda: str(tmpdir)
    monkeypatch.setattr(spack.cmd.env, "create_temp_env_directory", env_dir)
    shell = env("activate", "--temp", "--sh")
    active_env_var = next(line for line in shell.splitlines() if ev.spack_env_var in line)
    assert str(tmpdir) in active_env_var
    assert ev.is_env_dir(str(tmpdir))


def test_activate_default(monkeypatch):
    """Tests whether `spack env activate` creates / activates the default
    environment"""
    assert not ev.exists("default")

    # Activating it the first time should create it
    env("activate", "--sh")
    env("deactivate", "--sh")
    assert ev.exists("default")

    # Activating it while it already exists should work
    env("activate", "--sh")
    env("deactivate", "--sh")
    assert ev.exists("default")

    env("remove", "-y", "default")
    assert not ev.exists("default")


def test_env_view_fail_if_symlink_points_elsewhere(tmpdir, install_mockery, mock_fetch):
    view = str(tmpdir.join("view"))
    # Put a symlink to an actual directory in view
    non_view_dir = str(tmpdir.mkdir("dont-delete-me"))
    os.symlink(non_view_dir, view)
    with ev.create("env", with_view=view):
        add("libelf")
        install("--fake")
    assert os.path.isdir(non_view_dir)


def test_failed_view_cleanup(tmp_path, mock_stage, mock_fetch, install_mockery):
    """Tests whether Spack cleans up after itself when a view fails to create"""
    view_dir = tmp_path / "view"
    with ev.create("env", with_view=str(view_dir)):
        add("libelf")
        install("--fake")

    # Save the current view directory.
    resolved_view = view_dir.resolve(strict=True)
    all_views = resolved_view.parent
    views_before = list(all_views.iterdir())

    # Add a spec that results in view clash when creating a view
    with ev.read("env"):
        add("libelf cflags=-O3")
        with pytest.raises(ev.SpackEnvironmentViewError):
            install("--fake")

    # Make sure there is no broken view in the views directory, and the current
    # view is the original view from before the failed regenerate attempt.
    views_after = list(all_views.iterdir())
    assert views_before == views_after
    assert view_dir.samefile(resolved_view), view_dir


def test_environment_view_target_already_exists(tmpdir, mock_stage, mock_fetch, install_mockery):
    """When creating a new view, Spack should check whether
    the new view dir already exists. If so, it should not be
    removed or modified."""

    # Create a new environment
    view = str(tmpdir.join("view"))
    env("create", "--with-view={0}".format(view), "test")
    with ev.read("test"):
        add("libelf")
        install("--fake")

    # Empty the underlying view
    real_view = os.path.realpath(view)
    assert os.listdir(real_view)  # make sure it had *some* contents
    shutil.rmtree(real_view)

    # Replace it with something new.
    os.mkdir(real_view)
    fs.touch(os.path.join(real_view, "file"))

    # Remove the symlink so Spack can't know about the "previous root"
    os.unlink(view)

    # Regenerate the view, which should realize it can't write into the same dir.
    msg = "Failed to generate environment view"
    with ev.read("test"):
        with pytest.raises(ev.SpackEnvironmentViewError, match=msg):
            env("view", "regenerate")

    # Make sure the dir was left untouched.
    assert not os.path.lexists(view)
    assert os.listdir(real_view) == ["file"]


def test_environment_query_spec_by_hash(mock_stage, mock_fetch, install_mockery):
    env("create", "test")
    with ev.read("test"):
        add("libdwarf")
        concretize()
    with ev.read("test") as e:
        spec = e.matching_spec("libelf")
        install("/{0}".format(spec.dag_hash()))
    with ev.read("test") as e:
        assert not e.matching_spec("libdwarf").installed
        assert e.matching_spec("libelf").installed


@pytest.mark.parametrize("lockfile", ["v1", "v2", "v3"])
def test_read_old_lock_and_write_new(config, tmpdir, lockfile):
    # v1 lockfiles stored by a coarse DAG hash that did not include build deps.
    # They could not represent multiple build deps with different build hashes.
    #
    # v2 and v3 lockfiles are keyed by a "build hash", so they can represent specs
    # with different build deps but the same DAG hash. However, those two specs
    # could never have been built together, because they cannot coexist in a
    # Spack DB, which is keyed by DAG hash. The second one would just be a no-op
    # no-op because its DAG hash was already in the DB.
    #
    # Newer Spack uses a fine-grained DAG hash that includes build deps, package hash,
    # and more. But, we still have to identify old specs by their original DAG hash.
    # Essentially, the name (hash) we give something in Spack at concretization time is
    # its name forever (otherwise we'd need to relocate prefixes and disrupt existing
    # installations). So, we just discard the second conflicting dtbuild1 version when
    # reading v2 and v3 lockfiles. This is what old Spack would've done when installing
    # the environment, anyway.
    #
    # This test ensures the behavior described above.
    lockfile_path = os.path.join(spack.paths.test_path, "data", "legacy_env", "%s.lock" % lockfile)

    # read in the JSON from a legacy lockfile
    with open(lockfile_path) as f:
        old_dict = sjson.load(f)

    # read all DAG hashes from the legacy lockfile and record its shadowed DAG hash.
    old_hashes = set()
    shadowed_hash = None
    for key, spec_dict in old_dict["concrete_specs"].items():
        if "hash" not in spec_dict:
            # v1 and v2 key specs by their name in concrete_specs
            name, spec_dict = next(iter(spec_dict.items()))
        else:
            # v3 lockfiles have a `name` field and key by hash
            name = spec_dict["name"]

        # v1 lockfiles do not have a "hash" field -- they use the key.
        dag_hash = key if lockfile == "v1" else spec_dict["hash"]
        old_hashes.add(dag_hash)

        # v1 lockfiles can't store duplicate build dependencies, so they
        # will not have a shadowed hash.
        if lockfile != "v1":
            # v2 and v3 lockfiles store specs by build hash, so they can have multiple
            # keys for the same DAG hash. We discard the second one (dtbuild@1.0).
            if name == "dtbuild1" and spec_dict["version"] == "1.0":
                shadowed_hash = dag_hash

    # make an env out of the old lockfile -- env should be able to read v1/v2/v3
    test_lockfile_path = str(tmpdir.join("spack.lock"))
    shutil.copy(lockfile_path, test_lockfile_path)
    _env_create("test", init_file=test_lockfile_path, with_view=False)

    # re-read the old env as a new lockfile
    e = ev.read("test")
    hashes = set(e._to_lockfile_dict()["concrete_specs"])

    # v1 doesn't have duplicate build deps.
    # in v2 and v3, the shadowed hash will be gone.
    if shadowed_hash:
        old_hashes -= set([shadowed_hash])

    # make sure we see the same hashes in old and new lockfiles
    assert old_hashes == hashes


def test_read_v1_lock_creates_backup(config, tmp_path):
    """When reading a version-1 lockfile, make sure that a backup of that file
    is created.
    """
    v1_lockfile_path = pathlib.Path(spack.paths.test_path) / "data" / "legacy_env" / "v1.lock"
    test_lockfile_path = tmp_path / "init" / ev.lockfile_name
    test_lockfile_path.parent.mkdir(parents=True, exist_ok=False)
    shutil.copy(v1_lockfile_path, test_lockfile_path)

    e = ev.create_in_dir(tmp_path, init_file=test_lockfile_path)
    assert os.path.exists(e._lock_backup_v1_path)
    assert filecmp.cmp(e._lock_backup_v1_path, v1_lockfile_path)


@pytest.mark.parametrize("lockfile", ["v1", "v2", "v3"])
def test_read_legacy_lockfile_and_reconcretize(
    mock_stage, mock_fetch, install_mockery, lockfile, tmp_path
):
    # In legacy lockfiles v2 and v3 (keyed by build hash), there may be multiple
    # versions of the same spec with different build dependencies, which means
    # they will have different build hashes but the same DAG hash.
    # In the case of DAG hash conflicts, we always keep the spec associated with
    # whichever root spec came first in the "roots" list.
    #
    # After reconcretization with the *new*, finer-grained DAG hash, there should no
    # longer be conflicts, and the previously conflicting specs can coexist in the
    # same environment.
    test_path = pathlib.Path(spack.paths.test_path)
    lockfile_content = test_path / "data" / "legacy_env" / f"{lockfile}.lock"
    legacy_lockfile_path = tmp_path / ev.lockfile_name
    shutil.copy(lockfile_content, legacy_lockfile_path)

    # The order of the root specs in this environment is:
    #     [
    #         wci7a3a -> dttop ^dtbuild1@0.5,
    #         5zg6wxw -> dttop ^dtbuild1@1.0
    #     ]
    # So in v2 and v3 lockfiles we have two versions of dttop with the same DAG
    # hash but different build hashes.

    env("create", "test", str(legacy_lockfile_path))
    test = ev.read("test")
    assert len(test.specs_by_hash) == 1

    single_root = next(iter(test.specs_by_hash.values()))

    # v1 only has version 1.0, because v1 was keyed by DAG hash, and v1.0 overwrote
    # v0.5 on lockfile creation. v2 only has v0.5, because we specifically prefer
    # the one that would be installed when we read old lockfiles.
    if lockfile == "v1":
        assert single_root["dtbuild1"].version == Version("1.0")
    else:
        assert single_root["dtbuild1"].version == Version("0.5")

    # Now forcefully reconcretize
    with ev.read("test"):
        concretize("-f")

    # After reconcretizing, we should again see two roots, one depending on each
    # of the dtbuild1 versions specified in the roots of the original lockfile.
    test = ev.read("test")
    assert len(test.specs_by_hash) == 2

    expected_versions = set([Version("0.5"), Version("1.0")])
    current_versions = set(s["dtbuild1"].version for s in test.specs_by_hash.values())
    assert current_versions == expected_versions


def _parse_dry_run_package_installs(make_output):
    """Parse `spack install ... # <spec>` output from a make dry run."""
    return [
        Spec(line.split("# ")[1]).name
        for line in make_output.splitlines()
        if line.startswith("spack")
    ]


@pytest.mark.parametrize(
    "depfile_flags,expected_installs",
    [
        # This installs the full environment
        (
            ["--use-buildcache=never"],
            [
                "dtbuild1",
                "dtbuild2",
                "dtbuild3",
                "dtlink1",
                "dtlink2",
                "dtlink3",
                "dtlink4",
                "dtlink5",
                "dtrun1",
                "dtrun2",
                "dtrun3",
                "dttop",
            ],
        ),
        # This prunes build deps at depth > 0
        (
            ["--use-buildcache=package:never,dependencies:only"],
            [
                "dtbuild1",
                "dtlink1",
                "dtlink2",
                "dtlink3",
                "dtlink4",
                "dtlink5",
                "dtrun1",
                "dtrun2",
                "dtrun3",
                "dttop",
            ],
        ),
        # This prunes all build deps
        (
            ["--use-buildcache=only"],
            ["dtlink1", "dtlink3", "dtlink4", "dtlink5", "dtrun1", "dtrun3", "dttop"],
        ),
        # Test whether pruning of build deps is correct if we explicitly include one
        # that is also a dependency of a root.
        (
            ["--use-buildcache=only", "dttop", "dtbuild1"],
            [
                "dtbuild1",
                "dtlink1",
                "dtlink2",
                "dtlink3",
                "dtlink4",
                "dtlink5",
                "dtrun1",
                "dtrun2",
                "dtrun3",
                "dttop",
            ],
        ),
    ],
)
def test_environment_depfile_makefile(depfile_flags, expected_installs, tmpdir, mock_packages):
    env("create", "test")
    make = Executable("make")
    makefile = str(tmpdir.join("Makefile"))
    with ev.read("test"):
        add("dttop")
        concretize()

    # Disable jobserver so we can do a dry run.
    with ev.read("test"):
        env(
            "depfile",
            "-o",
            makefile,
            "--make-disable-jobserver",
            "--make-prefix=prefix",
            *depfile_flags,
        )

    # Do make dry run.
    out = make("-n", "-f", makefile, output=str)

    specs_that_make_would_install = _parse_dry_run_package_installs(out)

    # Check that all specs are there (without duplicates)
    assert set(specs_that_make_would_install) == set(expected_installs)
    assert len(specs_that_make_would_install) == len(set(specs_that_make_would_install))


def test_depfile_safe_format():
    """Test that depfile.MakefileSpec.safe_format() escapes target names."""

    class SpecLike:
        def format(self, _):
            return "abc@def=ghi"

    spec = depfile.MakefileSpec(SpecLike())
    assert spec.safe_format("{name}") == "abc_def_ghi"
    assert spec.unsafe_format("{name}") == "abc@def=ghi"


def test_depfile_works_with_gitversions(tmpdir, mock_packages, monkeypatch):
    """Git versions may contain = chars, which should be escaped in targets,
    otherwise they're interpreted as makefile variable assignments."""
    monkeypatch.setattr(spack.package_base.PackageBase, "git", "repo.git", raising=False)
    env("create", "test")

    make = Executable("make")
    makefile = str(tmpdir.join("Makefile"))

    # Create an environment with dttop and dtlink1 both at a git version,
    # and generate a depfile
    with ev.read("test"):
        add(f"dttop@{'a' * 40}=1.0 ^dtlink1@{'b' * 40}=1.0")
        concretize()
        env("depfile", "-o", makefile, "--make-disable-jobserver", "--make-prefix=prefix")

    # Do a dry run on the generated depfile
    out = make("-n", "-f", makefile, output=str)

    # Check that all specs are there (without duplicates)
    specs_that_make_would_install = _parse_dry_run_package_installs(out)
    expected_installs = [
        "dtbuild1",
        "dtbuild2",
        "dtbuild3",
        "dtlink1",
        "dtlink2",
        "dtlink3",
        "dtlink4",
        "dtlink5",
        "dtrun1",
        "dtrun2",
        "dtrun3",
        "dttop",
    ]
    assert set(specs_that_make_would_install) == set(expected_installs)
    assert len(specs_that_make_would_install) == len(set(specs_that_make_would_install))


@pytest.mark.parametrize(
    "picked_package,expected_installs",
    [
        (
            "dttop",
            [
                "dtbuild2",
                "dtlink2",
                "dtrun2",
                "dtbuild1",
                "dtlink4",
                "dtlink3",
                "dtlink1",
                "dtlink5",
                "dtbuild3",
                "dtrun3",
                "dtrun1",
                "dttop",
            ],
        ),
        ("dtrun1", ["dtlink5", "dtbuild3", "dtrun3", "dtrun1"]),
    ],
)
def test_depfile_phony_convenience_targets(
    picked_package, expected_installs: set, tmpdir, mock_packages
):
    """Check whether convenience targets "install/%" and "install-deps/%" are created for
    each package if "--make-prefix" is absent."""
    make = Executable("make")
    with fs.working_dir(str(tmpdir)):
        with ev.create_in_dir("."):
            add("dttop")
            concretize()

        with ev.Environment(".") as e:
            picked_spec = e.matching_spec(picked_package)
            env("depfile", "-o", "Makefile", "--make-disable-jobserver")

        # Phony install/* target should install picked package and all its deps
        specs_that_make_would_install = _parse_dry_run_package_installs(
            make("-n", picked_spec.format("install/{name}-{version}-{hash}"), output=str)
        )

        assert set(specs_that_make_would_install) == set(expected_installs)
        assert len(specs_that_make_would_install) == len(set(specs_that_make_would_install))

        # Phony install-deps/* target shouldn't install picked package
        specs_that_make_would_install = _parse_dry_run_package_installs(
            make("-n", picked_spec.format("install-deps/{name}-{version}-{hash}"), output=str)
        )

        assert set(specs_that_make_would_install) == set(expected_installs) - {picked_package}
        assert len(specs_that_make_would_install) == len(set(specs_that_make_would_install))


def test_environment_depfile_out(tmpdir, mock_packages):
    env("create", "test")
    makefile_path = str(tmpdir.join("Makefile"))
    with ev.read("test"):
        add("libdwarf")
        concretize()
    with ev.read("test"):
        env("depfile", "-G", "make", "-o", makefile_path)
        stdout = env("depfile", "-G", "make")
        with open(makefile_path, "r") as f:
            assert stdout == f.read()


def test_spack_package_ids_variable(tmpdir, mock_packages):
    # Integration test for post-install hooks through prefix/SPACK_PACKAGE_IDS
    # variable
    env("create", "test")
    makefile_path = str(tmpdir.join("Makefile"))
    include_path = str(tmpdir.join("include.mk"))

    # Create env and generate depfile in include.mk with prefix example/
    with ev.read("test"):
        add("libdwarf")
        concretize()

    with ev.read("test"):
        env(
            "depfile",
            "-G",
            "make",
            "--make-disable-jobserver",
            "--make-prefix=example",
            "-o",
            include_path,
        )

    # Include in Makefile and create target that depend on SPACK_PACKAGE_IDS
    with open(makefile_path, "w") as f:
        f.write(
            r"""
all: post-install

include include.mk

example/post-install/%: example/install/%
	$(info post-install: $(HASH)) # noqa: W191,E101

post-install: $(addprefix example/post-install/,$(example/SPACK_PACKAGE_IDS))
"""
        )
    make = Executable("make")

    # Do dry run.
    out = make("-n", "-C", str(tmpdir), output=str)

    # post-install: <hash> should've been executed
    with ev.read("test") as test:
        for s in test.all_specs():
            assert "post-install: {}".format(s.dag_hash()) in out


def test_depfile_empty_does_not_error(tmp_path):
    # For empty environments Spack should create a depfile that does nothing
    make = Executable("make")
    makefile = str(tmp_path / "Makefile")

    env("create", "test")
    with ev.read("test"):
        env("depfile", "-o", makefile)

    make("-f", makefile)

    assert make.returncode == 0


def test_unify_when_possible_works_around_conflicts():
    e = ev.create("coconcretization")
    e.unify = "when_possible"

    e.add("mpileaks+opt")
    e.add("mpileaks~opt")
    e.add("mpich")

    e.concretize()

    assert len([x for x in e.all_specs() if x.satisfies("mpileaks")]) == 2
    assert len([x for x in e.all_specs() if x.satisfies("mpileaks+opt")]) == 1
    assert len([x for x in e.all_specs() if x.satisfies("mpileaks~opt")]) == 1
    assert len([x for x in e.all_specs() if x.satisfies("mpich")]) == 1


def test_env_include_packages_url(
    tmpdir, mutable_empty_config, mock_spider_configs, mock_curl_configs
):
    """Test inclusion of a (GitHub) URL."""
    develop_url = "https://github.com/fake/fake/blob/develop/"
    default_packages = develop_url + "etc/fake/defaults/packages.yaml"
    spack_yaml = tmpdir.join("spack.yaml")
    with spack_yaml.open("w") as f:
        f.write("spack:\n  include:\n    - {0}\n".format(default_packages))
    assert os.path.isfile(spack_yaml.strpath)

    with spack.config.override("config:url_fetch_method", "curl"):
        env = ev.Environment(tmpdir.strpath)
        ev.activate(env)
        scopes = env.included_config_scopes()
        assert len(scopes) == 1

        cfg = spack.config.get("packages")
        assert "openmpi" in cfg["all"]["providers"]["mpi"]


def test_relative_view_path_on_command_line_is_made_absolute(tmp_path, config):
    with fs.working_dir(str(tmp_path)):
        env("create", "--with-view", "view", "--dir", "env")
        environment = ev.Environment(os.path.join(".", "env"))
        environment.regenerate_views()
        assert os.path.samefile("view", environment.default_view.root)


def test_environment_created_in_users_location(mutable_mock_env_path, tmp_path):
    """Test that an environment is created in a location based on the config"""
    env_dir = str(mutable_mock_env_path)

    assert str(tmp_path) in env_dir
    assert not os.path.isdir(env_dir)

    dir_name = "user_env"
    env("create", dir_name)
    out = env("list")

    assert dir_name in out
    assert env_dir in ev.root(dir_name)
    assert os.path.isdir(os.path.join(env_dir, dir_name))


def test_environment_created_from_lockfile_has_view(mock_packages, tmpdir):
    """When an env is created from a lockfile, a view should be generated for it"""
    env_a = str(tmpdir.join("a"))
    env_b = str(tmpdir.join("b"))

    # Create an environment and install a package in it
    env("create", "-d", env_a)
    with ev.Environment(env_a):
        add("libelf")
        install("--fake")

    # Create another environment from the lockfile of the first environment
    env("create", "-d", env_b, os.path.join(env_a, "spack.lock"))

    # Make sure the view was created
    with ev.Environment(env_b) as e:
        assert os.path.isdir(e.view_path_default)
