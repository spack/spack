##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from __future__ import print_function

import os
import re

import llnl.util.tty as tty
from llnl.util.lang import attr_setdefault, index_by
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize
from llnl.util.filesystem import working_dir

import spack.config
import spack.paths
import spack.spec
import spack.store
from spack.error import SpackError


# cmd has a submodule called "list" so preserve the python list module
python_list = list

# Patterns to ignore in the commands directory when looking for commands.
ignore_files = r'^\.|^__init__.py$|^#'

SETUP_PARSER = "setup_parser"
DESCRIPTION = "description"

#: Names of all commands
all_commands = []


def python_name(cmd_name):
    """Convert ``-`` to ``_`` in command name, to make a valid identifier."""
    return cmd_name.replace("-", "_")


def cmd_name(python_name):
    """Convert module name (with ``_``) to command name (with ``-``)."""
    return python_name.replace('_', '-')


#: global, cached list of all commands -- access through all_commands()
_all_commands = None


def all_commands():
    """Get a sorted list of all spack commands.

    This will list the lib/spack/spack/cmd directory and find the
    commands there to construct the list.  It does not actually import
    the python files -- just gets the names.
    """
    global _all_commands
    if _all_commands is None:
        _all_commands = []
        for file in os.listdir(spack.paths.command_path):
            if file.endswith(".py") and not re.search(ignore_files, file):
                cmd = re.sub(r'.py$', '', file)
                _all_commands.append(cmd_name(cmd))
        _all_commands.sort()
    return _all_commands


def remove_options(parser, *options):
    """Remove some options from a parser."""
    for option in options:
        for action in parser._actions:
            if vars(action)['option_strings'][0] == option:
                parser._handle_conflict_resolve(None, [(option, action)])
                break


def get_module(cmd_name):
    """Imports the module for a particular command name and returns it.

    Args:
        cmd_name (str): name of the command for which to get a module
            (contains ``-``, not ``_``).
    """
    pname = python_name(cmd_name)
    module_name = "%s.%s" % (__name__, pname)
    module = __import__(module_name,
                        fromlist=[pname, SETUP_PARSER, DESCRIPTION],
                        level=0)

    attr_setdefault(module, SETUP_PARSER, lambda *args: None)  # null-op
    attr_setdefault(module, DESCRIPTION, "")

    if not hasattr(module, pname):
        tty.die("Command module %s (%s) must define function '%s'." %
                (module.__name__, module.__file__, pname))

    return module


def get_command(cmd_name):
    """Imports the command's function from a module and returns it.

    Args:
        cmd_name (str): name of the command for which to get a module
            (contains ``-``, not ``_``).
    """
    pname = python_name(cmd_name)
    return getattr(get_module(pname), pname)


def parse_specs(args, **kwargs):
    """Convenience function for parsing arguments from specs.  Handles common
       exceptions and dies if there are errors.
    """
    concretize = kwargs.get('concretize', False)
    normalize = kwargs.get('normalize', False)
    tests = kwargs.get('tests', False)

    try:
        specs = spack.spec.parse(args)
        for spec in specs:
            if concretize:
                spec.concretize(tests=tests)  # implies normalize
            elif normalize:
                spec.normalize(tests=tests)

        return specs

    except spack.spec.SpecParseError as e:
        msg = e.message + "\n" + str(e.string) + "\n"
        msg += (e.pos + 2) * " " + "^"
        raise SpackError(msg)

    except spack.spec.SpecError as e:

        msg = e.message
        if e.long_message:
            msg += e.long_message

        raise SpackError(msg)


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
        args += [colorize("  @K{%s} " % s.dag_hash(7)) +
                 s.cformat('$_$@$%@$=') for s in matching_specs]
        args += ["Use a more specific spec."]
        tty.die(*args)

    return matching_specs[0]


def gray_hash(spec, length):
    return colorize('@K{%s}' % spec.dag_hash(length))


def display_specs(specs, args=None, **kwargs):
    """Display human readable specs with customizable formatting.

    Prints the supplied specs to the screen, formatted according to the
    arguments provided.

    Specs are grouped by architecture and compiler, and columnized if
    possible.  There are three possible "modes":

      * ``short`` (default): short specs with name and version, columnized
      * ``paths``: Two columns: one for specs, one for paths
      * ``deps``: Dependency-tree style, like ``spack spec``; can get long

    Options can add more information to the default display. Options can
    be provided either as keyword arguments or as an argparse namespace.
    Keyword arguments take precedence over settings in the argparse
    namespace.

    Args:
        specs (list of spack.spec.Spec): the specs to display
        args (optional argparse.Namespace): namespace containing
            formatting arguments

    Keyword Args:
        mode (str): Either 'short', 'paths', or 'deps'
        long (bool): Display short hashes with specs
        very_long (bool): Display full hashes with specs (supersedes ``long``)
        namespace (bool): Print namespaces along with names
        show_flags (bool): Show compiler flags with specs
        variants (bool): Show variants with specs

    """
    def get_arg(name, default=None):
        """Prefer kwargs, then args, then default."""
        if name in kwargs:
            return kwargs.get(name)
        elif args is not None:
            return getattr(args, name, default)
        else:
            return default

    mode      = get_arg('mode', 'short')
    hashes    = get_arg('long', False)
    namespace = get_arg('namespace', False)
    flags     = get_arg('show_flags', False)
    full_compiler = get_arg('show_full_compiler', False)
    variants  = get_arg('variants', False)

    hlen = 7
    if get_arg('very_long', False):
        hashes = True
        hlen = None

    nfmt = '.' if namespace else '_'
    ffmt = ''
    if full_compiler or flags:
        ffmt += '$%'
        if full_compiler:
            ffmt += '@'
        ffmt += '+'
    vfmt = '$+' if variants else ''
    format_string = '$%s$@%s%s' % (nfmt, ffmt, vfmt)

    # Make a dict with specs keyed by architecture and compiler.
    index = index_by(specs, ('architecture', 'compiler'))

    # Traverse the index and print out each package
    for i, (architecture, compiler) in enumerate(sorted(index)):
        if i > 0:
            print()

        header = "%s{%s} / %s{%s}" % (spack.spec.architecture_color,
                                      architecture, spack.spec.compiler_color,
                                      compiler)
        # Sometimes we want to display specs that are not yet concretized.
        # If they don't have a compiler / architecture attached to them,
        # then skip the header
        if architecture is not None or compiler is not None:
            tty.hline(colorize(header), char='-')

        specs = index[(architecture, compiler)]
        specs.sort()

        abbreviated = [s.cformat(format_string) for s in specs]
        if mode == 'paths':
            # Print one spec per line along with prefix path
            width = max(len(s) for s in abbreviated)
            width += 2
            format = "    %%-%ds%%s" % width

            for abbrv, spec in zip(abbreviated, specs):
                prefix = gray_hash(spec, hlen) if hashes else ''
                print(prefix + (format % (abbrv, spec.prefix)))

        elif mode == 'deps':
            for spec in specs:
                print(spec.tree(
                    format=format_string,
                    indent=4,
                    prefix=(lambda s: gray_hash(s, hlen)) if hashes else None))

        elif mode == 'short':
            # Print columns of output if not printing flags
            if not flags and not full_compiler:

                def fmt(s):
                    string = ""
                    if hashes:
                        string += gray_hash(s, hlen) + ' '
                    string += s.cformat('$-%s$@%s' % (nfmt, vfmt))

                    return string

                colify(fmt(s) for s in specs)
            # Print one entry per line if including flags
            else:
                for spec in specs:
                    # Print the hash if necessary
                    hsh = gray_hash(spec, hlen) + ' ' if hashes else ''
                    print(hsh + spec.cformat(format_string) + '\n')

        else:
            raise ValueError(
                "Invalid mode for display_specs: %s. Must be one of (paths,"
                "deps, short)." % mode)


def spack_is_git_repo():
    """Ensure that this instance of Spack is a git clone."""
    with working_dir(spack.paths.prefix):
        return os.path.isdir('.git')
