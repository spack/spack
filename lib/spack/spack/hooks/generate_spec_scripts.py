# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import sys
from typing import Tuple

import spack.bootstrap.config
import spack.repo
import spack.store
import spack.user_environment as uenv
import spack.util.filesystem as fs
import spack.util.tty as tty


def _get_shell_script_path(spec, shell: str, load: bool) -> str:
    """Returns the path to the shell script to load or unload the specified spec for the shell.

    Args:
        spec: The spec whose shell script we are returning the path of
        shell: The shell that the user is running
        load: Whether to return the path to the load or unload script
    """
    if spec.external:
        return ""

    extension = ""
    if shell == "bat":
        extension = ".bat"
    elif shell == "pwsh":
        extension = ".ps1"

    if load:
        return os.path.join(spec.prefix, ".spack", f"load{extension}")
    else:
        return os.path.join(spec.prefix, ".spack", f"unload{extension}")


def path_to_load_shell_script(spec, shell: str) -> str:
    """Returns the path to the shell script to load the specified spec for the shell.

    Args:
        spec: The spec whose shell script we are returning the path of
        shell: The shell that the user is running on
    """
    return _get_shell_script_path(spec, shell, load=True)


def path_to_unload_shell_script(spec, shell: str) -> str:
    """Returns the path to the shell script to unload the specified spec for the shell.

    Args:
        spec: The spec whose shell script we are returning the path of
        shell: The shell that the user is running
    """
    return _get_shell_script_path(spec, shell, load=False)


def write_script(shell_script_path: str, mods: str, shell: str):
    """Helper function to write spec's shell scripts

    Args:
        shell_script_path: Path to the shell script.
        mods: Modifications to write to the script.
        shell: Shell type
    """
    uenv.write_shell_script(shell_script_path, mods, shell)


def make_repo_path(root):
    """Make a RepoPath from the repo subdirectories in an environment.

    Args:
        root: the root of the environment
    """
    if not os.path.isdir(root):
        return None
    repos = (
        spack.repo.from_path(os.path.dirname(p))
        for p in glob.glob(os.path.join(root, "**", "repo.yaml"), recursive=True)
    )
    return spack.repo.RepoPath(*repos) if repos else None


def get_environment_modifications(spec, shell, repo=None) -> Tuple[str, str]:
    """Returns both load and unload environment modifications for the spec.
    Args:
        spec: The spec whose environment modifications we are returning
        shell: The shell that the user is running
        repo: (Optional) A repo to use when calculating environment modifications

    Returns:
        tuple: (load_modifications, unload_modifications)
    """
    load_env_mod = uenv.environment_modifications_for_specs(spec, repo=repo)
    unload_env_mod = load_env_mod.reversed()

    load_env_mod.prepend_path(uenv.spack_loaded_hashes_var, spec.dag_hash())
    load_mods = load_env_mod.shell_modifications(shell)

    unload_env_mod.remove_path(uenv.spack_loaded_hashes_var, spec.dag_hash())
    unload_mods = unload_env_mod.shell_modifications(shell)

    return load_mods, unload_mods


def source_script(script_path: str, shell: str) -> str:
    """Returns the command to source a shell script for the given shell.

    Args:
        script_path: Path to the shell script.
        shell: The shell that the user is running
    """
    if shell in ("csh", "fish"):
        return f'source "{script_path}"\n'
    elif shell == "bat":
        return f'call "{script_path}"\n'
    else:  # sh, pwsh
        return f'. "{script_path}"\n'


def post_install(spec, explicit=None):
    """Creates and writes a cached shell script in for all available shells

    Args:
        spec: The spec the requires the shell scripts
        explicit: (Optional) is the spec explicitly installed by the user
    """

    if spec.external:
        return

    # Skip script generation during bootstrapping
    if spack.bootstrap.config.is_bootstrapping():
        return

    shells_avail = ["sh"]  # csh & fish have the same script as sh

    if sys.platform == "win32":
        shells_avail = ["bat", "pwsh"]

    for shell in shells_avail:
        try:
            load_script_path = path_to_load_shell_script(spec, shell)
            unload_script_path = path_to_unload_shell_script(spec, shell)

            spack_dir = spack.store.STORE.layout.metadata_path(spec)
            fs.mkdirp(spack_dir)

            cached_repo = make_repo_path(spack_dir)

            # Write shell script to load & unload
            load_mods, unload_mods = get_environment_modifications(spec, shell, cached_repo)
            write_script(load_script_path, load_mods, shell)
            write_script(unload_script_path, unload_mods, shell)
        except Exception as e:
            msg = f"Error generating shell scripts for {spec.name} in {shell} shell: {e}"
            tty.warn(msg)
