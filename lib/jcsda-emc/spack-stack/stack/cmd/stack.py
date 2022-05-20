import os
import spack.cmd
import spack
import logging
from spack.extensions.stack.stack_env import stack_path
from spack.extensions.stack.cmd.stack_cmds.create import setup_create_parser, stack_create

description = "Create spack-stack environment"
section = "spack-stack-env"
level = "long"


default_env_name = 'default'
default_env_path = os.path.join(stack_path(), 'envs')
default_packages = os.path.join(stack_path(),
                                'configs', 'common', 'packages.yaml')
container_path = os.path.join(stack_path(), 'configs' 'containers')


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='stack_command')
    create_parser = sp.add_parser('create',
                                  help='Create spack-stack env or container.')
    setup_create_parser(create_parser)


# Main command that calls subcommands
def stack(parser, args):
    if args.stack_command == 'create':
        stack_create(parser, args)
