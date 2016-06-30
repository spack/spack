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
from __future__ import print_function
import os
import shutil
import sys
import collections

import llnl.util.tty as tty
import spack.cmd
from llnl.util.filesystem import mkdirp
from spack.modules import module_types
from spack.util.string import *

from spack.cmd.uninstall import ask_for_confirmation

description = "Manipulate module files"


def _add_common_arguments(subparser):
    type_help = 'Type of module files'
    subparser.add_argument('--module-type', help=type_help, required=True, choices=module_types)
    constraint_help = 'Optional constraint to select a subset of installed packages'
    subparser.add_argument('constraint', nargs='*', help=constraint_help)


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='module_command')
    # spack module refresh
    refresh_parser = sp.add_parser('refresh', help='Regenerate all module files.')
    refresh_parser.add_argument('--delete-tree', help='Delete the module file tree before refresh', action='store_true')
    _add_common_arguments(refresh_parser)

    # spack module find
    find_parser = sp.add_parser('find', help='Find module files for packages.')
    find_parser.add_argument(
        '-r', '--dependencies', action='store_true',
        dest='recurse_dependencies',
        help='Recursively traverse dependencies for modules to load.')

    find_parser.add_argument(
        '-s', '--shell', action='store_true', dest='shell',
        help='Generate shell script (instead of input for module command)')

    find_parser.add_argument(
        '-p', '--prefix', dest='prefix',
        help='Prepend to module names when issuing module load commands')
    _add_common_arguments(find_parser)


class MultipleMatches(Exception):
    pass


class NoMatch(Exception):
    pass


def module_find(mtype, specs, args):
    """
    Look at all installed packages and see if the spec provided
    matches any.  If it does, check whether there is a module file
    of type <mtype> there, and print out the name that the user
    should type to use that package's module.
    """
    if len(specs) == 0:
        raise NoMatch()

    if len(specs) > 1:
        raise MultipleMatches()

    spec = specs.pop()
    if not args.recurse_dependencies:
        mod = module_types[mtype](spec)
        if not os.path.isfile(mod.file_name):
            tty.die("No %s module is installed for %s" % (mtype, spec))

        print(mod.use_name)
    else:

        def _find_modules(spec, modules_list):
            """Finds all modules and sub-modules for a spec"""
            if str(spec.version) == 'system':
                # No Spack module for system-installed packages
                return

            if args.recurse_dependencies:
                for dep in spec.dependencies.values():
                    _find_modules(dep, modules_list)

            mod = module_types[mtype](spec)
            if not os.path.isfile(mod.file_name):
                tty.die("No %s module is installed for %s" % (mtype, spec))
            modules_list.append((spec, mod))
        # --------------------------------------

        modules = set()    # Modules we will load
        seen = set()

        # ----------- Chase down modules for it and all its dependencies
        modules_dups = list()
        _find_modules(spec, modules_dups)

        # Remove duplicates while keeping order
        modules_unique = list()
        for spec, mod in modules_dups:
            if mod.use_name not in seen:
                modules_unique.append((spec,mod))
                seen.add(mod.use_name)

        # Output...
        if args.shell:
            module_cmd = {'tcl': 'module load', 'dotkit': 'dotkit use'}[mtype]
        for spec, mod in modules_unique:
            if args.shell:
                print('# %s' % spec.format())
                print('%s %s%s' % (module_cmd, args.prefix, mod.use_name))
            else:
                print(mod.use_name)


def module_refresh(name, specs, args):
    """
    Regenerate all module files for installed packages known to
    spack (some packages may no longer exist).
    """
    # Prompt a message to the user about what is going to change
    if not specs:
        tty.msg('No package matches your query')
        return

    tty.msg('You are about to regenerate the {name} module files for the following specs:\n'.format(name=name))
    for s in specs:
        print(s.format(color=True))
    print('')
    ask_for_confirmation('Do you want to proceed ? ')

    cls = module_types[name]

    # Detect name clashes
    writers = [cls(spec) for spec in specs]
    file2writer = collections.defaultdict(list)
    for item in writers:
        file2writer[item.file_name].append(item)

    if len(file2writer) != len(writers):
        message = 'Name clashes detected in module files:\n'
        for filename, writer_list in file2writer.items():
            if len(writer_list) > 1:
                message += '\nfile : {0}\n'.format(filename)
                for x in writer_list:
                    message += 'spec : {0}\n'.format(x.spec.format(color=True))
        tty.error(message)
        tty.error('Operation aborted')
        raise SystemExit(1)

    # Proceed regenerating module files
    tty.msg('Regenerating {name} module files'.format(name=name))
    if os.path.isdir(cls.path) and args.delete_tree:
        shutil.rmtree(cls.path, ignore_errors=False)
    mkdirp(cls.path)
    for x in writers:
        x.write(overwrite=True)

# Qualifiers to be used when querying the db for specs
constraint_qualifiers = {
    'refresh': {
        'installed': True,
        'known': True
    },
    'find': {
    }
}

# Dictionary of callbacks based on the value of module_command
callbacks = {
    'refresh': module_refresh,
    'find': module_find
}


def module(parser, args):
    module_type = args.module_type
    # Query specs from command line
    qualifiers = constraint_qualifiers[args.module_command]
    specs = [s for s in spack.installed_db.query(**qualifiers)]
    constraint = ' '.join(args.constraint)
    if constraint:
        specs = [x for x in specs if x.satisfies(constraint, strict=True)]
    # Call the appropriate function
    try:
        callbacks[args.module_command](module_type, specs, args)
    except MultipleMatches:
        message = 'the constraint \'{query}\' matches multiple packages, and this is not allowed in this context'
        tty.error(message.format(query=constraint))
        for s in specs:
            sys.stderr.write(s.format(color=True) + '\n')
        raise SystemExit(1)
    except NoMatch:
        message = 'the constraint \'{query}\' match no package, and this is not allowed in this context'
        tty.die(message.format(query=constraint))
