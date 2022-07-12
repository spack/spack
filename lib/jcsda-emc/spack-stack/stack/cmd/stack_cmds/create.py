import logging
import os
import shutil
from sys import platform

import llnl.util.tty as tty

from spack.extensions.stack.container_env import StackContainer
from spack.extensions.stack.stack_env import StackEnv, stack_path

description = "Create spack-stack environment (environment or container)"
section = "spack-stack"
level = "long"

default_env_name = 'default'
default_env_path = stack_path('envs')


def default_site():
    if platform == "linux" or platform == "linux2":
        return "linux.default"
    elif platform == "darwin":
        return "macos.default"


def site_help():
    _, site_dirs, _ = next(os.walk(stack_path('configs', 'sites')))
    help_string = 'Pre-configured platform, or "default" for an empty site.yaml.'
    help_string += os.linesep
    help_string += 'Defaults to "default" if no arg is given'
    help_string += os.linesep
    help_string += 'Available options are: '
    help_string += os.linesep
    for site in site_dirs:
        help_string += '\t' + site + os.linesep
    return help_string


def template_help():
    _, template_dirs, _ = next(os.walk(stack_path('configs', 'templates')))
    help_string = 'Environment template' + os.linesep
    help_string += 'Default to an empty spack.yaml' + os.linesep
    help_string += 'Available options are: ' + os.linesep
    for template in template_dirs:
        help_string += '\t' + template + os.linesep
    return help_string


def container_config_help():
    _, _, container_configs = next(os.walk(stack_path('configs', 'containers')))
    help_string = 'Pre-configured container.' + os.linesep
    help_string += 'Available options are: ' + os.linesep
    for config in container_configs:
        help_string += '\t' + config.rstrip('.yaml') + os.linesep
    return help_string


def setup_common_parser_args(subparser):
    """Shared CLI args for container and environment subcommands"""
    subparser.add_argument(
        '--template', type=str, required=False, dest='template', default='empty',
        help=template_help()
    )

    subparser.add_argument(
        '--name', type=str, required=False, default=None,
        help='Environment name, defaults to "{}".'.format(default_env_name)
    )

    subparser.add_argument(
        '--dir', type=str, required=False, default=default_env_path,
        help='Environment will be placed in <dir>/<name>/.'
        ' Default is {}/<name>/.'.format(default_env_path)
    )

    subparser.add_argument(
        '--overwrite', action='store_true', required=False, default=False,
        help='Overwrite existing environment if it exists.'
        ' Warning this is dangerous.'
    )

    subparser.add_argument(
        '--packages', type=str, required=False, default=None,
        help='Base packages.yaml, use to override common packages.yaml.'
    )


def setup_ctr_parser(subparser):
    """ create container-specific parsing options"""
    subparser.add_argument(
        'container', help=container_config_help())

    setup_common_parser_args(subparser)


def setup_env_parser(subparser):
    """ create environment-specific parsing options"""
    setup_common_parser_args(subparser)
    subparser.add_argument(
        '--site', type=str, required=False, default=default_site(),
        help=site_help()
    )

    subparser.add_argument(
        '--prefix', type=str, required=False, default=None,
        help="""Install prefix for spack packages and
                modules (not the spack environment)."""
    )


def setup_create_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='env_type')

    env_parser = sp.add_parser('env', help='Create local Spack environment')
    ctr_parser = sp.add_parser('ctr', help='Create container.')

    setup_env_parser(env_parser)

    setup_ctr_parser(ctr_parser)


def container_create(args):
    """Create pre-configured container"""

    container = StackContainer(args.container, args.template, args.name,
                               args.dir, args.packages)

    env_dir = container.env_dir
    if os.path.exists(env_dir):
        if args.overwrite:
            tty.msg('Env {} exists. Overwriting...'.format(env_dir))
            shutil.rmtree(env_dir)
        else:
            raise Exception('Env: {} already exists'.format(env_dir))

    container.write()
    tty.msg('Created container {}'.format(env_dir))


def dict_from_args(args):
    dict = {}
    dict['site'] = args.site
    dict['template'] = args.template
    dict['name'] = args.name
    dict['install_prefix'] = args.prefix
    dict['base_packages'] = args.packages
    dict['dir'] = args.dir

    return dict


def env_create(args):
    """Create pre-configured Spack environment.

    Args: args

    Returns:

    """

    stack_settings = dict_from_args(args)
    stack_env = StackEnv(**stack_settings)

    env_dir = stack_env.env_dir()
    if os.path.exists(env_dir):
        if args.overwrite:
            tty.msg('Environment {} exists. Overwriting...'.format(env_dir))
            shutil.rmtree(env_dir)
        else:
            raise Exception('Environment: {} already exists'.format(env_dir))

    logging.debug('Creating environment from command-line args')
    stack_env = StackEnv(**stack_settings)
    stack_env.write()
    tty.msg('Created environment {}'.format(env_dir))


def stack_create(parser, args):
    if args.env_type == 'env':
        env_create(args)
    elif args.env_type == 'ctr':
        container_create(args)
