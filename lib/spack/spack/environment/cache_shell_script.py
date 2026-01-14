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
        shell: the shell that the user is running on
    """

    return os.path.join(env.path, ".spack-env", f"activate.{shell}")


def path_to_env_prompt_view_shell_script(env, shell) -> str:
    """Returns to path to the shell script to prompt and view commands for the env

    Args:
        env: the environment whose shell script we are returning the path of
        shell: the shell that the user is running on
    """

    return os.path.join(env.path, ".spack-env", f"prompt_view.{shell}")


def path_to_env_deactivate_shell_script(env, shell) -> str:
    """Returns to path to the shell script to activate the specified env for the shell that
    the user is running

    Args:
        env: the environment whose shell script we are returning the path of
        shell: the shell that the user is running on
    """

    return os.path.join(env.path, ".spack-env", f"deactivate.{shell}")


def write_env_activate_script(env, view):
    """Gets and writes the environment modifications for an activated environment to a
    cached shell script

    Args:
        env: the environment the activation script is written for
        view: the name of the environment's view
    """

    shells_avail = ["sh", "csh", "fish"]

    if sys.platform == "win32":
        shells_avail.extend(["bat", "pwsh"])

    for shell in shells_avail:
        cmds = spack.environment.shell.activate_commands(env, shell, view=view)

        env_mods = EnvironmentModifications()

        cmds += env_mods.shell_modifications(shell)

        activate_script_path = path_to_env_activate_shell_script(env, shell)

        with open(activate_script_path, "w", encoding="utf-8") as f:
            f.write(
                f"### Script created by spack (https://github.com/spack/spack) {datetime.today().strftime('%Y-%m-%d')}\n\n"
            )
            f.write(cmds)


def update_env_activate_script(env, prompt="", view=""):
    """Overwrite existing environment activation script with new environment modifications

    Args:
        env: the environment the activation script is written for
        prompt: name of environment's prompt
        view: the name of the environment's view
    """

    shells_avail = ["sh", "csh", "fish"]

    if sys.platform == "win32":
        shells_avail.extend(["bat", "pwsh"])

    for shell in shells_avail:
        env_mods = EnvironmentModifications()
        env_mods.extend(spack.environment.shell.activate(env=env, view=view))

        activate_cmds = spack.environment.shell.activate_commands(env, shell)
        activate_cmds += env_mods.shell_modifications(shell)
        despactivate_cmd = spack.environment.shell.despacktivate_cmds(shell)
        prompt_cmds = spack.environment.shell.activate_prompt_cmds(shell, prompt)
        view_cmd = spack.environment.shell.activate_view_cmds(shell, view)

        activate_script_path = path_to_env_activate_shell_script(env, shell)
        prompt_view_script_path = path_to_env_prompt_view_shell_script(env, shell)

        if not os.path.isfile(prompt_view_script_path):
            with open(prompt_view_script_path, "w", encoding="utf-8") as f:
                f.write(
                    f"### Script created by spack (https://github.com/spack/spack) {datetime.today().strftime('%Y-%m-%d')}\n\n"
                )
                f.write(despactivate_cmd)
                f.write(prompt_cmds)
                f.write(view_cmd)
        source_prompts = (
            f"source {prompt_view_script_path}" if os.path.isfile(prompt_view_script_path) else ""
        )

        with open(activate_script_path, "w", encoding="utf-8") as f:
            f.write(
                f"### Script created by spack (https://github.com/spack/spack) {datetime.today().strftime('%Y-%m-%d')}\n\n"
            )
            f.write(activate_cmds)
            f.write(source_prompts)


def write_env_deactivate_script(env, view):
    """Gets and writes the environment modifications to deactivate the specified
    environment to a cached shell script

    Args:
        env: the environment the deactivation script is written for
    """

    shells_avail = ["sh", "csh", "fish"]

    if sys.platform == "win32":
        shells_avail.extend(["bat", "pwsh"])

    for shell in shells_avail:
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
