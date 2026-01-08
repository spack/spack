# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import textwrap
from typing import Optional

import spack.config
import spack.llnl.util.tty as tty
import spack.repo
import spack.schema.environment
import spack.store
from spack.llnl.util.tty.color import colorize
from spack.util.environment import EnvironmentModifications


def activate_header(env, shell, view: Optional[str] = None):
    # Construct the commands to run
    cmds = ""
    if shell == "csh":
        # TODO: figure out how to make color work for csh
        cmds += f"_spack_env_set SPACK_ENV {env.path};\n"
        if view:
            cmds += f"_spack_env_set SPACK_ENV_VIEW {view};\n"
        cmds += 'alias despacktivate "spack env deactivate";\n'
    elif shell == "fish":
        cmds += f"_spack_env_set SPACK_ENV {env.path};\n"
        cmds += "function despacktivate;\n"
        cmds += "   spack env deactivate;\n"
        cmds += "end;\n"
    elif shell == "bat":
        # TODO: Color
        cmds += f'set "SPACK_ENV={env.path}"\n'
        if view:
            cmds += f'set "SPACK_ENV_VIEW={view}"\n'
    elif shell == "pwsh":
        cmds += f"$Env:SPACK_ENV='{env.path}'\n"
        if view:
            cmds += f"$Env:SPACK_ENV_VIEW='{view}'\n"
    else:
        cmds += f"_spack_env_set SPACK_ENV {env.path}\n"
        if view:
            cmds += f"_spack_env_set SPACK_ENV_VIEW {view} \n"
        cmds += "alias despacktivate='spack env deactivate';\n"
    return cmds


def activate_with_prompt(shell, prompt):
    bash_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=True)
    zsh_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=False, zsh=True)

    cmds = ""

    if shell == "csh":
        cmds += "if (! $?SPACK_OLD_PROMPT ) "
        cmds += f"_spack_env_set SPACK_OLD_PROMPT {prompt}\n"
        cmds += f"_spack_env_set prompt {prompt}\n"
    elif shell == "fish":
        if "color" in os.getenv("TERM", ""):
            prompt = colorize(f"@G{prompt} ", color=True)
        #
        # NOTE: We're not changing the fish_prompt function (which is fish's
        # solution to the PS1 variable) here. This is a bit fiddly, and easy to
        # screw up => spend time reasearching a solution. Feedback welcome.
        #
    elif shell == "sh":
        cmds = textwrap.dedent(
            rf"""
            if [ -z ${{SPACK_OLD_PS1+x}} ]; then
                if [ -z ${{PS1+x}} ]; then
                    PS1='$$$$';
                fi;
                export SPACK_OLD_PS1="${{PS1}}";
            fi;
            if [ -n "${{TERM:-}}" ] && [ "${{TERM#*color}}" != "${{TERM}}" ] && \
                [ -n "${{BASH:-}}" ];
            then
                export PS1="{bash_color_prompt} ${{PS1}}";
            elif [ -n "${{TERM:-}}" ] && [ "${{TERM#*color}}" != "${{TERM}}" ] && \
                    [ -n "${{ZSH_NAME:-}}" ];
            then
                export PS1="{zsh_color_prompt} ${{PS1}}";
            else
                export PS1="{prompt} ${{PS1}}";
            fi
            """
        ).lstrip("\n")
    return cmds


def activate_with_view(shell, view):
    cmd = ""
    if shell == "csh":
        cmd = f"_spack_env_set SPACK_ENV_VIEW {view};\n"
    elif shell == "bat":
        cmd = f'set "SPACK_ENV_VIEW={view}"\n'
    elif shell == "pwsh":
        cmd = f"$Env:SPACK_ENV_VIEW='{view}'\n"
    elif shell == "sh":
        cmd = f"_spack_env_set SPACK_ENV_VIEW {view}\n"
    return cmd


def deactivate_header(shell):
    cmds = ""
    if shell == "csh":
        cmds += "_spack_env_unset SPACK_ENV;\n"
        cmds += "_spack_env_unset SPACK_ENV_VIEW;\n"
        cmds += "if ( $?SPACK_OLD_PROMPT ) "
        cmds += '    eval \'_spack_env_set prompt SPACK_OLD_PROMPT &&'
        cmds += "          _spack_env_unset SPACK_OLD_PROMPT';\n"
        cmds += "unalias despacktivate;\n"
    elif shell == "fish":
        cmds += "set -e SPACK_ENV;\n"
        cmds += "set -e SPACK_ENV_VIEW;\n"
        cmds += "functions -e despacktivate;\n"
        #
        # NOTE: Not changing fish_prompt (above) => no need to restore it here.
        #
    elif shell == "bat":
        # TODO: Color
        cmds += 'set "SPACK_ENV="\n'
        cmds += 'set "SPACK_ENV_VIEW="\n'
        # TODO: despacktivate
        old_prompt = os.environ.get("SPACK_OLD_PROMPT")
        if old_prompt:
            cmds += f'set "PROMPT={old_prompt}"\n'
            cmds += 'set "SPACK_OLD_PROMPT="\n'
    elif shell == "pwsh":
        cmds += "Set-Item -Path Env:SPACK_ENV\n"
        cmds += "Set-Item -Path Env:SPACK_ENV_VIEW\n"
        cmds += (
            "function global:prompt { $pth = $(Convert-Path $(Get-Location))"
            ' | Split-Path -leaf; $spack_prompt = "[spack] $pth >"; '
            'if("$Env:SPACK_OLD_PROMPT") {$spack_prompt=$Env:SPACK_OLD_PROMPT};'
            " $spack_prompt}\n"
        )
    else:
        cmds += "if [ ! -z ${SPACK_ENV+x} ]; then\n"
        cmds += "unset SPACK_ENV; export SPACK_ENV;\n"
        cmds += "fi;\n"
        cmds += "if [ ! -z ${SPACK_ENV_VIEW+x} ]; then\n"
        cmds += "unset SPACK_ENV_VIEW; export SPACK_ENV_VIEW;\n"
        cmds += "fi;\n"
        cmds += "alias despacktivate > /dev/null 2>&1 && unalias despacktivate;\n"
        cmds += "if [ ! -z ${SPACK_OLD_PS1+x} ]; then\n"
        cmds += "    if [ \"$SPACK_OLD_PS1\" = '$$$$' ]; then\n"
        cmds += "        unset PS1; export PS1;\n"
        cmds += "    else\n"
        cmds += '        export PS1="$SPACK_OLD_PS1";\n'
        cmds += "    fi;\n"
        cmds += "    unset SPACK_OLD_PS1; export SPACK_OLD_PS1;\n"
        cmds += "fi;\n"

    return cmds


def activate(env, use_env_repo=False, view: Optional[str] = "default") -> EnvironmentModifications:
    """Activate an environment and append environment modifications

    To activate an environment, we add its configuration scope to the
    existing Spack configuration, and we set active to the current
    environment.

    Arguments:
        env: the environment to activate
        use_env_repo: use the packages exactly as they appear in the environment's repository
        view: generate commands to add runtime environment variables for named view

    Returns:
        spack.util.environment.EnvironmentModifications: Environment variables
        modifications to activate environment."""

    env_mods = EnvironmentModifications()

    #
    # NOTE in the fish-shell: Path variables are a special kind of variable
    # used to support colon-delimited path lists including PATH, CDPATH,
    # MANPATH, PYTHONPATH, etc. All variables that end in PATH (case-sensitive)
    # become PATH variables.
    #

    env_vars_yaml = spack.config.get("env_vars", None)
    if env_vars_yaml:
        env_mods.extend(spack.schema.environment.parse(env_vars_yaml))

    try:
        if view and env.has_view(view):
            with spack.store.STORE.db.read_transaction():
                env.add_view_to_env(env_mods, view)
    except (spack.repo.UnknownPackageError, spack.repo.UnknownNamespaceError) as e:
        tty.error(e)
        tty.die(
            "Environment view is broken due to a missing package or repo.\n",
            "  To activate without views enabled, activate with:\n",
            "    spack env activate -V {0}\n".format(env.name),
            "  To remove it and resolve the issue, " "force concretize with the command:\n",
            "    spack -e {0} concretize --force".format(env.name),
        )

    return env_mods


def deactivate(active_env, view) -> EnvironmentModifications:
    """Deactivate an environment and collect corresponding environment modifications.

    Note: unloads the environment in its current state, not in the state it was
        loaded in, meaning that specs that were removed from the spack environment
        after activation are not unloaded.

    Args:
        active_env (Environment): the current active environment to deactivate

    Returns:
        Environment variables modifications to activate environment.
    """
    env_mods = EnvironmentModifications()
    active = active_env

    if active is None:
        return env_mods

    with active.manifest.use_config():
        env_vars_yaml = spack.config.get("env_vars", None)
    if env_vars_yaml:
        env_mods.extend(spack.schema.environment.parse(env_vars_yaml).reversed())

    if view:
        try:
            with spack.store.STORE.db.read_transaction():
                active.rm_view_from_env(env_mods, view)
        except (spack.repo.UnknownPackageError, spack.repo.UnknownNamespaceError) as e:
            tty.warn(e)
            tty.warn(
                "Could not fully deactivate view due to missing package "
                "or repo, shell environment may be corrupt."
            )

    return env_mods
