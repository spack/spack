# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from datetime import datetime

import spack.environment.shell
import spack.store
from spack.util.environment import EnvironmentModifications


def path_to_env_activate_shell_script(env, shell) -> str:
    """Returns to path to the shell script to activate the specified env for the shell that
    the user is running

    Args:
        env: the environment whose shell script we are returning the path of
        shell: the shell that the user is running
    """
    if shell == "sh" or shell == "csh" or shell == "fish":
        shell = ""
    else:
        shell = f".{shell}"
    return os.path.join(env.path, ".spack-env", f"activate{shell}")


def path_to_env_deactivate_shell_script(env, shell) -> str:
    """Returns to path to the shell script to activate the specified env for the shell that
    the user is running

    Args:
        env: the environment whose shell script we are returning the path of
        shell: the shell that the user is running
    """

    return os.path.join(env.path, ".spack-env", f"deactivate.{shell}")


def get_shell_unique_env_cmds(shell, prompt, view) -> str:
    """Returns the prompt, view, and despacktivate commands which are unique
    to each shell

    Args:
        shell: the shell that the user is running
        prompt: name of user's prompt
        view: name of environment's view
    """

    despactivate_cmd = spack.environment.shell.despacktivate_cmds(shell)
    prompt_cmds = spack.environment.shell.activate_prompt_cmds(shell, prompt)
    view_cmd = spack.environment.shell.activate_view_cmds(shell, view)

    cmds = despactivate_cmd + prompt_cmds + view_cmd

    return cmds


def lockfile_newer_than_script(lockfile_date, script_path) -> bool:
    """Returns true of the environment's lockfile has been change more recently than the
    activation or deactivations script

    Args:
        lockfile_date: a timestamp of when the lockfile was last updated
        script_path: a path to the cached activation/deactivation script
    """

    if os.path.isfile(script_path):
        script_path_date = os.stat(script_path).st_mtime
    else:
        return True

    return lockfile_date > script_path_date


def write_env_activate_script(env, view):
    """Gets and writes the environment modifications for an activated environment to a
    cached shell script

    Args:
        env: the environment the activation script is written for
        view: the name of the environment's view
    """

    shells_avail = ["sh"]  # csh & fish have the same script as sh

    if sys.platform == "win32":
        shells_avail.extend(["bat", "pwsh"])

    for shell in shells_avail:
        env_mods = EnvironmentModifications()

        cmds = spack.environment.shell.activate_commands(env, shell, view=view)
        cmds += env_mods.shell_modifications(shell)

        activate_script_path = path_to_env_activate_shell_script(env, shell)

        with open(activate_script_path, "w", encoding="utf-8") as f:
            f.write(
                f"### Script created by spack (https://github.com/spack/spack) {datetime.today().strftime('%Y-%m-%d')}\n\n"
            )
            f.write(cmds)


def update_env_activate_script(env, view="default"):
    """Overwrite existing environment activation script with new environment modifications

    Args:
        env: the environment the activation script is written for
        prompt: name of environment's prompt
        view: the name of the environment's view
    """

    shells_avail = ["sh"]  # csh & fish have the same script as sh

    if sys.platform == "win32":
        shells_avail.extend(["bat", "pwsh"])

    if os.path.isfile(env.lock_path):
        lockfile_date = os.stat(env.lock_path).st_mtime
    else:
        lockfile_date = 0.00

    for shell in shells_avail:
        activate_script_path = path_to_env_activate_shell_script(env, shell)

        if lockfile_date != 0.00 and not lockfile_newer_than_script(
            lockfile_date, activate_script_path
        ):
            spack.environment.shell.activate(env=env, view=view)

            continue

        env_mods = EnvironmentModifications()
        env_mods.extend(spack.environment.shell.activate(env=env, view=view))

        cmds = spack.environment.shell.activate_commands(env, shell, view=view)
        cmds += env_mods.shell_modifications(shell)

        with open(activate_script_path, "w", encoding="utf-8") as f:
            f.write(
                f"### Script created by spack (https://github.com/spack/spack) {datetime.today().strftime('%Y-%m-%d')}\n\n"
            )
            f.write(cmds)


def write_env_deactivate_script(env, view):
    """Gets and writes the environment modifications to deactivate the specified
    environment to a cached shell script

    Args:
        env: the environment the deactivation script is written for
    """

    shells_avail = ["sh", "csh", "fish"]

    if sys.platform == "win32":
        shells_avail.extend(["bat", "pwsh"])

    if os.path.isfile(env.lock_path):
        lockfile_date = os.stat(env.lock_path).st_mtime
    else:
        lockfile_date = 0.00

    for shell in shells_avail:
        deactivate_script_path = path_to_env_deactivate_shell_script(env, shell)

        if lockfile_date != 0.00 and not lockfile_newer_than_script(
            lockfile_date, deactivate_script_path
        ):
            continue

        cmds = spack.environment.shell.deactivate_commands(shell)
        env_mods = spack.environment.shell.deactivate(env, view)

        cmds += env_mods.shell_modifications(shell)

        deactivate_script_path = os.path.join(env.path, ".spack-env", f"deactivate.{shell}")

        with spack.store.STORE.db.write_transaction():
            with open(deactivate_script_path, "w", encoding="utf-8") as f:
                f.write(
                    f"### Script created by spack (https://github.com/spack/spack) {datetime.today().strftime('%Y-%m-%d')}\n\n"
                )
                f.write(cmds)
