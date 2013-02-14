import os
import re

import spack
import spack.tty as tty

SETUP_PARSER = "setup_parser"
command_path = os.path.join(spack.lib_path, "spack", "cmd")

commands = []
for file in os.listdir(command_path):
    if file.endswith(".py") and not file == "__init__.py":
        cmd = re.sub(r'.py$', '', file)
        commands.append(cmd)
commands.sort()

def null_op(*args):
    pass


def get_module(name):
    """Imports the module for a particular command name and returns it."""
    module_name = "%s.%s" % (__name__, name)
    module = __import__(module_name, fromlist=[name, SETUP_PARSER], level=0)
    module.setup_parser = getattr(module, SETUP_PARSER, null_op)

    if not hasattr(module, name):
        tty.die("Command module %s (%s) must define function '%s'."
                % (module.__name__, module.__file__, name))

    return module


def get_command(name):
    """Imports the command's function from a module and returns it."""
    return getattr(get_module(name), name)
