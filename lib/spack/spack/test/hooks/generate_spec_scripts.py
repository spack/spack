# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

import spack.concretize
import spack.hooks.generate_spec_scripts as spec_script
import spack.user_environment as uenv
from spack.main import SpackCommand
from spack.spec import Spec

install = SpackCommand("install")


def _get_shell_cmd_invocation(cmd, var, shell):
    if "bat" in shell:
        return f'%{cmd}% "{var}"'
    elif "pwsh" in shell:
        return f"{cmd} '{var}'"
    return f"{cmd} {var}"


def test_paths_to_spec_scripts(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that load & unload shell scripts are written to the right location
    when a spec is installed"""

    spec = spack.concretize.concretize_one("mpileaks")

    install("--fake", spec.name)

    shell_extensions = {"sh": ""}  # csh and fish have the same scripts as sh
    if sys.platform == "win32":
        shell_extensions = {"bat": ".bat", "pwsh": ".ps1"}

    for shell, extension in shell_extensions.items():
        for pkg in spec.traverse():
            if pkg.external:
                continue

            expected_load_path = os.path.join(pkg.prefix, ".spack", f"load{extension}")
            path_to_load_script = spec_script.path_to_load_shell_script(pkg, shell)

            assert path_to_load_script == expected_load_path

            expected_unload_path = os.path.join(pkg.prefix, ".spack", f"unload{extension}")
            path_to_unload_script = spec_script.path_to_unload_shell_script(pkg, shell)

            assert path_to_unload_script == expected_unload_path


@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_shell_scripts_modify_loaded_hashes(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that the load & unload shell scripts contain the correct environment
    modifications for the spec"""

    spec = spack.concretize.concretize_one("mpileaks")

    install("--fake", spec.name)

    for pkg in spec.traverse():
        if pkg.external:
            continue

        path_to_load_shell = spec_script.path_to_load_shell_script(pkg, shell)
        path_to_unload_shell = spec_script.path_to_unload_shell_script(pkg, shell)

        with open(path_to_load_shell, "r", encoding="utf-8") as f:
            load_script = f.read()
        with open(path_to_unload_shell, "r", encoding="utf-8") as f:
            unload_script = f.read()

        separator = os.pathsep
        if shell == "bat":
            separator = f'"{os.pathsep}"'
        elif shell == "pwsh":
            separator = f"'{os.pathsep}'"

        prepend_var = _get_shell_cmd_invocation(
            "_spack_env_prepend", uenv.spack_loaded_hashes_var, shell
        )
        assert f"{prepend_var} {pkg.dag_hash()} {separator}" in load_script.splitlines()

        remove_var = _get_shell_cmd_invocation(
            "_spack_env_remove_value", uenv.spack_loaded_hashes_var, shell
        )
        assert f"{remove_var} {pkg.dag_hash()} {separator}" in unload_script.splitlines()


@pytest.mark.parametrize("install_together", (True, False))
@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_install_multiple_specs_shell_scripts(
    install_together, shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Ensure that the each spec environment modifications are written to the apporiate
    shell script and aren't put together when multiple specs are installed at once"""

    dyninst_spec = Spec("dyninst")
    hypre_spec = Spec("hypre")

    dyninst_spec = spack.concretize.concretize_one(dyninst_spec.name)
    hypre_spec = spack.concretize.concretize_one(hypre_spec.name)

    # Install multiple specs
    if install_together:
        install("--fake", dyninst_spec.name, hypre_spec.name)
    else:
        install("--fake", dyninst_spec.name)
        install("--fake", hypre_spec.name)

    # No overlap in load shell script
    path_to_dyninst = spec_script.path_to_load_shell_script(dyninst_spec, shell)
    path_to_hypre = spec_script.path_to_load_shell_script(hypre_spec, shell)

    with open(path_to_dyninst, "r", encoding="utf-8") as f:
        dyninst_load = f.read()
    with open(path_to_hypre, "r", encoding="utf-8") as f:
        hypre_load = f.read()

    separator = os.pathsep
    if shell == "bat":
        separator = f'"{os.pathsep}"'
    elif shell == "pwsh":
        separator = f"'{os.pathsep}'"

    assert (
        f"{_get_shell_cmd_invocation('_spack_env_prepend', 'CMAKE_PREFIX_PATH', shell)}"
        f" {dyninst_spec.prefix} {separator}" in dyninst_load
    )
    assert (
        f"{_get_shell_cmd_invocation('_spack_env_prepend', 'CMAKE_PREFIX_PATH', shell)}"
        f" {hypre_spec.prefix} {separator}" in hypre_load
    )

    assert (
        f"{_get_shell_cmd_invocation('_spack_env_prepend', 'CMAKE_PREFIX_PATH', shell)}"
        f" {dyninst_spec.prefix} {separator}" not in hypre_load
    )
    assert (
        f"{_get_shell_cmd_invocation('_spack_env_prepend', 'CMAKE_PREFIX_PATH', shell)}"
        f" {hypre_spec.prefix} {separator}" not in dyninst_load
    )

    assert hypre_spec.name not in dyninst_load
    assert dyninst_spec.name not in hypre_load


@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_no_scripts_for_external_spec_with_deps(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that no shell scripts are written for external specs even if they have dependencies"""

    spec = spack.concretize.concretize_one("externaltool")

    install("externaltool")

    for pkg in spec.traverse():
        path_to_load_script = spec_script.path_to_load_shell_script(pkg, shell)
        path_to_unload_script = spec_script.path_to_unload_shell_script(pkg, shell)

        assert not os.path.isfile(path_to_load_script)
        assert not os.path.isfile(path_to_unload_script)


def test_generate_script_creates_directory(
    install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that generate_script creates the directory if it doesn't exist"""

    spec = spack.concretize.concretize_one("mpileaks")

    install("--fake", spec.name)

    # Provide a path to a non-existent directory
    nonexistent_dir = os.path.join(spec.prefix, "nonexistent_dir")
    script_path = os.path.join(nonexistent_dir, "load")

    # Directory should not exist initially
    assert not os.path.exists(nonexistent_dir)

    # generate_script should create the directory
    spec_script.write_script(script_path, "Test script content", "###")

    # Now the directory and file should exist
    assert os.path.exists(nonexistent_dir)
    assert os.path.isfile(script_path)
