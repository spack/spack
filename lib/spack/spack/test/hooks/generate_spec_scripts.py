# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

import pytest

import spack.concretize
import spack.hooks.generate_spec_scripts as spec_script
import spack.user_environment as uenv
from spack.main import SpackCommand
from spack.spec import Spec

install = SpackCommand("install")
# TODO: Add shells for windows when shell script is written


@pytest.mark.parametrize(
    "shell",
    (["sh", "csh", "fish", "bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"]),
)
def test_paths_to_shell_cached(shell, install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that load & unload shell scripts are written to the right location
    when a spec is installed"""

    spec = Spec("mpileaks")
    spec = spack.concretize.concretize_one(spec.name)

    install("--fake", spec.name)

    extension = f".{shell}" if shell == "bat" or shell == "pwsh" else ""

    for pkg in spec.traverse():
        pkg_load_script = os.path.join(pkg.prefix, ".spack", f"load{extension}")
        path_to_load_script = spec_script.path_to_load_shell_script(pkg, shell)

        assert path_to_load_script == pkg_load_script

        pkg_unload_script = os.path.join(pkg.prefix, ".spack", f"unload{extension}")
        path_to_unload_script = spec_script.path_to_unload_shell_script(pkg, shell)

        assert path_to_unload_script == pkg_unload_script


@pytest.mark.parametrize(
    "shell",
    (["sh", "csh", "fish", "bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"]),
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
    "shell, set_command",
    (
        [
            ("sh", "_spack_env_.* %s %s :"),
            ("csh", "_spack_env_.* %s %s :"),
            ("fish", "_spack_env_.* %s %s :"),
            # ("bat", 'set "%s=%s"'),
            # ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [
            ("sh", "_spack_env_.* %s %s :"),
            ("csh", "_spack_env_.* %s %s :"),
            ("fish", "_spack_env_.* %s %s :"),
        ]
    ),
)
def test_contents_of_shell_scripts(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
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

        assert re.search(
            set_command % (uenv.spack_loaded_hashes_var, pkg.dag_hash()), load_script
        )
        assert re.search(
            set_command % (uenv.spack_loaded_hashes_var, pkg.dag_hash()), unload_script
        )


@pytest.mark.parametrize(
    "shell,set_command",
    (
        [
            ("sh", "_spack_env_prepend %s %s"),
            ("csh", "_spack_env_prepend %s %s"),
            ("fish", "_spack_env_prepend %s %s"),
            # ("bat", 'set "%s=%s"'),
            # ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [
            ("sh", "_spack_env_prepend %s %s"),
            ("csh", "_spack_env_prepend %s %s"),
            ("fish", "_spack_env_prepend %s %s"),
        ]
    ),
)
def test_install_individual_specs_scripts(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
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

    assert re.search(set_command % ("CMAKE_PREFIX_PATH", dyninst_spec.prefix), dyninst_load)
    assert re.search(set_command % ("CMAKE_PREFIX_PATH", mpich_spec.prefix), mpich_load)

    assert mpich_spec.name not in dyninst_load
    assert dyninst_spec.name not in mpich_load


@pytest.mark.parametrize(
    "shell,set_command",
    (
        [
            ("sh", "_spack_env_prepend %s %s"),
            ("csh", "_spack_env_prepend %s %s"),
            ("fish", "_spack_env_prepend %s %s"),
            # ("bat", 'set "%s=%s"'),
            # ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [
            ("sh", "_spack_env_prepend %s %s"),
            ("csh", "_spack_env_prepend %s %s"),
            ("fish", "_spack_env_prepend %s %s"),
        ]
    ),
)
def test_install_multiple_specs_shell_scripts(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Ensure that the each spec environment modifications are written to the apporiate
    shell script and aren't put together when multiple specs are installed at once"""

    dyninst_spec = Spec("dyninst")
    hypre_spec = Spec("hypre")

    dyninst_spec = spack.concretize.concretize_one(dyninst_spec.name)
    hypre_spec = spack.concretize.concretize_one(hypre_spec.name)

    # Install multiple specs
    install("--fake", dyninst_spec.name, hypre_spec.name)

    # no overlap in load shell script
    path_to_dyninst = spec_script.path_to_load_shell_script(dyninst_spec, shell)
    path_to_hypre = spec_script.path_to_load_shell_script(hypre_spec, shell)

    with open(path_to_dyninst, "r", encoding="utf-8") as f:
        dyninst_load = f.read()
    with open(path_to_hypre, "r", encoding="utf-8") as f:
        hypre_load = f.read()

    assert re.search(set_command % ("CMAKE_PREFIX_PATH", dyninst_spec.prefix), dyninst_load)
    assert re.search(set_command % ("CMAKE_PREFIX_PATH", hypre_spec.prefix), hypre_load)

    assert not re.search(set_command % ("CMAKE_PREFIX_PATH", dyninst_spec.prefix), hypre_load)
    assert not re.search(set_command % ("CMAKE_PREFIX_PATH", hypre_spec.prefix), dyninst_load)

    assert hypre_spec.name not in dyninst_load
    assert dyninst_spec.name not in hypre_load


@pytest.mark.parametrize(
    "shell",
    (["sh", "csh", "fish", "bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"]),
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


def test_write_spec_scripts_fails_on_nonexistent_directory(
        install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that write_spec_scripts prints an error message when it fails to write a script
    because the directory doesn't exist"""

    spec = Spec("mpileaks")
    spec = spack.concretize.concretize_one(spec.name)

    install("--fake", spec.name)

    # Provide a path to a non-existent directory
    bad_path = os.path.join(spec.prefix, "nonexistent_dir", "load")

    with pytest.raises(OSError):
        spec_script.write_spec_scripts(bad_path, "some modifications")
