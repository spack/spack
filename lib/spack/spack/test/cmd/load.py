# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import os
import sys

import pytest

import spack.concretize
import spack.hooks.generate_spec_scripts as spec_script
import spack.user_environment as uenv
from spack.main import SpackCommand

load = SpackCommand("load")
unload = SpackCommand("unload")
install = SpackCommand("install")
location = SpackCommand("location")


def _get_load_cmds(spec, shell):
    load_script_file = spec_script.path_to_load_shell_script(spec, shell)

    with open(load_script_file, "r", encoding="utf-8") as f:
        return f.read()


def test_load_recursive(install_mockery, mock_fetch, mock_archive, mock_packages, working_env):
    def test_load_shell(shell):
        """Test that `spack load` applies prefix inspections of its required runtime deps in
        topo-order"""
        install("--fake", "mpileaks")
        mpileaks_spec = spack.concretize.concretize_one("mpileaks")

        # Ensure our reference variable is clean.
        os.environ["CMAKE_PREFIX_PATH"] = "/hello" + os.pathsep + "/world"

        load(shell, "mpileaks")

        load_cmds = _get_load_cmds(mpileaks_spec, shell[2:])

        def extract_value(output, variable):
            value = []
            for line in output.splitlines():
                if not line:
                    continue

                info = line.split(" ")
                if info[1] == variable:
                    value.insert(0, info[2])
            return value

        # Map a prefix found in CMAKE_PREFIX_PATH back to a package name in mpileaks' DAG.
        prefix_to_pkg = lambda prefix: next(
            s.name for s in mpileaks_spec.traverse() if s.prefix == prefix
        )

        paths_shell = extract_value(load_cmds, "CMAKE_PREFIX_PATH")

        # All but the last two paths are added by spack load; lookup what packages they're from.
        pkgs = [prefix_to_pkg(p) for p in paths_shell]

        # Do we have all the runtime packages?
        assert set(pkgs) == set(
            s.name for s in mpileaks_spec.traverse(deptype=("link", "run"), root=True)
        )

        # Finally, do we list them in topo order?
        for i, pkg in enumerate(pkgs):
            assert {s.name for s in mpileaks_spec[pkg].traverse(direction="parents")}.issubset(
                pkgs[: i + 1]
            )

        # Lastly, do we keep track that mpileaks was loaded?
        assert (
            extract_value(load_cmds, uenv.spack_loaded_hashes_var)[0] == mpileaks_spec.dag_hash()
        )
        return paths_shell

    if sys.platform == "win32":
        params = ["--bat", "--pwsh"]
        test_load_shell(params[0])
        test_load_shell(params[1])
    else:
        params = ["--sh", "--csh"]
        paths_sh = test_load_shell(params[0])
        paths_csh = test_load_shell(params[1])
        assert paths_sh == paths_csh


@pytest.mark.parametrize(
    "shell", (["--bat", "--pwsh"] if sys.platform == "win32" else ["--sh", "--csh", "--fish"])
)
def test_load_includes_run_env(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Tests that environment changes from the package's
    `setup_run_environment` method are added to the user environment in
    addition to the prefix inspections"""
    install("--fake", "mpileaks")
    mpileaks_spec = spack.concretize.concretize_one("mpileaks")

    load(shell, "mpileaks")
    load_cmds = _get_load_cmds(mpileaks_spec, shell)

    assert "_spack_env_set FOOBAR mpileaks" in load_cmds


@pytest.mark.parametrize(
    "shell", (["--bat", "--pwsh"] if sys.platform == "win32" else ["--sh", "--csh", "--fish"])
)
def test_load_first(shell, install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test with and without the --first option"""
    install("--fake", "libelf@0.8.12")
    install("--fake", "libelf@0.8.13")

    # Now there are two versions of libelf, which should cause an error
    out = load(shell, "libelf", fail_on_error=False)
    assert "matches multiple packages" in out
    assert "Use a more specific spec" in out

    # Using --first should avoid the error condition
    load(shell, "--first", "libelf")


def test_load_fails_no_shell(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that spack load prints an error message without a shell."""
    install("--fake", "mpileaks")

    out = load("mpileaks", fail_on_error=False)
    assert "To set up shell support" in out


@pytest.mark.parametrize(
    "shell", (["--bat", "--pwsh"] if sys.platform == "win32" else ["--sh", "--csh", "--fish"])
)
def test_unload(shell, install_mockery, mock_fetch, mock_archive, mock_packages, working_env):
    """Tests that any variables set in the user environment are undone by the
    unload command"""
    install("--fake", "mpileaks")
    mpileaks_spec = spack.concretize.concretize_one("mpileaks")

    # Set so unload has something to do
    os.environ["FOOBAR"] = "mpileaks"
    os.environ[uenv.spack_loaded_hashes_var] = ("%s" + os.pathsep + "%s") % (
        mpileaks_spec.dag_hash(),
        "garbage",
    )

    unload(shell, "mpileaks")

    unload_script_file = spec_script.path_to_unload_shell_script(mpileaks_spec, shell[2:])

    with open(unload_script_file, "r", encoding="utf-8") as f:
        unload_cmds = f.read()

    print(unload_cmds)
    assert "_spack_env_unset FOOBAR" in unload_cmds


def test_unload_fails_no_shell(
    install_mockery, mock_fetch, mock_archive, mock_packages, working_env
):
    """Test that spack unload prints an error message without a shell."""
    install("--fake", "mpileaks")
    mpileaks_spec = spack.concretize.concretize_one("mpileaks")
    os.environ[uenv.spack_loaded_hashes_var] = mpileaks_spec.dag_hash()

    out = unload("mpileaks", fail_on_error=False)
    assert "To set up shell support" in out


@pytest.mark.parametrize(
    "shell", (["--bat", "--pwsh"] if sys.platform == "win32" else ["--sh", "--csh", "--fish"])
)
def test_load_regenerates_deleted_script(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that spack load regenerates the load script if it was deleted and uses the cached repo."""
    install("--fake", "mpileaks")
    mpileaks_spec = spack.concretize.concretize_one("mpileaks")

    load(shell, "mpileaks")

    load_script_file = spec_script.path_to_load_shell_script(mpileaks_spec, shell)
    assert os.path.exists(load_script_file)

    os.remove(load_script_file)
    assert not os.path.exists(load_script_file)

    # Verify cached repo exists
    cache_dir = os.path.join(mpileaks_spec.prefix, ".spack")
    repo_yaml_files = glob.glob(os.path.join(cache_dir, "**", "repo.yaml"), recursive=True)
    assert len(repo_yaml_files) > 0

    load(shell, "mpileaks")
    assert os.path.exists(load_script_file)


@pytest.mark.parametrize(
    "shell", (["--bat", "--pwsh"] if sys.platform == "win32" else ["--sh", "--csh", "--fish"])
)
def test_unload_regenerates_deleted_script(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that spack load regenerates the load script if it was deleted and uses the cached repo."""
    install("--fake", "mpileaks")
    mpileaks_spec = spack.concretize.concretize_one("mpileaks")

    unload(shell, "mpileaks")

    unload_script_file = spec_script.path_to_unload_shell_script(mpileaks_spec, shell)
    assert os.path.exists(unload_script_file)

    os.remove(unload_script_file)
    assert not os.path.exists(unload_script_file)

    # Verify cached repo exists
    cache_dir = os.path.join(mpileaks_spec.prefix, ".spack")
    repo_yaml_files = glob.glob(os.path.join(cache_dir, "**", "repo.yaml"), recursive=True)
    assert len(repo_yaml_files) > 0

    unload(shell, "mpileaks")
    assert os.path.exists(unload_script_file)
