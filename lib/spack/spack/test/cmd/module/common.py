# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.config
import spack.main
import spack.repo
import spack.store

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
def test_remove_and_add(database, module_type, modulefile_filenames):
    """Tests adding and removing a tcl module file."""

    if module_type == "lmod":
        # TODO: Testing this with lmod requires mocking
        # TODO: the core compilers
        return

    rm_cli_args = ["rm", "-y", "mpileaks"]
    module_files = modulefile_filenames(module_type, "mpileaks")
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
