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
import shutil
import sys

import llnl.util.tty as tty
import spack.cmd
from llnl.util.filesystem import mkdirp
from spack.modules import module_types
from spack.util.string import *

description ="Manipulate modules and dotkits."


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='module_command')

    refresh_parser = sp.add_parser('refresh', help='Regenerate all module files.')

    find_parser = sp.add_parser('find', help='Find module files for packages.')
    find_parser.add_argument(
        'module_type', help="Type of module to find file for. [" + '|'.join(module_types) + "]")
    find_parser.add_argument(
        '-r', '--dependencies', action='store_true', dest='recurse_dependencies',
        help='Recursively traverse dependencies for modules to load.')

    find_parser.add_argument(
        '-s', '--shell', action='store_true', dest='shell',
        help='Generate shell script (instead of input for module command)')

    find_parser.add_argument('spec', nargs='+', help='spec to find a module file for.')


    

def module_find(mtype, flags, spec_array):
    """Look at all installed packages and see if the spec provided
       matches any.  If it does, check whether there is a module file
       of type <mtype> there, and print out the name that the user
       should type to use that package's module.
    """

    # --------------------------------------
    def _find_modules(spec, modules_list):
        """Finds all modules and sub-modules for a spec"""
        if str(spec.version) == 'system':
            # No Spack module for system-installed packages
            return

        if flags.recurse_dependencies:
            for dep in spec.dependencies.values():
                _find_modules(dep, modules_list)

        mod = module_types[mtype](spec)
        if not os.path.isfile(mod.file_name):
            tty.die("No %s module is installed for %s" % (mtype, spec))
        modules_list.append((spec, mod))


    # --------------------------------------

    if mtype not in module_types:
        tty.die("Invalid module type: '%s'.  Options are %s" % (mtype, comma_or(module_types)))

    raw_specs = spack.cmd.parse_specs(spec_array)
    modules = set()    # Modules we will load
    seen = set()
    for raw_spec in raw_specs:

        # ----------- Make sure the spec only resolves to ONE thing
        specs = spack.installed_db.query(raw_spec)
        if len(specs) == 0:
            tty.die("No installed packages match spec %s" % raw_spec)

        if len(specs) > 1:
            tty.error("Multiple matches for spec %s.  Choose one:" % spec)
            for s in specs:
                sys.stderr.write(s.tree(color=True))
            sys.exit(1)
        spec = specs[0]

        # ----------- Chase down modules for it and all its dependencies
        modules_dups = list()
        _find_modules(spec, modules_dups)

        # Remove duplicates while keeping order
        modules_unique = list()
        for spec,mod in modules_dups:
            if mod.use_name not in seen:
                modules_unique.append((spec,mod))
                seen.add(mod.use_name)

        # Output...
        if flags.shell:
            module_cmd = {'tcl' : 'module load', 'dotkit' : 'dotkit use'}[mtype]
        for spec,mod in modules_unique:
            if flags.shell:
                print '# %s' % spec.format()
                print '%s %s' % (module_cmd, mod.use_name)
            else:
                print mod.use_name

def module_refresh():
    """Regenerate all module files for installed packages known to
       spack (some packages may no longer exist)."""
    specs = [s for s in spack.installed_db.query(installed=True, known=True)]

    for name, cls in module_types.items():
        tty.msg("Regenerating %s module files." % name)
        if os.path.isdir(cls.path):
            shutil.rmtree(cls.path, ignore_errors=False)
        mkdirp(cls.path)
        for spec in specs:
            tty.debug("   Writing file for %s" % spec)
            cls(spec).write()


def module(parser, args):
    if args.module_command == 'refresh':
        module_refresh()

    elif args.module_command == 'find':
        module_find(args.module_type, args, args.spec)
