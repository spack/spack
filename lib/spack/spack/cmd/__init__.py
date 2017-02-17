##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import re
import sys

import llnl.util.tty as tty
from llnl.util.lang import *
from llnl.util.tty.colify import *
from llnl.util.tty.color import *

import spack
import spack.config
import spack.spec
import spack.store

#
# Settings for commands that modify configuration
#
# Commands that modify configuration by default modify the *highest*
# priority scope.
default_modify_scope = spack.config.highest_precedence_scope().name
# Commands that list configuration list *all* scopes by default.
default_list_scope = None

# cmd has a submodule called "list" so preserve the python list module
python_list = list

# Patterns to ignore in the commands directory when looking for commands.
ignore_files = r'^\.|^__init__.py$|^#'

SETUP_PARSER = "setup_parser"
DESCRIPTION = "description"

command_path = os.path.join(spack.lib_path, "spack", "cmd")

commands = []
for file in os.listdir(command_path):
    if file.endswith(".py") and not re.search(ignore_files, file):
        cmd = re.sub(r'.py$', '', file)
        commands.append(cmd)
commands.sort()


def remove_options(parser, *options):
    """Remove some options from a parser."""
    for option in options:
        for action in parser._actions:
            if vars(action)['option_strings'][0] == option:
                parser._handle_conflict_resolve(None, [(option, action)])
                break


def get_cmd_function_name(name):
    return name.replace("-", "_")


def get_module(name):
    """Imports the module for a particular command name and returns it."""
    module_name = "%s.%s" % (__name__, name)
    module = __import__(module_name,
                        fromlist=[name, SETUP_PARSER, DESCRIPTION],
                        level=0)

    attr_setdefault(module, SETUP_PARSER, lambda *args: None)  # null-op
    attr_setdefault(module, DESCRIPTION, "")

    fn_name = get_cmd_function_name(name)
    if not hasattr(module, fn_name):
        tty.die("Command module %s (%s) must define function '%s'." %
                (module.__name__, module.__file__, fn_name))

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

    try:
        specs = spack.spec.parse(args)
        for spec in specs:
            if concretize:
                spec.concretize()  # implies normalize
            elif normalize:
                spec.normalize()

        return specs

    except spack.parse.ParseError as e:
        tty.error(e.message, e.string, e.pos * " " + "^")
        sys.exit(1)

    except spack.spec.SpecError as e:
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
        return line_list[:max_num - 1] + ['...'] + line_list[-1:]
    else:
        return line_list


def disambiguate_spec(spec):
    matching_specs = spack.store.db.query(spec)
    if not matching_specs:
        tty.die("Spec '%s' matches no installed packages." % spec)

    elif len(matching_specs) > 1:
        args = ["%s matches multiple packages." % spec,
                "Matching packages:"]
        color = sys.stdout.isatty()
        args += [colorize("  @K{%s} " % s.dag_hash(7), color=color) +
                 s.format('$_$@$%@$=', color=color) for s in matching_specs]
        args += ["Use a more specific spec."]
        tty.die(*args)

    return matching_specs[0]


def gray_hash(spec, length):
    return colorize('@K{%s}' % spec.dag_hash(length))


def display_specs(specs, **kwargs):
    mode = kwargs.get('mode', 'short')
    hashes = kwargs.get('long', False)
    namespace = kwargs.get('namespace', False)
    flags = kwargs.get('show_flags', False)
    variants = kwargs.get('variants', False)

    hlen = 7
    if kwargs.get('very_long', False):
        hashes = True
        hlen = None

    nfmt = '.' if namespace else '_'
    ffmt = '$%+' if flags else ''
    vfmt = '$+' if variants else ''
    format_string = '$%s$@%s%s' % (nfmt, ffmt, vfmt)

    # Make a dict with specs keyed by architecture and compiler.
    index = index_by(specs, ('architecture', 'compiler'))

    # Traverse the index and print out each package
    for i, (architecture, compiler) in enumerate(sorted(index)):
        if i > 0:
            print

        header = "%s{%s} / %s{%s}" % (spack.spec.architecture_color,
                                      architecture, spack.spec.compiler_color,
                                      compiler)
        tty.hline(colorize(header), char='-')

        specs = index[(architecture, compiler)]
        specs.sort()

        abbreviated = [s.format(format_string, color=True) for s in specs]
        if mode == 'paths':
            # Print one spec per line along with prefix path
            width = max(len(s) for s in abbreviated)
            width += 2
            format = "    %%-%ds%%s" % width

            for abbrv, spec in zip(abbreviated, specs):
                prefix = gray_hash(spec, hlen) if hashes else ''
                print prefix + (format % (abbrv, spec.prefix))

        elif mode == 'deps':
            for spec in specs:
                print(spec.tree(
                    format=format_string,
                    color=True,
                    indent=4,
                    prefix=(lambda s: gray_hash(s, hlen)) if hashes else None))

        elif mode == 'short':
            # Print columns of output if not printing flags
            if not flags:

                def fmt(s):
                    string = ""
                    if hashes:
                        string += gray_hash(s, hlen) + ' '
                    string += s.format('$-%s$@%s' % (nfmt, vfmt), color=True)

                    return string

                colify(fmt(s) for s in specs)
            # Print one entry per line if including flags
            else:
                for spec in specs:
                    # Print the hash if necessary
                    hsh = gray_hash(spec, hlen) + ' ' if hashes else ''
                    print(hsh + spec.format(format_string, color=True) + '\n')

        else:
            raise ValueError(
                "Invalid mode for display_specs: %s. Must be one of (paths,"
                "deps, short)." % mode)
