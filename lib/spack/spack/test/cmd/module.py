# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import pytest

import spack.concretize
import spack.config
import spack.main
import spack.modules
import spack.modules.cache
import spack.modules.lmod
import spack.repo
import spack.store
import spack.util.module_cmd
from spack.config import Configuration
from spack.old_installer import PackageInstaller

module = spack.main.SpackCommand("module")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


#: make sure module files are generated for all the tests here
@pytest.fixture(scope="module", autouse=True)
def ensure_module_files_are_there(mock_packages_repo, mock_store, mock_configuration_scopes):
    """Generate module files for module tests."""
    module = spack.main.SpackCommand("module")
    with spack.store.use_store(str(mock_store)):
        with spack.config.use_configuration(*mock_configuration_scopes):
            with spack.repo.use_repositories(mock_packages_repo):
                module("tcl", "refresh", "-y")


def _module_files(module_type, *specs):
    specs = [spack.concretize.concretize_one(x) for x in specs]
    writer_cls = spack.modules.module_types[module_type]
    return [writer_cls.from_spec(spec, "default").layout.filename for spec in specs]


@pytest.fixture(
    params=[
        ["rm", "doesnotexist"],  # Try to remove a non existing module
        ["find", "mpileaks"],  # Try to find a module with multiple matches
        ["find", "doesnotexist"],  # Try to find a module with no matches
        ["find", "--unknown_args"],  # Try to give an unknown argument
    ]
)
def failure_args(request):
    """A list of arguments that will cause a failure"""
    return request.param


@pytest.fixture(params=["tcl", "lmod"])
def module_type(request):
    return request.param


# TODO : test the --delete-tree option
# TODO : this requires having a separate directory for test modules
# TODO : add tests for loads and find to check the prompt format


@pytest.mark.db
def test_exit_with_failure(database, module_type, failure_args):
    with pytest.raises(spack.main.SpackCommandError):
        module(module_type, *failure_args)


@pytest.mark.db
def test_remove_and_add(database, module_type):
    """Tests adding and removing a tcl module file."""

    if module_type == "lmod":
        # TODO: Testing this with lmod requires mocking
        # TODO: the core compilers
        return

    rm_cli_args = ["rm", "-y", "mpileaks"]
    module_files = _module_files(module_type, "mpileaks")
    for item in module_files:
        assert os.path.exists(item)

    module(module_type, *rm_cli_args)
    for item in module_files:
        assert not os.path.exists(item)

    module(module_type, "refresh", "-y", "mpileaks")
    for item in module_files:
        assert os.path.exists(item)


@pytest.mark.db
@pytest.mark.parametrize("cli_args", [["libelf"], ["--full-path", "libelf"]])
def test_find(database, cli_args, module_type):
    if module_type == "lmod":
        # TODO: Testing this with lmod requires mocking
        # TODO: the core compilers
        return

    module(module_type, *(["find"] + cli_args))


@pytest.mark.db
@pytest.mark.usefixtures("database")
@pytest.mark.regression("2215")
def test_find_fails_on_multiple_matches():
    # As we installed multiple versions of mpileaks, the command will
    # fail because of multiple matches
    out = module("tcl", "find", "mpileaks", fail_on_error=False)
    assert module.returncode == 1
    assert "matches multiple packages" in out

    # Passing multiple packages from the command line also results in the
    # same failure
    out = module("tcl", "find", "mpileaks ^mpich", "libelf", fail_on_error=False)
    assert module.returncode == 1
    assert "matches multiple packages" in out


@pytest.mark.db
@pytest.mark.usefixtures("database")
@pytest.mark.regression("2570")
def test_find_fails_on_non_existing_packages():
    # Another way the command might fail is if the package does not exist
    out = module("tcl", "find", "doesnotexist", fail_on_error=False)
    assert module.returncode == 1
    assert "matches no package" in out


@pytest.mark.db
@pytest.mark.usefixtures("database")
def test_find_recursive():
    # If we call find without options it should return only one module
    out = module("tcl", "find", "mpileaks ^zmpi")
    assert len(out.split()) == 1

    # If instead we call it with the recursive option the length should
    # be greater
    out = module("tcl", "find", "-r", "mpileaks ^zmpi")
    assert len(out.split()) > 1


@pytest.mark.db
def test_find_recursive_excluded(mutable_database, module_configuration):
    module_configuration("exclude")

    module("lmod", "refresh", "-y", "--delete-tree")
    module("lmod", "find", "-r", "mpileaks ^mpich")


@pytest.mark.db
def test_loads_recursive_excluded(mutable_database, module_configuration):
    module_configuration("exclude")

    module("lmod", "refresh", "-y", "--delete-tree")
    output = module("lmod", "loads", "-r", "mpileaks ^mpich")
    lines = output.split("\n")

    assert any(re.match(r"[^#]*module load.*mpileaks", ln) for ln in lines)
    assert not any(re.match(r"[^#]module load.*callpath", ln) for ln in lines)
    assert any(re.match(r"## excluded or missing.*callpath", ln) for ln in lines)

    # TODO: currently there is no way to separate stdout and stderr when
    # invoking a SpackCommand. Supporting this requires refactoring
    # SpackCommand, or log_output, or both.
    # start_of_warning = spack.cmd.modules._missing_modules_warning[:10]
    # assert start_of_warning not in output


# Needed to make the 'module_configuration' fixture below work
writer_cls = spack.modules.lmod.LmodModulefileWriter


@pytest.mark.db
def test_setdefault_command(mutable_database, mutable_config: Configuration):
    data = {
        "default": {
            "enable": ["lmod"],
            "lmod": {"core_compilers": ["clang@3.3"], "hierarchy": ["mpi"]},
        }
    }
    mutable_config.set("modules", data)
    # Install two different versions of pkg-a
    other_spec, preferred = "pkg-a@1.0", "pkg-a@2.0"

    specs = [
        spack.concretize.concretize_one(other_spec),
        spack.concretize.concretize_one(preferred),
    ]
    PackageInstaller([s.package for s in specs], explicit=True, fake=True).install()

    writers = {
        preferred: writer_cls.from_spec(specs[1], "default"),
        other_spec: writer_cls.from_spec(specs[0], "default"),
    }

    # Create two module files for the same software
    module("lmod", "refresh", "-y", "--delete-tree", preferred, other_spec)

    # Assert initial directory state: no link and all module files present
    link_name = os.path.join(os.path.dirname(writers[preferred].layout.filename), "default")
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert not os.path.exists(link_name)

    # Set the default to be the other spec
    module("lmod", "setdefault", other_spec)

    # Check that a link named 'default' exists, and points to the right file
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert os.path.exists(link_name) and os.path.islink(link_name)
    assert os.path.realpath(link_name) == os.path.realpath(writers[other_spec].layout.filename)

    # Reset the default to be the preferred spec
    module("lmod", "setdefault", preferred)

    # Check that a link named 'default' exists, and points to the right file
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert os.path.exists(link_name) and os.path.islink(link_name)
    assert os.path.realpath(link_name) == os.path.realpath(writers[preferred].layout.filename)


@pytest.fixture()
def module_cmd_calls(monkeypatch):
    """Intercepts module command runs, and returns the list of their arguments."""
    monkeypatch.setattr(spack.modules.cache, "_pending_dirs", set())
    calls = []

    def fake_module(*args, environb=None, **kwargs):
        calls.append((args, environb))
        return ""

    monkeypatch.setattr(spack.util.module_cmd, "module", fake_module)
    return calls


def _enable_update_cache(mutable_config):
    mutable_config.set("modules", {"default": {"enable": ["tcl"], "tcl": {"update_cache": True}}})


@pytest.mark.db
def test_tcl_refresh_updates_module_cache(mutable_database, mutable_config, module_cmd_calls):
    """Tests that a refresh ends with a single cachebuild of the changed directories,
    when 'update_cache' is set."""
    _enable_update_cache(mutable_config)

    module("tcl", "refresh", "-y", "mpileaks")

    assert len(module_cmd_calls) == 2
    assert module_cmd_calls[0][0] == ("cacheclear",)
    args, _ = module_cmd_calls[1]
    assert args[0] == "cachebuild"
    assert len(args) > 1 and all(os.path.isdir(d) for d in args[1:])

    # Module file removal also triggers a cache update
    module_cmd_calls.clear()
    module("tcl", "rm", "-y", "mpileaks")

    assert len(module_cmd_calls) == 2
    assert module_cmd_calls[0][0] == ("cacheclear",)
    assert module_cmd_calls[1][0][0] == "cachebuild"


@pytest.mark.db
def test_tcl_refresh_no_update_cache_by_default(mutable_database, module_cmd_calls):
    """Tests that no cache update happens when 'update_cache' is not set."""
    module("tcl", "refresh", "-y", "mpileaks")
    assert not module_cmd_calls


@pytest.mark.db
def test_tcl_setdefault_updates_module_cache(
    mutable_database, mutable_config: Configuration, module_cmd_calls
):
    """Tests that setting the default module file triggers a cache update, when
    'update_cache' is set."""
    _enable_update_cache(mutable_config)
    other_spec, preferred = "pkg-a@1.0", "pkg-a@2.0"
    specs = [
        spack.concretize.concretize_one(other_spec),
        spack.concretize.concretize_one(preferred),
    ]
    PackageInstaller([s.package for s in specs], explicit=True, fake=True).install()
    module("tcl", "refresh", "-y", preferred, other_spec)

    module_cmd_calls.clear()
    module("tcl", "setdefault", other_spec)

    assert len(module_cmd_calls) == 2
    assert module_cmd_calls[0][0] == ("cacheclear",)
    assert module_cmd_calls[1][0][0] == "cachebuild"


@pytest.mark.db
def test_tcl_cachebuild_command(mutable_database, mutable_config: Configuration, module_cmd_calls):
    """Tests that 'spack module tcl cachebuild' builds the cache of every modulepath
    directory managed by spack, even when 'update_cache' is not set."""
    # Exclude one package from module file generation to also verify that excluded
    # specs do not contribute modulepath directories
    mutable_config.set(
        "modules", {"default": {"enable": ["tcl"], "tcl": {"exclude": ["libdwarf"]}}}
    )
    module("tcl", "refresh", "-y")
    module_cmd_calls.clear()

    module("tcl", "cachebuild")

    assert len(module_cmd_calls) == 1
    args, _ = module_cmd_calls[0]
    assert args[0] == "cachebuild"
    assert len(args) > 1 and all(os.path.isdir(d) for d in args[1:])


@pytest.mark.db
def test_tcl_cacheclear_command(database, module_cmd_calls, monkeypatch):
    """Tests that 'spack module tcl cacheclear' runs with MODULEPATH set to the
    modulepath directories managed by spack, ignoring the inherited value."""
    monkeypatch.setenv("MODULEPATH", "/some/user/modulepath")
    module("tcl", "refresh", "-y")
    module_cmd_calls.clear()

    module("tcl", "cacheclear")

    assert len(module_cmd_calls) == 1
    args, environb = module_cmd_calls[0]
    assert args == ("cacheclear",)
    modulepath = os.fsdecode(environb[b"MODULEPATH"])
    assert modulepath and all(os.path.isdir(d) for d in modulepath.split(os.pathsep))
    assert "/some/user/modulepath" not in modulepath


@pytest.mark.db
def test_cache_subcommands_without_modulepath_directory(database, module_cmd_calls, monkeypatch):
    """Tests that cache sub-commands run no module command when no modulepath
    directory holds module files of known installed packages."""
    monkeypatch.setattr(spack.repo.PATH, "exists", lambda name: False)

    out = module("tcl", "cachebuild")
    assert "No modulepath directory found" in out

    out = module("tcl", "cacheclear")
    assert "No modulepath directory found" in out

    assert not module_cmd_calls


@pytest.mark.db
def test_cache_subcommands_are_tcl_only(database):
    """Tests that cache sub-commands are not available for lmod."""
    for subcommand in ("cachebuild", "cacheclear"):
        with pytest.raises(spack.main.SpackCommandError):
            module("lmod", subcommand)
