# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import textwrap
from typing import Optional

import spack.config
import spack.repo
import spack.schema.environment
import spack.store
from spack.util import tty
from spack.util.environment import EnvironmentModifications
from spack.util.tty.color import colorize


def activate_commands(env, view: Optional[str] = None):
    # Construct the commands to run
    cmds = f"_spack_env_set SPACK_ENV {env.path}\n"

    if view:
        cmds += f"_spack_env_set SPACK_ENV_VIEW {view}\n"
    return cmds


def despacktivate_cmds(shell):
    cmd = ""
    if shell == "csh":
        # TODO: figure out how to make color work for csh
        cmd += 'alias despacktivate "spack env deactivate";\n'
    elif shell == "fish":
        cmd += "function despacktivate;\n"
        cmd += "   spack env deactivate;\n"
        cmd += "end;\n"
    elif shell == "sh":
        cmd += "alias despacktivate='spack env deactivate';\n"
    return cmd


def activate_prompt_cmds(shell, prompt):
    bash_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=True)
    zsh_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=False, zsh=True)

    cmds = ""

    if not prompt:
        return cmds

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
    elif shell == "bat":
        # TODO: Color
        if prompt:
            old_prompt = os.environ.get("SPACK_OLD_PROMPT")
            if not old_prompt:
                old_prompt = os.environ.get("PROMPT")
            cmds += f"_spack_env_set SPACK_OLD_PROMPT {old_prompt}"
            cmds += f"_spack_env_set PROMPT {prompt} $P$G"
    elif shell == "pwsh":
        cmds += (
            "function global:prompt { $pth = $(Convert-Path $(Get-Location))"
            ' | Split-Path -leaf; if(!"$Env:SPACK_OLD_PROMPT") '
            '{$Env:SPACK_OLD_PROMPT="[spack] PS $pth>"}; '
            '"%s PS $pth>"}' % prompt
        )
    else:
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



def activate(env, view: Optional[str] = "default") -> EnvironmentModifications:
    """Compute environment modifications for activating an environment.

    Arguments:
        env: the environment to activate
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

    env_vars_yaml = spack.config.CONFIG.get("env_vars", None)
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
            "  To remove it and resolve the issue, force concretize with the command:\n",
            "    spack -e {0} concretize --force".format(env.name),
        )

    return env_mods


def validate_view(env, view: Optional[str] = "default") -> None:
    """Validate that an environment's view is accessible.

    This checks if the view can be loaded and prints warnings if packages
    or repos are missing/broken. This is useful when using cached activation
    scripts to ensure the repo context hasn't changed.

    Arguments:
        env: the environment to validate
        view: the view name to validate
    """
    # Simply call activate() and discard the result - it will trigger
    # the same validation and error handling
    _ = activate(env, view)


def deactivate_commands(shell):
    # TODO: Color for bat
    cmds = "_spack_env_unset SPACK_ENV\n"
    cmds += "_spack_env_unset SPACK_ENV_VIEW\n"

    if shell == "csh":
        cmds += "if ( $?SPACK_OLD_PROMPT ) "
        cmds += "    eval '_spack_env_set prompt SPACK_OLD_PROMPT &&"
        cmds += "          _spack_env_unset SPACK_OLD_PROMPT';\n"
        cmds += "unalias despacktivate;\n"
    elif shell == "fish":
        cmds += "functions -e despacktivate;\n"
        #
        # NOTE: Not changing fish_prompt (above) => no need to restore it here.
        #
    elif shell == "bat":
        # TODO: despacktivate
        old_prompt = os.environ.get("SPACK_OLD_PROMPT")
        if old_prompt:
            cmds += f"_spack_env_set PROMPT {old_prompt}\n"
            cmds += "_spack_env_unset SPACK_OLD_PROMPT\n"
    elif shell == "pwsh":
        cmds += (
            "function global:prompt { $pth = $(Convert-Path $(Get-Location))"
            ' | Split-Path -leaf; $spack_prompt = "[spack] $pth >"; '
            'if("$Env:SPACK_OLD_PROMPT") {$spack_prompt=$Env:SPACK_OLD_PROMPT};'
            " $spack_prompt}\n"
        )
    else:
        cmds += textwrap.dedent(
            """
                alias despacktivate > /dev/null 2>&1 && unalias despacktivate;
                if [ ! -z ${SPACK_OLD_PS1+x} ]; then
                    if [ "$SPACK_OLD_PS1" = '$$$$' ]; then
                        unset PS1;
                    else
                        export PS1="$SPACK_OLD_PS1";
                    fi;
                    unset SPACK_OLD_PS1;
                fi
            """
        ).strip("\n")

    return cmds


def deactivate(active_env, view) -> EnvironmentModifications:
    """Deactivate an environment and collect corresponding environment modifications.

    Note: unloads the environment in its current state, not in the state it was
        loaded in, meaning that specs that were removed from the spack environment
        after activation are not unloaded.

    Args:
        active_env (Environment): the current active environment to deactivate
        view (str): the view to deactivate

    Returns:
        Environment variables modifications to activate environment.
    """
    env_mods = EnvironmentModifications()

    if active_env is None:
        return env_mods

    with active_env.manifest.use_config():
        env_vars_yaml = spack.config.CONFIG.get("env_vars", None)
    if env_vars_yaml:
        env_mods.extend(spack.schema.environment.parse(env_vars_yaml).reversed())

    if view:
        try:
            with spack.store.STORE.db.read_transaction():
                active_env.rm_view_from_env(env_mods, view)
        except (spack.repo.UnknownPackageError, spack.repo.UnknownNamespaceError) as e:
            tty.warn(e)
            tty.warn(
                "Could not fully deactivate view due to missing package "
                "or repo, shell environment may be corrupt."
            )

    return env_mods
