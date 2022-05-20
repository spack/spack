import spack.cmd.common.arguments
import spack.cmd.modules
import os
import logging
from spack.extensions.stack.stack_env import StackEnv, stack_path, app_path
from spack.extensions.stack.container_env import StackContainer
import shutil
import llnl.util.tty as tty
import spack.util.spack_yaml as syaml

description = "Create spack-stack environment (env or container)"
section = "spack-stack-env"
level = "long"

default_env_name = 'default'
default_env_path = stack_path('envs')
default_packages = stack_path('configs', 'common', 'packages.yaml')


def site_help():
    _, site_dirs, _ = next(os.walk(stack_path('configs', 'sites')))
    help_string = 'Pre-configured platform, or "default" for an empty site.yaml.' + os.linesep
    help_string += 'Defaults to "default" if no arg is given' + os.linesep
    help_string += 'Available options are: ' + os.linesep
    for site in site_dirs:
        help_string += '\t' + site + os.linesep
    return help_string


def app_help():
    _, app_dirs, _ = next(os.walk(stack_path('configs', 'apps')))
    help_string = 'Application environment to build.' + os.linesep
    help_string += 'Available options are: ' + os.linesep
    for app in app_dirs:
        help_string += '\t' + app + os.linesep
    return help_string


def container_config_help():
    _, _, container_configs = next(os.walk(stack_path('configs', 'containers')))
    help_string = 'Pre-configured container.' + os.linesep
    help_string += 'Available options are: ' + os.linesep
    for config in container_configs:
        help_string += '\t' + config.rstrip('.yaml') + os.linesep
    return help_string


def spec_help():
    help_string = 'Any valid spack spec, e.g. "wget" or "jedi-ufs-bundle-env".' + os.linesep
    return help_string


def setup_common_parser_args(subparser):
    """Shared CLI args for container and env subcommands"""
    subparser.add_argument(
        '--app', type=str, required=False, dest='app', default='empty',
        help=app_help()
    )

    subparser.add_argument(
        '--name', type=str, required=False, default=None,
        help='Environment name, defaults to {}.'.format(default_env_name) +
        ' Environment will be in <prefix>/<name>'
    )

    subparser.add_argument(
        '--dir', type=str, required=False, default=default_env_path,
        help='Environment will be placed in <dir>/<name>/contents.'
        ' Default is {}.'.format(default_env_path)
    )

    subparser.add_argument(
        '--overwrite', action='store_true', required=False, default=False,
        help='Overwrite existing environment if it exists.'
        ' Warning this is dangerous.'
    )

    subparser.add_argument(
        '--packages', type=str, required=False, default=default_packages,
        help='Base packages.yaml.'
        ' Defaults to {}'.format(default_packages)
    )


def setup_container_parser(subparser):
    subparser.add_argument(
        'container', help=container_config_help())

    setup_common_parser_args(subparser)


def setup_env_parser(subparser):
    """ create env specific parsing options"""
    setup_common_parser_args(subparser)
    subparser.add_argument(
        '--site', type=str, required=False, default='default',
        help=site_help()
    )

    subparser.add_argument(
        '--prefix', type=str, required=False, default=None,
        help='Install prefix.'
    )

    subparser.add_argument(
        '--envs-file', type=str, required=False, default=None,
        help='Create environments from envs.yaml file.'
        ' Other command-line options will be ignored'
    )


def setup_create_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='env_type')

    env_parser = sp.add_parser('env', help='Create local Spack environment')
    container_parser = sp.add_parser('container', help='Create container.')

    setup_env_parser(env_parser)

    setup_container_parser(container_parser)


def container_create(args):
    """Create pre-configured container"""

    container = StackContainer(args.container, args.app, args.name,
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
    dict['app'] = args.app
    dict['name'] = args.name
    dict['envs_file'] = args.envs_file
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
            tty.msg('Env {} exists. Overwriting...'.format(env_dir))
            shutil.rmtree(env_dir)
        else:
            raise Exception('Env: {} already exists'.format(env_dir))

    if args.envs_file:
        logging.debug('Creating envs from envs_file')
        with open(args.envs_file, 'r') as f:
            site_envs = syaml.load_config(stream=f)

        envs = site_envs['envs']
        for env in envs:
            stack_env = StackEnv(**env['env'])
            stack_env.write()
    else:
        logging.debug('Creating envs from command-line args')
        stack_env = StackEnv(**stack_settings)
        stack_env.write()
        tty.msg('Created env {}'.format(env_dir))


def stack_create(parser, args):
    if args.env_type == 'env':
        env_create(args)
    elif args.env_type == 'container':
        container_create(args)
