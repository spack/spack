# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import textwrap
from typing import List, Optional

import spack.config
import spack.environment as ev
import spack.repo
import spack.schema.environment
import spack.store
from spack.active_environment import active_environment
from spack.util import tty
from spack.util.environment import EnvironmentModifications, ShellCmdString
from spack.util.tty.color import colorize


def activate_header(env, shell, prompt=None, view: Optional[str] = None):
    # Construct the commands to run
    shell_cmd = ShellCmdString(shell)
    cmds: List[str] = [shell_cmd.set("SPACK_ENV", env.path)]
    if view:
        cmds.append(shell_cmd.set("SPACK_ENV_VIEW", view))
    cmds.extend(shell_cmd.alias("despacktivate", "spack env deactivate"))

    if prompt:
        if shell == "csh":
            # TODO: figure out how to make color work for csh
            cmds.append('if (! $?SPACK_OLD_PROMPT ) setenv SPACK_OLD_PROMPT "${prompt}"')
            cmds.append('set prompt="%s ${prompt}"' % prompt)
        elif shell == "fish":
            # NOTE: We're not changing the fish_prompt function (which is fish's
            # solution to the PS1 variable) here. This is a bit fiddly, and easy to
            # screw up => spend time reasearching a solution. Feedback welcome.
            pass
        elif shell == "bat":
            # TODO: Color
            old_prompt = os.environ.get("SPACK_OLD_PROMPT")
            if not old_prompt:
                old_prompt = os.environ.get("PROMPT")
            cmds.append(shell_cmd.set("SPACK_OLD_PROMPT", str(old_prompt)))
            cmds.append(shell_cmd.set("PROMPT", f"{prompt} $P$G"))
        elif shell == "pwsh":
            cmds.append(
                "function global:prompt { $pth = $(Convert-Path $(Get-Location))"
                ' | Split-Path -leaf; if(!"$Env:SPACK_OLD_PROMPT") '
                '{$Env:SPACK_OLD_PROMPT="[spack] PS $pth>"}; '
                '"%s PS $pth>"}' % prompt
            )
        else:
            bash_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=True)
            zsh_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=False, zsh=True)
            cmds.append(
                textwrap.dedent(
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
                ).strip("\n")
            )
    return shell_cmd.join(cmds)


def deactivate_header(shell):
    shell_cmd = ShellCmdString(shell)
    cmds: List[str] = [shell_cmd.unset("SPACK_ENV"), shell_cmd.unset("SPACK_ENV_VIEW")]

    if shell == "csh":
        cmds.append(
            "if ( $?SPACK_OLD_PROMPT ) "
            '    eval \'set prompt="$SPACK_OLD_PROMPT" &&'
            "          unsetenv SPACK_OLD_PROMPT'"
        )
        cmds.append("unalias despacktivate")
    elif shell == "fish":
        cmds.append("functions -e despacktivate")
        #
        # NOTE: Not changing fish_prompt (above) => no need to restore it here.
        #
    elif shell == "bat":
        # TODO: despacktivate
        old_prompt = os.environ.get("SPACK_OLD_PROMPT")
        if old_prompt:
            cmds.append(shell_cmd.set("PROMPT", old_prompt))
            cmds.append(shell_cmd.unset("SPACK_OLD_PROMPT"))
    elif shell == "pwsh":
        cmds.append(
            "function global:prompt { $pth = $(Convert-Path $(Get-Location))"
            ' | Split-Path -leaf; $spack_prompt = "[spack] $pth >"; '
            'if("$Env:SPACK_OLD_PROMPT") {$spack_prompt=$Env:SPACK_OLD_PROMPT};'
            " $spack_prompt}"
        )
    else:
        cmds.append(
            textwrap.dedent(
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
        )

    return shell_cmd.join(cmds)


def activate(
    env: ev.Environment, use_env_repo=False, view: Optional[str] = "default"
) -> EnvironmentModifications:
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
    ev.activate(env, use_env_repo=use_env_repo)

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


def deactivate() -> EnvironmentModifications:
    """Deactivate an environment and collect corresponding environment modifications.

    Note: unloads the environment in its current state, not in the state it was
        loaded in, meaning that specs that were removed from the spack environment
        after activation are not unloaded.

    Returns:
        Environment variables modifications to activate environment.
    """
    env_mods = EnvironmentModifications()
    active = active_environment()

    if active is None:
        return env_mods

    with active.manifest.use_config():
        env_vars_yaml = spack.config.CONFIG.get("env_vars", None)
    if env_vars_yaml:
        env_mods.extend(spack.schema.environment.parse(env_vars_yaml).reversed())

    active_view = os.getenv(ev.spack_env_view_var)

    if active_view and active.has_view(active_view):
        try:
            with spack.store.STORE.db.read_transaction():
                active.rm_view_from_env(env_mods, active_view)
        except (spack.repo.UnknownPackageError, spack.repo.UnknownNamespaceError) as e:
            tty.warn(e)
            tty.warn(
                "Could not fully deactivate view due to missing package "
                "or repo, shell environment may be corrupt."
            )

    ev.deactivate()

    return env_mods
