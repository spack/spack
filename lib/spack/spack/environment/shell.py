# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import textwrap
import warnings
from typing import List, Mapping, Optional

import spack.config
import spack.environment as ev
import spack.repo
import spack.schema.environment
import spack.store
import spack.user_environment as uenv
import spack.util.undo_record as undo_record
from spack.util import tty
from spack.util.environment import EnvironmentModifications, ShellCmdString
from spack.util.tty.color import colorize


def _make_spack_prompt(shell: str, prompt: str) -> List[str]:
    shell_cmd = ShellCmdString(shell)
    if shell == "csh":
        # TODO: figure out how to make color work for csh
        return [
            'if (! $?SPACK_OLD_PROMPT ) setenv SPACK_OLD_PROMPT "${prompt}"',
            'set prompt="%s ${prompt}"' % prompt,
        ]
    elif shell == "fish":
        # NOTE: We're not changing the fish_prompt function (which is fish's
        # solution to the PS1 variable) here. This is a bit fiddly, and easy to
        # screw up => spend time reasearching a solution. Feedback welcome.
        return []
    elif shell == "bat":
        # TODO: Color
        old_prompt = os.environ.get("SPACK_OLD_PROMPT")
        if not old_prompt:
            old_prompt = os.environ.get("PROMPT")
        return [
            shell_cmd.set("SPACK_OLD_PROMPT", str(old_prompt)),
            shell_cmd.set("PROMPT", f"{prompt} $P$G"),
        ]
    elif shell == "pwsh":
        return [
            "function global:prompt { $pth = $(Convert-Path $(Get-Location))"
            ' | Split-Path -leaf; if(!"$Env:SPACK_OLD_PROMPT") '
            '{$Env:SPACK_OLD_PROMPT="[spack] PS $pth>"}; '
            '"%s PS $pth>"}' % prompt
        ]
    else:
        bash_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=True)
        zsh_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=False, zsh=True)
        return [
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
        ]


def _short_name(env: ev.Environment) -> str:
    if env.name == env.path:
        return os.path.basename(env.path)
    return env.name


def activate_header(
    env: ev.Environment, shell: str, prompt: bool = False, view: Optional[str] = None
):
    short_name = _short_name(env)

    # Construct the commands to run
    shell_cmd = ShellCmdString(shell)
    cmds: List[str] = [shell_cmd.set("SPACK_ENV", env.path)]
    if view:
        cmds.append(shell_cmd.set("SPACK_ENV_VIEW", view))
    cmds.extend(shell_cmd.alias("despacktivate", "spack env deactivate"))

    if prompt:
        cmds.extend(_make_spack_prompt(shell, f"[{short_name}]"))
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


#: Kind of the undo record unit holding the changes made by activating an environment
_ENV_KIND = "env"


def read_undo_record(environ: Mapping[str, str]) -> undo_record.UndoRecord:
    """Returns the undo record stored in ``environ``. Units undone outside the record (environment
    not in ``SPACK_ENV``, spec not in ``SPACK_LOADED_HASHES``) are dropped, and the variables keep
    their value.
    """
    record = undo_record.UndoRecord.from_environ(environ)
    stale = uenv.unloaded_keys(record, environ)
    unit = record.find(_ENV_KIND)
    active = environ.get(ev.spack_env_var)
    if unit is not None and (active is None or unit.key != _environment_key(active)):
        stale.append(unit.key)
    if stale:
        record.forget(stale)
    return record


def _environment_key(path: str) -> str:
    return undo_record.unit_key(_ENV_KIND, path)


def activate(
    env: ev.Environment,
    record: undo_record.UndoRecord,
    use_env_repo=False,
    view: Optional[str] = "default",
) -> None:
    """Activates an environment, and pushes its environment modifications on the undo record of
    the shell.

    To activate an environment, we add its configuration scope to the
    existing Spack configuration, and we set active to the current
    environment.

    Arguments:
        env: the environment to activate
        record: undo record of the shell
        use_env_repo: use the packages exactly as they appear in the environment's repository
        view: generate commands to add runtime environment variables for named view
    """
    ev.activate(env, use_env_repo=use_env_repo)

    env_mods = EnvironmentModifications()
    env_mods.set("VIRTUAL_ENV_PROMPT", _short_name(env))

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

    record.push(
        undo_record.Unit(_environment_key(env.path), undo_record.ops_from_modifications(env_mods))
    )


def deactivate(record: undo_record.UndoRecord) -> None:
    """Deactivate the active environment, removing its unit from the undo record of the shell.

    An environment activated without a record (by an older Spack, or before the shell was
    updated) cannot be undone: its changes to the shell environment are left in place, with a
    warning.
    """
    unit = record.find(_ENV_KIND)
    if unit is None:
        warnings.warn(
            "the environment was activated without an undo record, so its changes to "
            "environment variables are left in the shell"
        )
    else:
        record.remove(unit.key)

    ev.deactivate()
