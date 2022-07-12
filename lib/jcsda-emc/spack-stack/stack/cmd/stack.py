import os

from spack.extensions.stack.cmd.stack_cmds.create import (
    setup_create_parser,
    stack_create,
)
from spack.extensions.stack.cmd.stack_cmds.setup_meta_modules import (
    setup_meta_modules_parser,
    stack_setup_meta_modules,
)
from spack.extensions.stack.stack_paths import stack_path

description = "Create spack-stack environment"
section = "spack-stack"
level = "long"


default_env_name = 'default'
default_env_path = os.path.join(stack_path(), 'envs')
default_packages = os.path.join(stack_path(),
                                'configs', 'common', 'packages.yaml')
container_path = os.path.join(stack_path(), 'configs' 'containers')


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='stack_command')
    create_parser = sp.add_parser('create',
                                  help='Create spack-stack environment or container.')
    meta_modules_parser = sp.add_parser('setup-meta-modules',
                                        help='Create lmod/lua or tcl/tk meta-modules')
    setup_create_parser(create_parser)
    setup_meta_modules_parser(meta_modules_parser)


# Main command that calls subcommands
def stack(parser, args):
    if args.stack_command == 'create':
        stack_create(parser, args)
    if args.stack_command == 'setup-meta-modules':
        stack_setup_meta_modules(parser, args)
