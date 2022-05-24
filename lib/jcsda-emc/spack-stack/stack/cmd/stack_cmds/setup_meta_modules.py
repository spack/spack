import logging
import spack.cmd.common.arguments
import spack.cmd.modules
from spack.extensions.stack.meta_modules import setup_meta_modules
import llnl.util.tty as tty

description = "Create meta-modules"
section = "spack-stack"
level = "long"


# Add potential arguments to setup-meta-modules
def setup_meta_modules_parser(subparser):
    pass


def stack_setup_meta_modules(parser, args):
        setup_meta_modules()
