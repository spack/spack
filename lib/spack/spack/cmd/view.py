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
'''Produce a "view" of a Spack DAG.

A "view" is file hierarchy representing the union of a number of
Spack-installed package file hierarchies.  The union is formed from:

- specs resolved from the package names given by the user (the seeds)

- all dependencies of the seeds unless user specifies `--no-dependencies`

- less any specs with names matching the regular expressions given by
  `--exclude`

The `view` can be built and tore down via a number of methods (the "actions"):

- symlink :: a file system view which is a directory hierarchy that is
  the union of the hierarchies of the installed packages in the DAG
  where installed files are referenced via symlinks.

- hardlink :: like the symlink view but hardlinks are used.

- statlink :: a view producing a status report of a symlink or
  hardlink view.

The file system view concept is imspired by Nix, implemented by
brett.viren@gmail.com ca 2016.

All operations on views are performed via proxy objects such as
YamlFilesystemView.

'''
import os

import llnl.util.tty as tty
from llnl.util.link_tree import MergeConflictError

import spack.cmd
import spack.store
from spack.filesystem_view import YamlFilesystemView

description = "produce a single-rooted directory view of packages"
section = "environment"
level = "short"

actions_link = ["symlink", "add", "soft", "hardlink", "hard"]
actions_remove = ["remove", "rm"]
actions_status = ["statlink", "status", "check"]


def relaxed_disambiguate(specs, view):
    """
        When dealing with querying actions (remove/status) the name of the spec
        is sufficient even though more versions of that name might be in the
        database.
    """
    name_to_spec = dict((s.name, s) for s in view.get_all_specs())

    def squash(matching_specs):
        if not matching_specs:
            tty.die("Spec matches no installed packages.")

        elif len(matching_specs) == 1:
            return matching_specs[0]

        elif matching_specs[0].name in name_to_spec:
            return name_to_spec[matching_specs[0].name]

        else:
            # we just return the first matching spec, the error about the
            # missing spec will be printed later on
            return matching_specs[0]

    # make function always return a list to keep consistency between py2/3
    return list(map(squash, map(spack.store.db.query, specs)))


def setup_parser(sp):
    setup_parser.parser = sp

    sp.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help="If not verbose only warnings/errors will be printed.")
    sp.add_argument(
        '-e', '--exclude', action='append', default=[],
        help="exclude packages with names matching the given regex pattern")
    sp.add_argument(
        '-d', '--dependencies', choices=['true', 'false', 'yes', 'no'],
        default='true',
        help="Link/remove/list dependencies.")

    ssp = sp.add_subparsers(metavar='ACTION', dest='action')

    specs_opts = dict(metavar='spec', action='store',
                      help="seed specs of the packages to view")

    # The action parameterizes the command but in keeping with Spack
    # patterns we make it a subcommand.
    file_system_view_actions = {
        "symlink": ssp.add_parser(
            'symlink', aliases=['add', 'soft'],
            help='add package files to a filesystem view via symbolic links'),
        "hardlink": ssp.add_parser(
            'hardlink', aliases=['hard'],
            help='add packages files to a filesystem via via hard links'),
        "remove": ssp.add_parser(
            'remove', aliases=['rm'],
            help='remove packages from a filesystem view'),
        "statlink": ssp.add_parser(
            'statlink', aliases=['status', 'check'],
            help='check status of packages in a filesystem view')
    }

    # All these options and arguments are common to every action.
    for cmd, act in file_system_view_actions.items():
        act.add_argument('path', nargs=1,
                         help="path to file system view directory")

        if cmd == "remove":
            grp = act.add_mutually_exclusive_group(required=True)
            act.add_argument(
                '--no-remove-dependents', action="store_true",
                help="Do not remove dependents of specified specs.")

            # with all option, spec is an optional argument
            so = specs_opts.copy()
            so["nargs"] = "*"
            so["default"] = []
            grp.add_argument('specs', **so)
            grp.add_argument("-a", "--all", action='store_true',
                             help="act on all specs in view")

        elif cmd == "statlink":
            so = specs_opts.copy()
            so["nargs"] = "*"
            act.add_argument('specs', **so)

        else:
            # without all option, spec is required
            so = specs_opts.copy()
            so["nargs"] = "+"
            act.add_argument('specs', **so)

    for cmd in ["symlink", "hardlink"]:
        act = file_system_view_actions[cmd]
        act.add_argument("-i", "--ignore-conflicts", action='store_true')

    return


def view(parser, args):
    'Produce a view of a set of packages.'

    specs = spack.cmd.parse_specs(args.specs)
    path = args.path[0]

    view = YamlFilesystemView(
        path, spack.store.layout,
        ignore_conflicts=getattr(args, "ignore_conflicts", False),
        link=os.link if args.action in ["hardlink", "hard"]
        else os.symlink,
        verbose=args.verbose)

    # Process common args and specs
    if getattr(args, "all", False):
        specs = view.get_all_specs()
        if len(specs) == 0:
            tty.warn("Found no specs in %s" % path)

    elif args.action in actions_link:
        # only link commands need to disambiguate specs
        specs = [spack.cmd.disambiguate_spec(s) for s in specs]

    elif args.action in actions_status:
        # no specs implies all
        if len(specs) == 0:
            specs = view.get_all_specs()
        else:
            specs = relaxed_disambiguate(specs, view)

    else:
        # status and remove can map the name to packages in view
        specs = relaxed_disambiguate(specs, view)

    with_dependencies = args.dependencies.lower() in ['true', 'yes']

    # Map action to corresponding functionality
    if args.action in actions_link:
        try:
            view.add_specs(*specs,
                           with_dependencies=with_dependencies,
                           exclude=args.exclude)
        except MergeConflictError:
            tty.info("Some file blocked the merge, adding the '-i' flag will "
                     "ignore this conflict. For more information see e.g. "
                     "https://github.com/spack/spack/issues/9029")
            raise

    elif args.action in actions_remove:
        view.remove_specs(*specs,
                          with_dependencies=with_dependencies,
                          exclude=args.exclude,
                          with_dependents=not args.no_remove_dependents)

    elif args.action in actions_status:
        view.print_status(*specs, with_dependencies=with_dependencies)

    else:
        tty.error('Unknown action: "%s"' % args.action)
