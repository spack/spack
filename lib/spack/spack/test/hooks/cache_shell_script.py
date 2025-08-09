# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

import pytest

import spack.concretize
import spack.hooks.cache_shell_script as shell_script
from spack.main import SpackCommand
from spack.spec import Spec

install = SpackCommand("install")


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

    for pkg in spec.traverse():
        path_to_load_shell = os.path.join(pkg.prefix, ".spack", f"load.{shell}")
        script_path_to_load_shell = shell_script.path_to_load_shell_script(pkg, shell)

        assert path_to_load_shell == script_path_to_load_shell

        path_to_unload_shell = os.path.join(pkg.prefix, ".spack", f"unload.{shell}")
        script_path_to_unload_shell = shell_script.path_to_unload_shell_script(pkg, shell)

        assert path_to_unload_shell == script_path_to_unload_shell


# import util environment's _SHELL_SET_STRINGS??
@pytest.mark.parametrize(
    "shell",
    (["sh", "csh", "fish", "bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"]),
)
def test_install_script_cached(shell, install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that load & unload shell scripts are written when a spec is installed"""

    spec = Spec("mpileaks")
    spec = spack.concretize.concretize_one(spec.name)

    install("--fake", spec.name)

    for pkg in spec.traverse():

        if not pkg.external:
            path_to_load_shell = shell_script.path_to_load_shell_script(pkg, shell)
            path_to_unload_shell = shell_script.path_to_unload_shell_script(pkg, shell)

            assert os.path.isfile(path_to_load_shell)
            assert os.path.isfile(path_to_unload_shell)


# TODO: Reinstate other shells when it's shell script is written
@pytest.mark.parametrize(
    "shell",
    (
        [
            ("sh"),
            # ("csh", "setenv %s %s"),
            # ("fish", "set %s %s"),
            # ("bat", 'set "%s=%s"'),
            # ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else ["sh"]  # , ("csh", "setenv %s %s"), ("fish", "set %s %s")]
    ),
)
def test_contents_of_shell_scripts(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):

    spec = Spec("mpileaks")
    spec = spack.concretize.concretize_one(spec.name)

    install("--fake", spec.name)

    for pkg in spec.traverse():
        if not pkg.external:
            path_to_load_shell = shell_script.path_to_load_shell_script(pkg, shell)
            path_to_unload_shell = shell_script.path_to_unload_shell_script(pkg, shell)

            with open(path_to_load_shell, "r", encoding="utf-8") as f:
                load_script = f.read()

            with open(path_to_unload_shell, "r", encoding="utf-8") as f:
                unload_script = f.read()

            assert f"_spack_env_prepend SPACK_LOADED_HASHES {pkg.dag_hash()}" in load_script
            assert f"_spack_env_remove_value SPACK_LOADED_HASHES {pkg.dag_hash()}" in unload_script


# TODO: Reinstate other shells when it's shell script is written
@pytest.mark.parametrize(
    "shell,set_command",
    (
        [
            ("sh", "_spack_env_.* %s %s :"),
            # ("csh", "setenv %s %s"),
            # ("fish", "set %s %s"),
            # ("bat", 'set "%s=%s"'),
            # ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [("sh", "_spack_env_.* %s %s :")]  # , ("csh", "setenv %s %s"), ("fish", "set %s %s")]
    ),
)
def test_install_individual_specs_shell_scripts(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
):  # TODO: get better name
    """Ensure that the each spec environment modifications are written to the apporiate
    shell script and aren't put together"""

    dyninst_spec = Spec("dyninst")
    mpich_spec = Spec("mpich")

    dyninst_spec = spack.concretize.concretize_one(dyninst_spec.name)
    mpich_spec = spack.concretize.concretize_one(mpich_spec.name)

    # Install specs individually
    install("--fake", dyninst_spec.name)
    install("--fake", mpich_spec.name)

    # no overlap in load shell script
    path_to_dyninst = shell_script.path_to_load_shell_script(dyninst_spec, shell)
    path_to_mpich = shell_script.path_to_load_shell_script(mpich_spec, shell)

    with open(path_to_dyninst, "r", encoding="utf-8") as f:
        dyninst_load = f.read()

    assert re.search(set_command % ("CMAKE_PREFIX_PATH", dyninst_spec.prefix), dyninst_load)

    with open(path_to_mpich, "r", encoding="utf-8") as f:
        mpich_load = f.read()

    assert re.search(set_command % ("CMAKE_PREFIX_PATH", mpich_spec.prefix), mpich_load)

    assert mpich_spec.name not in dyninst_load
    assert dyninst_spec.name not in mpich_load


# TODO: Reinstate other shells when it's shell script is written
@pytest.mark.parametrize(
    "shell,set_command",
    (
        [
            ("sh", "_spack_env_.* %s %s :"),
            # ("csh", "setenv %s %s"),
            # ("fish", "set %s %s"),
            # ("bat", 'set "%s=%s"'),
            # ("pwsh", "$Env %s %s"),
        ]
        if sys.platform == "win32"
        else [("sh", "_spack_env_.* %s %s :")]  # , ("csh", "setenv %s %s"), ("fish", "set %s %s")]
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
    path_to_dyninst = shell_script.path_to_load_shell_script(dyninst_spec, shell)
    path_to_hypre = shell_script.path_to_load_shell_script(hypre_spec, shell)

    with open(path_to_dyninst, "r", encoding="utf-8") as f:
        dyninst_load = f.read()

    assert re.search(set_command % ("CMAKE_PREFIX_PATH", dyninst_spec.prefix), dyninst_load)

    with open(path_to_hypre, "r", encoding="utf-8") as f:
        hypre_load = f.read()

    assert re.search(set_command % ("CMAKE_PREFIX_PATH", hypre_spec.prefix), hypre_load)

    assert hypre_spec.name not in dyninst_load
    assert dyninst_spec.name not in hypre_load
