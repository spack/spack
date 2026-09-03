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


def _get_activate_commands(env, view: Optional[str] = None, shell: str = "sh") -> str:
    """Get the commands to activate an environment.

    Args:
        env: the environment to activate
        view: the name of the environment's view
        shell: the shell that the user is running
    Returns:
        A list of commands to activate the environment
    """
    env_mods = spack.environment.shell.activate(env=env, view=view)

    cmds = ""
    cmds += spack.environment.shell.activate_commands(env, view)
    cmds += env_mods.shell_modifications(shell)

    return cmds


def _get_deactivate_commands(env, view: Optional[str] = None, shell: str = "sh") -> str:
    """Get the commands to deactivate an environment.

    Args:
        env: the environment to deactivate
        view: the name of the environment's view
        shell: the shell that the user is running
    Returns:
        A list of commands to deactivate the environment
    """
    env_mods = spack.environment.shell.deactivate(env, view)

    cmds = ""
    cmds += spack.environment.shell.deactivate_commands(shell)
    cmds += env_mods.shell_modifications(shell)

    return cmds


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

    # Script does NOT need update if no lockfile exists
    if lockfile_mtime == 0.0:
        return False

    script_mtime = os.stat(script_path).st_mtime
    return lockfile_mtime >= script_mtime


def _write_env_script(env: "spack.environment.Environment", view: Optional[str] = None, activate: bool = True):
    """Helper method for write_env_(de)activate_script methods"""

    # Ensure .env subdir exists
    env.ensure_env_directory_exists(dot_env=True)

    # Get lockfile modification time
    lockfile_mtime = os.stat(env.lock_path).st_mtime if os.path.isfile(env.lock_path) else 0.0

    if activate:
        script_type = "activate"
        shells = WINDOWS_SHELLS if sys.platform == "win32" else ["sh"]

    else:
        script_type = "deactivate"
        shells = WINDOWS_SHELLS if sys.platform == "win32" else ["sh", "csh", "fish"]


    for shell in shells:
        script_path = path_to_env_script(env, shell, script_type, view)
        if _script_needs_update(lockfile_mtime, script_path):
            if activate:
                cmds = _get_activate_commands(env, view=view, shell=shell)
            else:
                cmds = _get_deactivate_commands(env, view=view, shell=shell)
            uenv.write_shell_script(script_path, cmds, shell)


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

    script_name = (
        f"{view}_{script_type}{extension}" if view else f"noview_{script_type}{extension}"
    )

    script_path = os.path.join(env.path, ".spack-env", script_name)

    return script_path


def regenerate_env_scripts(env):
    """Regenerate the activation and deactivation scripts for an environment.

    Args:
        env: the environment whose scripts we are regenerating
    """
    spack_env_dir = os.path.join(env.path, ".spack-env")
    if os.path.isdir(spack_env_dir):
        # Remove all activation/deactivation scripts to force regeneration
        for filename in os.listdir(spack_env_dir):
            if "_activate" in filename or "_deactivate" in filename:
                script_path = os.path.join(spack_env_dir, filename)
                try:
                    os.remove(script_path)
                except OSError:
                    pass

    if env.views:
        for view_name in env.views.keys():
            write_env_activate_script(env, view_name)
            write_env_deactivate_script(env, view_name)

    write_env_activate_script(env, None)
    write_env_deactivate_script(env, None)


def write_env_activate_script(env: "spack.environment.Environment", view: Optional[str] = None):
    """Generate and write activation scripts for an environment.

    Args:
        env: the environment the activation script is written for
        view: the name of the environment's view
    """
    return _write_env_script(env, view, activate=True)


def write_env_deactivate_script(env, view: Optional[str] = None):
    """Generate and write deactivation scripts for an environment.

    Args:
        env: the environment the deactivation script is written for
        view: the name of the environment's view
    """
    _write_env_script(env, view, activate=False)


def get_shell_unique_env_cmds(shell, prompt: Optional[str] = None) -> str:
    """Returns the prompt and despacktivate commands which are unique to each shell.

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
        return f'source "{env_script_path}"\n'
    elif shell == "bat":
        return f'call "{env_script_path}"\n'
    else:  # sh, pwsh
        return f'. "{env_script_path}"\n'
