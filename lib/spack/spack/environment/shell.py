# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import llnl.util.tty as tty
from llnl.util.tty.color import colorize

import spack.environment as ev
import spack.repo
import spack.store
from spack.util.environment import EnvironmentModifications


def activate_header(env, shell, prompt=None):
    # Construct the commands to run
    cmds = ''
    if shell == 'csh':
        # TODO: figure out how to make color work for csh
        cmds += 'setenv SPACK_ENV %s;\n' % env.path
        cmds += 'alias despacktivate "spack env deactivate";\n'
        if prompt:
            cmds += 'if (! $?SPACK_OLD_PROMPT ) '
            cmds += 'setenv SPACK_OLD_PROMPT "${prompt}";\n'
            cmds += 'set prompt="%s ${prompt}";\n' % prompt
    elif shell == 'fish':
        if 'color' in os.getenv('TERM', '') and prompt:
            prompt = colorize('@G{%s} ' % prompt, color=True)

        cmds += 'set -gx SPACK_ENV %s;\n' % env.path
        cmds += 'function despacktivate;\n'
        cmds += '   spack env deactivate;\n'
        cmds += 'end;\n'
        #
        # NOTE: We're not changing the fish_prompt function (which is fish's
        # solution to the PS1 variable) here. This is a bit fiddly, and easy to
        # screw up => spend time reasearching a solution. Feedback welcome.
        #
    else:
        if 'color' in os.getenv('TERM', '') and prompt:
            prompt = colorize('@G{%s}' % prompt, color=True)

        cmds += 'export SPACK_ENV=%s;\n' % env.path
        cmds += "alias despacktivate='spack env deactivate';\n"
        if prompt:
            cmds += 'if [ -z ${SPACK_OLD_PS1+x} ]; then\n'
            cmds += '    if [ -z ${PS1+x} ]; then\n'
            cmds += "        PS1='$$$$';\n"
            cmds += '    fi;\n'
            cmds += '    export SPACK_OLD_PS1="${PS1}";\n'
            cmds += 'fi;\n'
            cmds += 'export PS1="%s ${PS1}";\n' % prompt

    return cmds


def deactivate_header(shell):
    cmds = ''
    if shell == 'csh':
        cmds += 'unsetenv SPACK_ENV;\n'
        cmds += 'if ( $?SPACK_OLD_PROMPT ) '
        cmds += 'set prompt="$SPACK_OLD_PROMPT" && '
        cmds += 'unsetenv SPACK_OLD_PROMPT;\n'
        cmds += 'unalias despacktivate;\n'
    elif shell == 'fish':
        cmds += 'set -e SPACK_ENV;\n'
        cmds += 'functions -e despacktivate;\n'
        #
        # NOTE: Not changing fish_prompt (above) => no need to restore it here.
        #
    else:
        cmds += 'if [ ! -z ${SPACK_ENV+x} ]; then\n'
        cmds += 'unset SPACK_ENV; export SPACK_ENV;\n'
        cmds += 'fi;\n'
        cmds += 'alias despacktivate > /dev/null 2>&1 && unalias despacktivate;\n'
        cmds += 'if [ ! -z ${SPACK_OLD_PS1+x} ]; then\n'
        cmds += '    if [ "$SPACK_OLD_PS1" = \'$$$$\' ]; then\n'
        cmds += '        unset PS1; export PS1;\n'
        cmds += '    else\n'
        cmds += '        export PS1="$SPACK_OLD_PS1";\n'
        cmds += '    fi;\n'
        cmds += '    unset SPACK_OLD_PS1; export SPACK_OLD_PS1;\n'
        cmds += 'fi;\n'

    return cmds


def activate(env, use_env_repo=False, add_view=True):
    """
    Activate an environment and append environment modifications

    To activate an environment, we add its configuration scope to the
    existing Spack configuration, and we set active to the current
    environment.

    Arguments:
        env (spack.environment.Environment): the environment to activate
        use_env_repo (bool): use the packages exactly as they appear in the
            environment's repository
        add_view (bool): generate commands to add view to path variables

    Returns:
        spack.util.environment.EnvironmentModifications: Environment variables
        modifications to activate environment.
    """
    ev.activate(env, use_env_repo=use_env_repo)

    env_mods = EnvironmentModifications()

    #
    # NOTE in the fish-shell: Path variables are a special kind of variable
    # used to support colon-delimited path lists including PATH, CDPATH,
    # MANPATH, PYTHONPATH, etc. All variables that end in PATH (case-sensitive)
    # become PATH variables.
    #
    try:
        if add_view and ev.default_view_name in env.views:
            with spack.store.db.read_transaction():
                env.add_default_view_to_env(env_mods)
    except (spack.repo.UnknownPackageError,
            spack.repo.UnknownNamespaceError) as e:
        tty.error(e)
        tty.die(
            'Environment view is broken due to a missing package or repo.\n',
            '  To activate without views enabled, activate with:\n',
            '    spack env activate -V {0}\n'.format(env.name),
            '  To remove it and resolve the issue, '
            'force concretize with the command:\n',
            '    spack -e {0} concretize --force'.format(env.name))

    return env_mods


def deactivate():
    """
    Deactivate an environment and collect corresponding environment modifications.

    Note: unloads the environment in its current state, not in the state it was
        loaded in, meaning that specs that were removed from the spack environment
        after activation are not unloaded.

    Returns:
        spack.util.environment.EnvironmentModifications: Environment variables
        modifications to activate environment.
    """
    env_mods = EnvironmentModifications()
    active = ev.active_environment()

    if active is None:
        return env_mods

    if ev.default_view_name in active.views:
        try:
            with spack.store.db.read_transaction():
                active.rm_default_view_from_env(env_mods)
        except (spack.repo.UnknownPackageError,
                spack.repo.UnknownNamespaceError) as e:
            tty.warn(e)
            tty.warn('Could not fully deactivate view due to missing package '
                     'or repo, shell environment may be corrupt.')

    ev.deactivate()

    return env_mods
