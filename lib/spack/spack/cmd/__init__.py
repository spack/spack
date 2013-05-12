import os
import re
import sys

import spack
import spack.spec
import spack.tty as tty
import spack.attr as attr

# Patterns to ignore in the commands directory when looking for commands.
ignore_files = r'^\.|^__init__.py$|^#'

SETUP_PARSER = "setup_parser"
DESCRIPTION  = "description"

command_path = os.path.join(spack.lib_path, "spack", "cmd")

commands = []
for file in os.listdir(command_path):
    if file.endswith(".py") and not re.search(ignore_files, file):
        cmd = re.sub(r'.py$', '', file)
        commands.append(cmd)
commands.sort()


def get_cmd_function_name(name):
    return name.replace("-", "_")


def get_module(name):
    """Imports the module for a particular command name and returns it."""
    module_name = "%s.%s" % (__name__, name)
    module = __import__(
        module_name, fromlist=[name, SETUP_PARSER, DESCRIPTION],
        level=0)

    attr.setdefault(module, SETUP_PARSER, lambda *args: None) # null-op
    attr.setdefault(module, DESCRIPTION, "")

    fn_name = get_cmd_function_name(name)
    if not hasattr(module, fn_name):
        tty.die("Command module %s (%s) must define function '%s'."
                % (module.__name__, module.__file__, fn_name))

    return module


def get_command(name):
    """Imports the command's function from a module and returns it."""
    return getattr(get_module(name), get_cmd_function_name(name))


def parse_specs(args):
    """Convenience function for parsing arguments from specs.  Handles common
       exceptions and dies if there are errors.
    """
    if type(args) == list:
        args = " ".join(args)

    try:
        return spack.spec.parse(" ".join(args))

    except spack.parse.ParseError, e:
        e.print_error(sys.stdout)
        sys.exit(1)

    except spack.spec.SpecError, e:
        tty.error(e.message)
        sys.exit(1)
