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
import os
from datetime import datetime

import argparse
import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.cmd
import spack.concretize
import spack.config
import spack.mirror
import spack.repo
import spack.cmd.common.arguments as arguments
from spack.spec import Spec
from spack.error import SpackError
from spack.util.spack_yaml import syaml_dict

description = "manage mirrors"
section = "config"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['no_checksum'])

    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='mirror_command')

    # Create
    create_parser = sp.add_parser('create', help=mirror_create.__doc__)
    create_parser.add_argument('-d', '--directory', default=None,
                               help="directory in which to create mirror")
    create_parser.add_argument(
        'specs', nargs=argparse.REMAINDER,
        help="specs of packages to put in mirror")
    create_parser.add_argument(
        '-f', '--file', help="file with specs of packages to put in mirror")
    create_parser.add_argument(
        '-D', '--dependencies', action='store_true',
        help="also fetch all dependencies")
    create_parser.add_argument(
        '-o', '--one-version-per-spec', action='store_const',
        const=1, default=0,
        help="only fetch one 'preferred' version per spec, not all known")

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # Add
    add_parser = sp.add_parser('add', help=mirror_add.__doc__)
    add_parser.add_argument('name', help="mnemonic name for mirror")
    add_parser.add_argument(
        'url', help="url of mirror directory from 'spack mirror create'")
    add_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify")

    # Remove
    remove_parser = sp.add_parser('remove', aliases=['rm'],
                                  help=mirror_remove.__doc__)
    remove_parser.add_argument('name')
    remove_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify")

    # List
    list_parser = sp.add_parser('list', help=mirror_list.__doc__)
    list_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_list_scope(),
        help="configuration scope to read from")


def mirror_add(args):
    """Add a mirror to Spack."""
    url = args.url
    if url.startswith('/'):
        url = 'file://' + url

    mirrors = spack.config.get('mirrors', scope=args.scope)
    if not mirrors:
        mirrors = syaml_dict()

    for name, u in mirrors.items():
        if name == args.name:
            tty.die("Mirror with name %s already exists." % name)
        if u == url:
            tty.die("Mirror with url %s already exists." % url)
        # should only be one item per mirror dict.

    items = [(n, u) for n, u in mirrors.items()]
    items.insert(0, (args.name, url))
    mirrors = syaml_dict(items)
    spack.config.set('mirrors', mirrors, scope=args.scope)


def mirror_remove(args):
    """Remove a mirror by name."""
    name = args.name

    mirrors = spack.config.get('mirrors', scope=args.scope)
    if not mirrors:
        mirrors = syaml_dict()

    if name not in mirrors:
        tty.die("No mirror with name %s" % name)

    old_value = mirrors.pop(name)
    spack.config.set('mirrors', mirrors, scope=args.scope)
    tty.msg("Removed mirror %s with url %s" % (name, old_value))


def mirror_list(args):
    """Print out available mirrors to the console."""
    mirrors = spack.config.get('mirrors', scope=args.scope)
    if not mirrors:
        tty.msg("No mirrors configured.")
        return

    max_len = max(len(n) for n in mirrors.keys())
    fmt = "%%-%ds%%s" % (max_len + 4)

    for name in mirrors:
        print(fmt % (name, mirrors[name]))


def _read_specs_from_file(filename):
    specs = []
    with open(filename, "r") as stream:
        for i, string in enumerate(stream):
            try:
                s = Spec(string)
                s.package
                specs.append(s)
            except SpackError as e:
                tty.die("Parse error in %s, line %d:" % (filename, i + 1),
                        ">>> " + string, str(e))
    return specs


def mirror_create(args):
    """Create a directory to be used as a spack mirror, and fill it with
       package archives."""
    # try to parse specs from the command line first.
    with spack.concretize.concretizer.disable_compiler_existence_check():
        specs = spack.cmd.parse_specs(args.specs, concretize=True)

        # If there is a file, parse each line as a spec and add it to the list.
        if args.file:
            if specs:
                tty.die("Cannot pass specs on the command line with --file.")
            specs = _read_specs_from_file(args.file)

        # If nothing is passed, use all packages.
        if not specs:
            specs = [Spec(n) for n in spack.repo.all_package_names()]
            specs.sort(key=lambda s: s.format("$_$@").lower())

        # If the user asked for dependencies, traverse spec DAG get them.
        if args.dependencies:
            new_specs = set()
            for spec in specs:
                spec.concretize()
                for s in spec.traverse():
                    new_specs.add(s)
            specs = list(new_specs)

        # Skip external specs, as they are already installed
        external_specs = [s for s in specs if s.external]
        specs = [s for s in specs if not s.external]

        for spec in external_specs:
            msg = 'Skipping {0} as it is an external spec.'
            tty.msg(msg.format(spec.cshort_spec))

        # Default name for directory is spack-mirror-<DATESTAMP>
        directory = args.directory
        if not directory:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            directory = 'spack-mirror-' + timestamp

        # Make sure nothing is in the way.
        existed = os.path.isdir(directory)

        # Actually do the work to create the mirror
        present, mirrored, error = spack.mirror.create(
            directory, specs, num_versions=args.one_version_per_spec)
        p, m, e = len(present), len(mirrored), len(error)

        verb = "updated" if existed else "created"
        tty.msg(
            "Successfully %s mirror in %s" % (verb, directory),
            "Archive stats:",
            "  %-4d already present"  % p,
            "  %-4d added"            % m,
            "  %-4d failed to fetch." % e)
        if error:
            tty.error("Failed downloads:")
            colify(s.cformat("$_$@") for s in error)


def mirror(parser, args):
    action = {'create': mirror_create,
              'add': mirror_add,
              'remove': mirror_remove,
              'rm': mirror_remove,
              'list': mirror_list}

    action[args.mirror_command](args)
