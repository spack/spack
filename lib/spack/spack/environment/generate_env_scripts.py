# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from typing import Optional

import spack.environment.shell
import spack.user_environment as uenv

# Shell configuration
UNIX_SHELLS = ["sh", "csh", "fish"]
WINDOWS_SHELLS = ["bat", "pwsh"]


def path_to_env_script(env, shell: str, script_type: str, view: Optional[str] = None) -> str:
    """Returns path to the shell script for activating or deactivating an environment.

    Args:
        env: the environment whose shell script we are returning the path of
        shell: the shell that the user is running
        script_type: Either 'activate' or 'deactivate'
        view: the name of the environment's view
    """
    if script_type == "activate":
        activate_extensions = {"sh": "", "csh": "", "fish": "", "bat": ".bat", "pwsh": ".ps1"}
        extension = activate_extensions.get(shell, "")
    else:
        extension = ".ps1" if shell == "pwsh" else f".{shell}"

    script_name = f"{view}_{script_type}{extension}" if view else f"{script_type}{extension}"
    return os.path.join(env.path, ".spack-env", script_name)


def _script_needs_update(lockfile_mtime: float, script_path: str) -> bool:
    """Check if a script needs to be regenerated.

    Args:
        lockfile_mtime: The modification time of the environment's lockfile
        script_path: Path to the cached activation/deactivation script

    Returns:
        True if the script doesn't exist or is older than the lockfile
    """
    if not os.path.isfile(script_path):
        return True

    if lockfile_mtime == 0.0:
        return True

    script_mtime = os.stat(script_path).st_mtime
    return lockfile_mtime > script_mtime


def write_env_activate_script(env: "spack.environment.Environment", view: Optional[str] = None):
    """Generate and write activation scripts for an environment.

    Args:
        env: the environment the activation script is written for
        view: the name of the environment's view
    """
    # Ensure .env subdir exists
    env.ensure_env_directory_exists(dot_env=True)

    # Get lockfile modification time
    lockfile_mtime = os.stat(env.lock_path).st_mtime if os.path.isfile(env.lock_path) else 0.0

    # Generate script for sh only on Unix (csh & fish source the same script)
    shells = WINDOWS_SHELLS if sys.platform == "win32" else UNIX_SHELLS
    if sys.platform != "win32":
        shells = ["sh"]

    for shell in shells:
        print(f"view: {view}")
        activate_script_path = path_to_env_script(env, shell, "activate", view)
        print(f"Writing activation script for {shell} at {activate_script_path}")

        # Update the script only if needed
        if _script_needs_update(lockfile_mtime, activate_script_path):
            env_mods = spack.environment.shell.activate(env=env, view=view)

            cmds = spack.environment.shell.activate_commands(env, view)
            cmds += env_mods.shell_modifications(shell)

            uenv.write_shell_script(activate_script_path, cmds, shell)


def write_env_deactivate_script(env, view: Optional[str] = None):
    """Generate and write deactivation scripts for an environment.

    Args:
        env: the environment the deactivation script is written for
        view: the name of the environment's view
    """
    # Ensure .env subdir exists
    env.ensure_env_directory_exists(dot_env=True)

    # Get lockfile modification time
    lockfile_mtime = os.stat(env.lock_path).st_mtime if os.path.isfile(env.lock_path) else 0.0

    shells = WINDOWS_SHELLS if sys.platform == "win32" else UNIX_SHELLS

    for shell in shells:
        deactivate_script_path = path_to_env_script(env, shell, "deactivate", view)

        # Update the script only if needed
        if _script_needs_update(lockfile_mtime, deactivate_script_path):
            env_mods = spack.environment.shell.deactivate(env, view)

            cmds = spack.environment.shell.deactivate_commands(shell)
            cmds += env_mods.shell_modifications(shell)

            uenv.write_shell_script(deactivate_script_path, cmds, shell)


def get_shell_unique_env_cmds(shell, prompt: Optional[str] = None) -> str:
    """Returns the prompt, view, and despacktivate commands which are unique to each shell.

    Args:
        shell: the shell that the user is running
        prompt: name of user's prompt
    """
    despactivate_cmd = spack.environment.shell.despacktivate_cmds(shell)
    prompt_cmds = spack.environment.shell.activate_prompt_cmds(shell, prompt)

    return despactivate_cmd + prompt_cmds


def source_env_script(env_script_path, shell: str) -> str:
    """Returns the command to source a shell script for the given shell.

    Args:
        script_path: Path to the shell script.
        shell: The shell that the user is running
    """
    if shell in ("csh", "fish"):
        return f"source {env_script_path}\n"
    elif shell == "bat":
        return f"call {env_script_path}\n"
    else:  # sh, pwsh
        return f". {env_script_path}\n"
