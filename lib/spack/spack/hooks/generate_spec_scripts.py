# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from datetime import datetime

import spack.llnl.util.tty as tty
import spack.user_environment as uenv


def path_to_load_shell_script(spec, shell):
    """"Returns the path to the shell script to load the specified spec for the shell.

    Args:
        spec: The spec whose shell script we are returning the path of
        shell: The shell that the user is running on
    """
    extension = f".{shell}" if shell == "bat" or shell == "pwsh" else ""

    return os.path.join(spec.prefix, ".spack", f"load{extension}")


def path_to_unload_shell_script(spec, shell):
    """Returns the path to the shell script to unload the specified spec for the shell.

    Args:
        spec: The spec whose shell script we are returning the path of
        shell: The shell that the user is running
    """
    extension = f".{shell}" if shell == "bat" or shell == "pwsh" else ""

    return os.path.join(spec.prefix, ".spack", f"unload{extension}")


def write_spec_scripts(shell_script_path, mods):
    """Helper function to write spec's shell scripts

    Args:
        shell_script_path: Path to the shell script.
        mods: Modifications to write to the script.
    """

    try:
        with open(shell_script_path, "w", encoding="utf-8") as f:
            f.write(
                f"### Script created by spack (https://github.com/spack/spack) {datetime.now().strftime('%Y-%m-%d')}\n\n"
            )
            f.write(mods)
    except OSError as e:
        tty.error(f"Error writing to {shell_script_path}: {e}")


def post_install(spec, explicit=None):
    """Creates and writes a cached shell script in for all available shells

    Args:
        spec: The spec the requires the shell scripts
        explicit: (Optional) Placeholder for future use or additional functionality.
    """

    if spec.external:
        return

    shells_avail = ["sh"]  # csh & fish have the same script as sh

    if sys.platform == "win32":
        shells_avail.extend(["bat", "pwsh"])

    load_env_mods = uenv.environment_modifications_for_specs(spec)
    unload_env_mod = uenv.environment_modifications_for_specs(spec).reversed()

    for shell in shells_avail:
        load_script_path = path_to_load_shell_script(spec, shell)
        unload_script_path = path_to_unload_shell_script(spec, shell)

        # Write shell script to load
        load_mods = load_env_mods.shell_modifications(shell)
        load_mods += f"_spack_env_prepend {uenv.spack_loaded_hashes_var} {spec.dag_hash()} :"
        write_spec_scripts(load_script_path, load_mods)

        # Write shell script to unload
        unload_mods = unload_env_mod.shell_modifications(shell)
        unload_mods += f"_spack_env_remove_value {uenv.spack_loaded_hashes_var} {spec.dag_hash()} :"
        write_spec_scripts(unload_script_path, unload_mods)
