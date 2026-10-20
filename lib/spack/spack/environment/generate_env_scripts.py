# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from typing import Optional, Tuple

import spack.environment.shell
import spack.user_environment as uenv


def get_activate_commands(
    env, view: Optional[str] = None, shell: str = "sh", use_cache: bool = True
) -> Tuple[str, str]:
    """Get the commands to activate an environment.

    Args:
        env: The environment to activate
        view: The name of the environment's view (e.g., "default")
        shell: The shell that the user is running (sh, csh, fish, bat, pwsh)
        use_cache: Whether to use cached helper functions (_spack_env_set, etc.)
            or plain shell commands (export, setenv, etc.)

    Returns:
        A tuple of (prefix_cmds, cmds) where:
            - prefix_cmds: Shell commands for prefix inspections
            - cmds: Shell commands for setting SPACK_ENV, SPACK_ENV_VIEW, and spec modifications
    """
    with env.manifest.use_config():
        prefix_mods, env_mods = spack.environment.shell.activate(env=env, view=view)

    cmds = ""
    prefix_cmds = ""

    cmds += spack.environment.shell.activate_commands(env, shell, view)
    cmds += env_mods.shell_modifications(shell, cache=use_cache)

    if prefix_mods:
        prefix_cmds += prefix_mods.shell_modifications(shell, cache=use_cache)

    return prefix_cmds, cmds


def get_deactivate_commands(
    env, view: Optional[str] = None, shell: str = "sh", use_cache: bool = True
) -> Tuple[str, str]:
    """Get the commands to deactivate an environment.

    Args:
        env: The environment to deactivate
        view: The name of the environment's view (e.g., "default")
        shell: The shell that the user is running (sh, csh, fish, bat, pwsh)
        use_cache: Whether to use cached helper functions (_spack_env_unset, etc.)
            or plain shell commands (unset, unsetenv, etc.)

    Returns:
        A tuple of (prefix_cmds, cmds) where:
            - prefix_cmds: Shell commands to reverse prefix inspections
            - cmds: Shell commands to unset SPACK_ENV, SPACK_ENV_VIEW, and reverse spec mods
    """
    prefix_mods, env_mods = spack.environment.shell.deactivate(env, view)

    cmds = ""
    prefix_cmds = ""

    cmds += spack.environment.shell.deactivate_commands(shell)
    cmds += env_mods.shell_modifications(shell, cache=use_cache)

    if prefix_mods:
        prefix_cmds += prefix_mods.shell_modifications(shell, cache=use_cache)

    return prefix_cmds, cmds


def _script_matches_env(env, script_path: str, view: Optional[str] = None) -> bool:
    """Check if a script matches the environment.

    Args:
        env: the environment to check against
        script_path: path to the cached activation/deactivation script
        view: the name of the environment's view
    Returns:
        True if the script matches the environment, False otherwise
    """
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

    if env.path not in script_content:
        return False

    if view and env.views[view].root not in script_content:
        return False

    return True


def _script_needs_update(yaml_mtime: float, lockfile_mtime: float, script_path: str) -> bool:
    """Check if a script needs to be regenerated.

    Args:
        lockfile_mtime: The modification time of the environment's lockfile
        yaml_mtime: The modification time of the environment's manifest file
        script_path: Path to the cached activation/deactivation script
    Returns:
        True if the script doesn't exist or is older than the yamlfile or lockfile
    """
    if not os.path.isfile(script_path):
        return True

    if yaml_mtime > os.stat(script_path).st_mtime:
        return True

    # Script does NOT need update if no lockfile exists
    if lockfile_mtime == 0.0:
        return False

    script_mtime = os.stat(script_path).st_mtime
    return lockfile_mtime >= script_mtime


def _write_env_script(
    env: "spack.environment.Environment", view: Optional[str] = None, activate: bool = True
):
    """Helper method for write_env_(de)activate_script methods"""

    # Ensure .env subdir exists
    env.ensure_env_directory_exists(dot_env=True)

    # Get yamlfile & lockfile modification time
    yaml_mtime = os.stat(env.manifest_path).st_mtime if os.path.isfile(env.manifest_path) else 0.0
    lockfile_mtime = os.stat(env.lock_path).st_mtime if os.path.isfile(env.lock_path) else 0.0

    if activate:
        script_type = "activate"
    else:
        script_type = "deactivate"

    shells = ["bat", "pwsh"] if sys.platform == "win32" else ["sh"]

    for shell in shells:
        script_path = path_to_env_script(env, shell, script_type, view)

        if _script_needs_update(
            yaml_mtime, lockfile_mtime, script_path
        ) or not _script_matches_env(env, script_path, view):
            if activate:
                _, cmds = get_activate_commands(env, view=view, shell=shell, use_cache=True)
            else:
                _, cmds = get_deactivate_commands(env, view=view, shell=shell, use_cache=True)
            uenv.write_shell_script(script_path, cmds, shell)


def path_to_env_script(env, shell: str, script_type: str, view: Optional[str] = None) -> str:
    """Returns path to the shell script for activating or deactivating an environment.

    Args:
        env: the environment whose shell script we are returning the path of
        shell: the shell that the user is running
        script_type: Either 'activate' or 'deactivate'
        view: the name of the environment's view
    """
    if shell == "bat":
        extension = ".bat"
    elif shell == "pwsh":
        extension = ".ps1"
    else:
        extension = ""

    script_name = (
        f"{view}_{script_type}{extension}" if view else f"noview_{script_type}{extension}"
    )

    return os.path.join(env.path, ".spack-env", script_name)


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


def set_despacktivate_and_prompt_cmds(env, shell, prompt: Optional[str] = None) -> str:
    """Returns the set prompt and alias despacktivate commands which are unique to each shell.

    Args:
        shell: the shell that the user is running
        prompt: name of user's prompt
    """
    despactivate_cmd = spack.environment.shell.alias_despacktivate_cmds(shell)
    prompt_cmds = spack.environment.shell.activate_prompt_cmds(env, shell, prompt)

    return despactivate_cmd + prompt_cmds


def remove_despacktivate_and_prompt_cmds(shell) -> str:
    """Returns the unset prompt and unalias despacktivate commands which are unique to each shell.

    Args:
        shell: the shell that the user is running
    """
    despactivate_cmd = spack.environment.shell.unalias_despacktivate_cmds(shell)
    prompt_cmds = spack.environment.shell.deactivate_prompt_cmds(shell)

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
