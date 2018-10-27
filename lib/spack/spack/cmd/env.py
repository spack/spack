# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
import argparse

import llnl.util.tty as tty
import llnl.util.filesystem as fs
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize

import spack.config
import spack.schema.env
import spack.cmd.install
import spack.cmd.uninstall
import spack.cmd.modules
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.string as string

description = "manage virtual environments"
section = "environment"
level = "long"


#: List of subcommands of `spack env`
subcommands = [
    'activate',
    'deactivate',
    'create',
    'destroy',
    ['list', 'ls'],
    'add',
    ['remove', 'rm'],
    'concretize',
    ['status', 'st'],
    'loads',
    'stage',
    'install',
    'uninstall',
]


def get_env(args, cmd_name, fail_on_error=True):
    """Get target environment from args, or from environment variables.

    This is used by a number of commands for handling the environment
    argument.

    Check whether an environment was passed via arguments, then whether
    it was passed via SPACK_ENV.  If an environment is found, read it in.
    If not, print an error message referencing the calling command.

    Arguments:
        args (Namespace): argparse namespace wtih command arguments
        cmd_name (str): name of calling command

    """
    env = args.env
    if not env:
        env = os.environ.get('SPACK_ENV')
        if not env:
            if not fail_on_error:
                return None
            tty.die(
                'spack env %s requires an active environment or an argument'
                % cmd_name)

    environment = ev.disambiguate(env)
    if not environment:
        tty.die('no such environment: %s' % env)
    return environment


#
# env activate
#
def env_activate_setup_parser(subparser):
    """set the current environment"""
    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        '--sh', action='store_const', dest='shell', const='sh',
        help="print sh commands to activate the environment")
    shells.add_argument(
        '--csh', action='store_const', dest='shell', const='csh',
        help="print csh commands to activate the environment")
    shells.add_argument(
        '-d', '--dir', action='store_true', default=False,
        help="force spack to treat env as a directory, not a name")

    subparser.add_argument(
        '-p', '--prompt', action='store_true', default=False,
        help="decorate the command line prompt when activating")
    subparser.add_argument(
        metavar='env', dest='activate_env',
        help='name of environment to activate')


def env_activate(args):
    if not args.activate_env:
        tty.die('spack env activate requires an environment name')

    env = args.activate_env
    if not args.shell:
        msg = [
            "This command works best with Spack's shell support",
            ""
        ] + spack.cmd.common.shell_init_instructions + [
            'Or, if you want to use `spack env activate` without initializing',
            'shell support, you can run one of these:',
            '',
            '    eval `spack env activate --sh %s`   # for bash/sh' % env,
            '    eval `spack env activate --csh %s`  # for csh/tcsh' % env,
        ]
        tty.msg(*msg)
        return 1

    if ev.exists(env) and not args.dir:
        spack_env = ev.root(env)
        short_name = env
        env_prompt = '[%s]' % env

    elif ev.is_env_dir(env):
        spack_env = os.path.abspath(env)
        short_name = os.path.basename(os.path.abspath(env))
        env_prompt = '[%s]' % short_name

    else:
        tty.die("No such environment: '%s'" % env)

    if args.shell == 'csh':
        # TODO: figure out how to make color work for csh
        sys.stdout.write('setenv SPACK_ENV %s;\n' % spack_env)
        sys.stdout.write('alias despacktivate "spack env deactivate";\n')
        if args.prompt:
            sys.stdout.write('if (! $?SPACK_OLD_PROMPT ) '
                             'setenv SPACK_OLD_PROMPT "${prompt}";\n')
            sys.stdout.write('set prompt="%s ${prompt}";\n' % env_prompt)

    else:
        if 'color' in os.environ['TERM']:
            env_prompt = colorize('@G{%s} ' % env_prompt, color=True)

        sys.stdout.write('export SPACK_ENV=%s;\n' % spack_env)
        sys.stdout.write("alias despacktivate='spack env deactivate';\n")
        if args.prompt:
            sys.stdout.write('if [ -z "${SPACK_OLD_PS1}" ]; then\n')
            sys.stdout.write('export SPACK_OLD_PS1="${PS1}"; fi;\n')
            sys.stdout.write('export PS1="%s ${PS1}";\n' % env_prompt)


#
# env deactivate
#
def env_deactivate_setup_parser(subparser):
    """deactivate any active environment in the shell"""
    shells = subparser.add_mutually_exclusive_group()
    shells.add_argument(
        '--sh', action='store_const', dest='shell', const='sh',
        help="print sh commands to deactivate the environment")
    shells.add_argument(
        '--csh', action='store_const', dest='shell', const='csh',
        help="print csh commands to deactivate the environment")


def env_deactivate(args):
    if not args.shell:
        msg = [
            "This command works best with Spack's shell support",
            ""
        ] + spack.cmd.common.shell_init_instructions + [
            'Or, if you want to use `spack env activate` without initializing',
            'shell support, you can run one of these:',
            '',
            '    eval `spack env deactivate --sh`   # for bash/sh',
            '    eval `spack env deactivate --csh`  # for csh/tcsh',
        ]
        tty.msg(*msg)
        return 1

    if 'SPACK_ENV' not in os.environ:
        tty.die('No environment is currently active.')

    if args.shell == 'csh':
        sys.stdout.write('unsetenv SPACK_ENV;\n')
        sys.stdout.write('if ( $?SPACK_OLD_PROMPT ) '
                         'set prompt="$SPACK_OLD_PROMPT" && '
                         'unsetenv SPACK_OLD_PROMPT;\n')
        sys.stdout.write('unalias despacktivate;\n')

    else:
        sys.stdout.write('unset SPACK_ENV; export SPACK_ENV;\n')
        sys.stdout.write('unalias despacktivate;\n')
        sys.stdout.write('if [ -n "$SPACK_OLD_PS1" ]; then\n')
        sys.stdout.write('export PS1="$SPACK_OLD_PS1";\n')
        sys.stdout.write('unset SPACK_OLD_PS1; export SPACK_OLD_PS1;\n')
        sys.stdout.write('fi;\n')


#
# env create
#
def env_create_setup_parser(subparser):
    """create a new environment"""
    subparser.add_argument('env', help='name of environment to create')
    subparser.add_argument(
        '-d', '--dir', action='store_true',
        help='create an environment in a specific directory')
    subparser.add_argument(
        'envfile', nargs='?', default=None,
        help='optional init file; can be spack.yaml or spack.lock')


def env_create(args):
    if args.envfile:
        with open(args.envfile) as f:
            _env_create(args.env, f, args.dir)
    else:
        _env_create(args.env, None, args.dir)


def _env_create(name_or_path, init_file=None, dir=False):
    """Create a new environment, with an optional yaml description.

    Arguments:
        name_or_path (str): name of the environment to create, or path to it
        init_file (str or file): optional initialization file -- can be
            spack.yaml or spack.lock
        dir (bool): if True, create an environment in a directory instead
            of a named environment
    """
    if dir:
        env = ev.Environment(name_or_path, init_file)
        env.write()
        tty.msg("Created environment in %s" % env.path)
    else:
        env = ev.create(name_or_path, init_file)
        env.write()
        tty.msg("Created environment '%s' in %s" % (name_or_path, env.path))
    return env


#
# env remove
#
def env_destroy_setup_parser(subparser):
    """destroy an existing environment"""
    subparser.add_argument(
        'env', nargs='+', help='environment(s) to destroy')
    arguments.add_common_arguments(subparser, ['yes_to_all'])


def env_destroy(args):
    if not args.yes_to_all:
        answer = tty.get_yes_or_no(
            'Really destroy %s %s?' % (
                string.plural(len(args.env), 'environment', show_n=False),
                string.comma_and(args.env)),
            default=False)
        if not answer:
            tty.die("Will not destroy any environments")

    for env in args.env:
        ev.destroy(env)
        tty.msg("Successfully destroyed environment '%s'" % env)


#
# env list
#
def env_list_setup_parser(subparser):
    """list available environments"""
    pass


def env_list(args):
    names = ev.list_environments()

    color_names = []
    for name in names:
        if ev.active and name == ev.active.name:
            name = colorize('@*g{%s}' % name)
        color_names.append(name)

    # say how many there are if writing to a tty
    if sys.stdout.isatty():
        if not names:
            tty.msg('No environments')
        else:
            tty.msg('%d environments' % len(names))

    colify(color_names, indent=4)


#
# env add
#
def env_add_setup_parser(subparser):
    """add a spec to an environment"""
    subparser.add_argument(
        '-e', '--env', help='add spec to this environment')
    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="spec of the package to add")


def env_add(args):
    env = get_env(args, 'add')

    for spec in spack.cmd.parse_specs(args.specs):
        if not env.add(spec):
            tty.msg("Package {0} was already added to {1}"
                    .format(spec.name, env.name))
        else:
            tty.msg('Adding %s to environment %s' % (spec, env.name))
    env.write()


#
# env remove
#
def env_remove_setup_parser(subparser):
    """remove a spec from an environment"""
    subparser.add_argument(
        '-e', '--env', help='remove spec with this name from environment')
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="Remove all specs from (clear) the environment")
    subparser.add_argument(
        'specs', nargs=argparse.REMAINDER, help="specs to be removed")


def env_remove(args):
    env = get_env(args, 'remove <spec>')

    if args.all:
        env.clear()
    else:
        for spec in spack.cmd.parse_specs(args.specs):
            tty.msg('Removing %s from environment %s' % (spec, env.name))
            env.remove(spec)
    env.write()


#
# env concretize
#
def env_concretize_setup_parser(subparser):
    """concretize user specs and write lockfile"""
    subparser.add_argument(
        'env', nargs='?', help='concretize all packages for this environment')
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")


def env_concretize(args):
    env = get_env(args, 'status')
    _env_concretize(env, use_repo=args.use_env_repo, force=args.force)


def _env_concretize(env, use_repo=False, force=False):
    """Function body separated out to aid in testing."""
    env.concretize(force=force)
    env.write()


# REMOVE
# env install
#
def env_install_setup_parser(subparser):
    """concretize and install all specs in an environment"""
    subparser.add_argument(
        'env', nargs='?', help='install all packages in this environment')
    subparser.add_argument(
        '--only-concrete', action='store_true', default=False,
        help='only install already concretized specs')
    spack.cmd.install.add_common_arguments(subparser)


def env_install(args):
    env = get_env(args, 'status')

    # concretize unless otherwise specified
    if not args.only_concrete:
        env.concretize()
        env.write()

    # install all specs in the environment
    env.install_all(args)


# REMOVE
# env uninstall
#
def env_uninstall_setup_parser(subparser):
    """uninstall packages from an environment"""
    subparser.add_argument(
        'env', nargs='?', help='uninstall all packages in this environment')
    spack.cmd.uninstall.add_common_arguments(subparser)


def env_uninstall(args):
    env = get_env(args, 'uninstall')
    env.uninstall(args)


#
# env status
#
def env_status_setup_parser(subparser):
    """get install status of specs in an environment"""
    subparser.add_argument(
        'env', nargs='?', help='name of environment to show status for')
    arguments.add_common_arguments(
        subparser,
        ['recurse_dependencies', 'long', 'very_long'])


def env_status(args):
    env = get_env(args, 'status', fail_on_error=False)
    if not env:
        tty.msg('No active environment')
        return

    # TODO: option to show packages w/ multiple instances?
    env.status(
        sys.stdout, recurse_dependencies=args.recurse_dependencies,
        hashes=args.long or args.very_long,
        hashlen=None if args.very_long else 7,
        install_status=True)


#
# env stage
#
def env_stage_setup_parser(subparser):
    """download all source files for all packages in an environment"""
    subparser.add_argument(
        'env', nargs='?', help='name of env to generate loads file for')


def env_stage(args):
    env = get_env(args, 'stage')
    for spec in env.specs_by_hash.values():
        for dep in spec.traverse():
            dep.package.do_stage()


#
# env loads
#
def env_loads_setup_parser(subparser):
    """list modules for an installed environment '(see spack module loads)'"""
    subparser.add_argument(
        'env', nargs='?', help='name of env to generate loads file for')
    subparser.add_argument(
        '-m', '--module-type', choices=('tcl', 'lmod'),
        help='type of module system to generate loads for')
    spack.cmd.modules.add_loads_arguments(subparser)


def env_loads(args):
    env = get_env(args, 'loads')

    # Set the module types that have been selected
    module_type = args.module_type
    if module_type is None:
        # If no selection has been made select all of them
        module_type = 'tcl'

    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False

    loads_file = fs.join_path(env.path, 'loads')
    with open(loads_file, 'w') as f:
        specs = env._get_environment_specs(
            recurse_dependencies=recurse_dependencies)

        spack.cmd.modules.loads(module_type, specs, args, f)

    print('To load this environment, type:')
    print('   source %s' % loads_file)


#: Dictionary mapping subcommand names and aliases to functions
subcommand_functions = {}


#
# spack env
#
def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='env_command')

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = 'env_%s' % name
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = 'env_%s_setup_parser' % name
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(
            name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def env(parser, args, **kwargs):
    """Look for a function called environment_<name> and call it."""
    action = subcommand_functions[args.env_command]
    action(args)
