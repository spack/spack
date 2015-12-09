##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import re
import sys

import llnl.util.tty as tty
from llnl.util.lang import attr_setdefault

import spack
import spack.spec

# cmd has a submodule called "list" so preserve the python list module
python_list = list

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

    attr_setdefault(module, SETUP_PARSER, lambda *args: None) # null-op
    attr_setdefault(module, DESCRIPTION, "")

    fn_name = get_cmd_function_name(name)
    if not hasattr(module, fn_name):
        tty.die("Command module %s (%s) must define function '%s'."
                % (module.__name__, module.__file__, fn_name))

    return module


def get_command(name):
    """Imports the command's function from a module and returns it."""
    return getattr(get_module(name), get_cmd_function_name(name))


def parse_specs(args, **kwargs):
    """Convenience function for parsing arguments from specs.  Handles common
       exceptions and dies if there are errors.
    """
    concretize = kwargs.get('concretize', False)
    normalize = kwargs.get('normalize', False)

    if isinstance(args, (python_list, tuple)):
        args = " ".join(args)

    try:
        specs = spack.spec.parse(args)
        for spec in specs:
            if concretize:
                spec.concretize() # implies normalize
            elif normalize:
                spec.normalize()

        return specs

    except spack.parse.ParseError, e:
        tty.error(e.message, e.string, e.pos * " " + "^")
        sys.exit(1)

    except spack.spec.SpecError, e:
        tty.error(e.message)
        sys.exit(1)


def elide_list(line_list, max_num=10):
    """Takes a long list and limits it to a smaller number of elements,
       replacing intervening elements with '...'.  For example::

           elide_list([1,2,3,4,5,6], 4)

       gives::

           [1, 2, 3, '...', 6]
    """
    if len(line_list) > max_num:
        return line_list[:max_num-1] + ['...'] + line_list[-1:]
    else:
        return line_list


def disambiguate_spec(spec):
    matching_specs = spack.installed_db.query(spec)
    if not matching_specs:
        tty.die("Spec '%s' matches no installed packages." % spec)

    elif len(matching_specs) > 1:
        args =  ["%s matches multiple packages." % spec,
                 "Matching packages:"]
        args += ["  " + str(s) for s in matching_specs]
        args += ["Use a more specific spec."]
        tty.die(*args)

    return matching_specs[0]
