# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
import argparse
from contextlib import contextmanager

import spack.environment as ev
import spack.util.spack_yaml as syaml

import spack.config
import spack.cmd.spec
import spack.cmd.install
import spack.cmd.uninstall
import spack.cmd.module
import spack.cmd.common.arguments as arguments

import llnl.util.tty as tty
import llnl.util.filesystem as fs

description = "group a subset of packages"
section = "environment"
level = "long"


#: List of subcommands of `spack env`
subcommands = [
    'create',
    'add',
    'remove',
    'upgrade',
    'spec',
    'concretize',
    'list',
    'loads',
    'location',
    'relocate',
    'stage',
    'install',
    'uninstall'
]


# =============== Modifies Environment

def setup_create_parser(subparser):
    """create a new environment"""
    subparser.add_argument(
        '--init-file', dest='init_file',
        help='File with user specs to add and configuration yaml to use')


def environment_create(args):
    if os.path.exists(ev.root(args.environment)):
        raise tty.die("Environment already exists: " + args.environment)

    _environment_create(args.environment)


def _environment_create(name, init_config=None):
    environment = ev.Environment(name)

    user_specs = list()
    config_sections = {}
    if init_config:
        for key, val in init_config.items():
            if key == 'user_specs':
                user_specs.extend(val)
            else:
                config_sections[key] = val

    for user_spec in user_specs:
        environment.add(user_spec)

    ev.write(environment)

    # When creating the environment, the user may specify configuration
    # to place in the environment initially. Spack does not interfere
    # with this configuration after initialization so it is handled here
    if len(config_sections) > 0:
        config_basedir = fs.join_path(environment.path, 'config')
        os.mkdir(config_basedir)
        for key, val in config_sections.items():
            yaml_section = syaml.dump({key: val}, default_flow_style=False)
            yaml_file = '{0}.yaml'.format(key)
            yaml_path = fs.join_path(config_basedir, yaml_file)
            with open(yaml_path, 'w') as f:
                f.write(yaml_section)


def setup_add_parser(subparser):
    """add a spec to an environment"""
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="Add all specs listed in env.yaml")
    subparser.add_argument(
        'package', nargs=argparse.REMAINDER,
        help="Spec of the package to add")


def environment_add(args):
    ev.check_consistency(args.environment)
    environment = ev.read(args.environment)
    parsed_specs = spack.cmd.parse_specs(args.package)

    if args.all:
        # Don't allow command-line specs with --all
        if len(parsed_specs) > 0:
            tty.die('Cannot specify --all and specs too on the command line')

        yaml_specs = environment.yaml['specs']
        if len(yaml_specs) == 0:
            tty.msg('No specs to add from env.yaml')

        # Add list of specs from env.yaml file
        for user_spec, _ in yaml_specs.items():    # OrderedDict
            environment.add(str(user_spec), report_existing=False)
    else:
        for spec in parsed_specs:
            environment.add(str(spec))

    ev.write(environment)


def setup_remove_parser(subparser):
    """remove a spec from an environment"""
    subparser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="Remove all specs from (clear) the environment")
    subparser.add_argument(
        'package', nargs=argparse.REMAINDER,
        help="Spec of the package to remove")


def environment_remove(args):
    ev.check_consistency(args.environment)
    environment = ev.read(args.environment)
    if args.all:
        environment.clear()
    else:
        for spec in spack.cmd.parse_specs(args.package):
            environment.remove(spec.format())
    ev.write(environment)


def setup_spec_parser(subparser):
    """show results of concretizing a spec for an environment"""
    spack.cmd.spec.add_common_arguments(subparser)
    add_use_repo_argument(subparser)


def environment_spec(args):
    environment = ev.read(args.environment)
    ev.prepare_repository(environment, use_repo=args.use_repo)
    ev.prepare_config_scope(environment)
    spack.cmd.spec.spec(None, args)


def setup_concretize_parser(subparser):
    """concretize user specs and write lockfile"""
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")
    add_use_repo_argument(subparser)


def environment_concretize(args):
    ev.check_consistency(args.environment)
    environment = ev.read(args.environment)
    _environment_concretize(
        environment, use_repo=args.use_repo, force=args.force)


def _environment_concretize(environment, use_repo=False, force=False):
    """Function body separated out to aid in testing."""

    # Change global search paths
    repo = ev.prepare_repository(environment, use_repo=use_repo)
    ev.prepare_config_scope(environment)

    new_specs = environment.concretize(force=force)

    for spec in new_specs:
        for dep in spec.traverse():
            ev.dump_to_environment_repo(dep, repo)

    # Moves <env>/.env.new to <env>/.env
    ev.write(environment, repo)


# =============== Does not Modify Environment
def setup_install_parser(subparser):
    """install all concretized specs in an environment"""
    spack.cmd.install.add_common_arguments(subparser)
    add_use_repo_argument(subparser)


def environment_install(args):
    ev.check_consistency(args.environment)
    environment = ev.read(args.environment)
    ev.prepare_repository(environment, use_repo=args.use_repo)
    environment.install(args)


def setup_uninstall_parser(subparser):
    """uninstall packages from an environment"""
    spack.cmd.uninstall.add_common_arguments(subparser)


def environment_uninstall(args):
    ev.check_consistency(args.environment)
    environment = ev.read(args.environment)
    ev.prepare_repository(environment)
    environment.uninstall(args)


# =======================================


def setup_relocate_parser(subparser):
    """reconcretize environment with new OS and/or compiler"""
    subparser.add_argument('--compiler', help="Compiler spec to use")
    add_use_repo_argument(subparser)


def environment_relocate(args):
    environment = ev.read(args.environment)
    ev.prepare_repository(environment, use_repo=args.use_repo)
    environment.reset_os_and_compiler(compiler=args.compiler)
    ev.write(environment)


def setup_list_parser(subparser):
    """list specs in an environment"""
    arguments.add_common_arguments(
        subparser,
        ['recurse_dependencies', 'long', 'very_long', 'install_status'])


def environment_list(args):
    # TODO? option to list packages w/ multiple instances?
    environment = ev.read(args.environment)
    environment.list(
        sys.stdout, recurse_dependencies=args.recurse_dependencies,
        hashes=args.long or args.very_long,
        hashlen=None if args.very_long else 7,
        install_status=args.install_status)


def setup_stage_parser(subparser):
    """Download all source files for all packages in an environment"""
    add_use_repo_argument(subparser)


def environment_stage(args):
    environment = ev.read(args.environment)
    ev.prepare_repository(environment, use_repo=args.use_repo)
    for spec in environment.specs_by_hash.values():
        for dep in spec.traverse():
            dep.package.do_stage()


def setup_location_parser(subparser):
    """print the root directory of the environment"""


def environment_location(args):
    environment = ev.read(args.environment)
    print(environment.path)


@contextmanager
def redirect_stdout(ofname):
    """Redirects STDOUT to (by default) a file within the environment;
    or else a user-specified filename."""
    with open(ofname, 'w') as f:
        original = sys.stdout
        sys.stdout = f
        yield
        sys.stdout = original


def setup_loads_parser(subparser):
    """list modules for an installed environment '(see spack module loads)'"""
    spack.cmd.modules.add_loads_arguments(subparser)


def environment_loads(args):
    # Set the module types that have been selected
    module_types = args.module_type
    if module_types is None:
        # If no selection has been made select all of them
        module_types = ['tcl']

    module_types = list(set(module_types))

    environment = ev.read(args.environment)
    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False
    ofname = fs.join_path(environment.path, 'loads')
    with redirect_stdout(ofname):
        specs = environment._get_environment_specs(
            recurse_dependencies=recurse_dependencies)
        spack.cmd.module.loads(module_types, specs, args)

    print('To load this environment, type:')
    print('   source %s' % ofname)


def setup_upgrade_parser(subparser):
    """upgrade a dependency package in an environment to the latest version"""
    subparser.add_argument('dep_name', help='Dependency package to upgrade')
    subparser.add_argument('--dry-run', action='store_true', dest='dry_run',
                           help="Just show the updates that would take place")
    add_use_repo_argument(subparser)


def environment_upgrade(args):
    environment = ev.read(args.environment)
    repo = ev.prepare_repository(
        environment, use_repo=args.use_repo, remove=[args.dep_name])
    new_dep = environment.upgrade_dependency(args.dep_name, args.dry_run)
    if not args.dry_run and new_dep:
        ev.dump_to_environment_repo(new_dep, repo)
        ev.write(environment, repo)


def add_use_repo_argument(cmd_parser):
    cmd_parser.add_argument(
        '--use-env-repo', action='store_true', dest='use_repo',
        help='Use package definitions stored in the environment')


def setup_parser(subparser):
    subparser.add_argument('environment', help="name of environment")
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='environment_command')

    for name in subcommands:
        setup_parser_cmd_name = 'setup_%s_parser' % name
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(name, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def env(parser, args, **kwargs):
    """Look for a function called environment_<name> and call it."""
    function_name = 'environment_%s' % args.environment_command
    action = globals()[function_name]
    action(args)
