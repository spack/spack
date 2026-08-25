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


def test_paths_to_spec_scripts(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that load & unload shell scripts are written to the right location
    when a spec is installed"""

    spec = Spec("mpileaks")
    spec = spack.concretize.concretize_one(spec.name)

    install("--fake", spec.name)

    shells_avail = ["sh"]  # csh and fish have the same scripts as sh

    if sys.platform == "win32":
        shells_avail = ["bat", "pwsh"]
    for shell in shells_avail:
        extension = ""
        if shell == "bat":
            extension = ".bat"
        elif shell == "pwsh":
            extension = ".ps1"

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
def test_load_unload_scripts_exist(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that load & unload shell scripts are written when a spec is installed"""

    spec = Spec("mpileaks")
    spec = spack.concretize.concretize_one(spec.name)

    install("--fake", spec.name)

    for pkg in spec.traverse():
        if not pkg.external:
            path_to_load_shell = spec_script.path_to_load_shell_script(pkg, shell)
            path_to_unload_shell = spec_script.path_to_unload_shell_script(pkg, shell)

            assert os.path.isfile(path_to_load_shell)
            assert os.path.isfile(path_to_unload_shell)


@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_contents_of_shell_scripts(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that the load & unload shell scripts contain the correct environment
    modifications for the spec"""

    spec = Spec("mpileaks")
    spec = spack.concretize.concretize_one(spec.name)

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

        separator = os.pathsep if shell != "bat" else f'"{os.pathsep}"'

        assert (
            f"_spack_env_prepend {uenv.spack_loaded_hashes_var} {pkg.dag_hash()} {separator}"
            in load_script.splitlines()
        )

        assert (
            f"_spack_env_remove_value {uenv.spack_loaded_hashes_var} "
            f"{pkg.dag_hash()} {separator}" in unload_script.splitlines()
        )


@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_install_individual_specs_scripts(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Ensure that the each spec's environment modifications are written to the apporiate
    load/unload script and aren't put together when multiple specs are installed individually"""

    dyninst_spec = Spec("dyninst")
    mpich_spec = Spec("mpich")

    dyninst_spec = spack.concretize.concretize_one(dyninst_spec.name)
    mpich_spec = spack.concretize.concretize_one(mpich_spec.name)

    # Install specs individually
    install("--fake", dyninst_spec.name)
    install("--fake", mpich_spec.name)

    # no overlap in load shell script
    path_to_dyninst = spec_script.path_to_load_shell_script(dyninst_spec, shell)
    path_to_mpich = spec_script.path_to_load_shell_script(mpich_spec, shell)

    with open(path_to_dyninst, "r", encoding="utf-8") as f:
        dyninst_load = f.read()
    with open(path_to_mpich, "r", encoding="utf-8") as f:
        mpich_load = f.read()

    separator = os.pathsep if shell != "bat" else f'"{os.pathsep}"'

    assert (
        f"_spack_env_prepend CMAKE_PREFIX_PATH {dyninst_spec.prefix} {separator}" in dyninst_load
    )
    assert f"_spack_env_prepend CMAKE_PREFIX_PATH {mpich_spec.prefix} {separator}" in mpich_load

    assert mpich_spec.name not in dyninst_load
    assert dyninst_spec.name not in mpich_load


@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_install_multiple_specs_shell_scripts(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Ensure that the each spec environment modifications are written to the apporiate
    shell script and aren't put together when multiple specs are installed at once"""

    dyninst_spec = Spec("dyninst")
    hypre_spec = Spec("hypre")

    dyninst_spec = spack.concretize.concretize_one(dyninst_spec.name)
    hypre_spec = spack.concretize.concretize_one(hypre_spec.name)

    # Install multiple specs
    install("--fake", dyninst_spec.name, hypre_spec.name)

    # No overlap in load shell script
    path_to_dyninst = spec_script.path_to_load_shell_script(dyninst_spec, shell)
    path_to_hypre = spec_script.path_to_load_shell_script(hypre_spec, shell)

    with open(path_to_dyninst, "r", encoding="utf-8") as f:
        dyninst_load = f.read()
    with open(path_to_hypre, "r", encoding="utf-8") as f:
        hypre_load = f.read()

    separator = os.pathsep if shell != "bat" else f'"{os.pathsep}"'

    assert (
        f"_spack_env_prepend CMAKE_PREFIX_PATH {dyninst_spec.prefix} {separator}" in dyninst_load
    )
    assert f"_spack_env_prepend CMAKE_PREFIX_PATH {hypre_spec.prefix} {separator}" in hypre_load

    assert (
        f"_spack_env_prepend CMAKE_PREFIX_PATH {dyninst_spec.prefix} {separator}" not in hypre_load
    )
    assert (
        f"_spack_env_prepend CMAKE_PREFIX_PATH {hypre_spec.prefix} {separator}" not in dyninst_load
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

    spec = Spec("mpileaks")
    spec = spack.concretize.concretize_one(spec.name)

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
