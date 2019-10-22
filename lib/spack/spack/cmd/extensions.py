# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.environment as ev
import spack.cmd as cmd
import spack.cmd.common.arguments as arguments
import spack.repo
import spack.store
from spack.filesystem_view import YamlFilesystemView

description = "list extensions for package"
section = "extensions"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['long', 'very_long'])
    subparser.add_argument('-d', '--deps', action='store_true',
                           help='output dependencies along with found specs')

    subparser.add_argument('-p', '--paths', action='store_true',
                           help='show paths to package install directories')
    subparser.add_argument(
        '-s', '--show', action='store', default='all',
        choices=("packages", "installed", "activated", "all"),
        help="show only part of output")
    subparser.add_argument(
        '-v', '--view', metavar='VIEW', type=str,
        help="the view to operate on")

    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help='spec of package to list extensions for')


def extensions(parser, args):
    if not args.spec:
        tty.die("extensions requires a package spec.")

    # Checks
    spec = cmd.parse_specs(args.spec)
    if len(spec) > 1:
        tty.die("Can only list extensions for one package.")

    if not spec[0].package.extendable:
        tty.die("%s is not an extendable package." % spec[0].name)

    env = ev.get_env(args, 'extensions')
    spec = cmd.disambiguate_spec(spec[0], env)

    if not spec.package.extendable:
        tty.die("%s does not have extensions." % spec.short_spec)

    if args.show in ("packages", "all"):
        # List package names of extensions
        extensions = spack.repo.path.extensions_for(spec)
        if not extensions:
            tty.msg("%s has no extensions." % spec.cshort_spec)
        else:
            tty.msg(spec.cshort_spec)
            tty.msg("%d extensions:" % len(extensions))
            colify(ext.name for ext in extensions)

    if args.view:
        target = args.view
    else:
        target = spec.prefix

    view = YamlFilesystemView(target, spack.store.layout)

    if args.show in ("installed", "all"):
        # List specs of installed extensions.
        installed = [
            s.spec for s in spack.store.db.installed_extensions_for(spec)]

        if args.show == "all":
            print
        if not installed:
            tty.msg("None installed.")
        else:
            tty.msg("%d installed:" % len(installed))
            cmd.display_specs(installed, args)

    if args.show in ("activated", "all"):
        # List specs of activated extensions.
        activated = view.extensions_layout.extension_map(spec)
        if args.show == "all":
            print
        if not activated:
            tty.msg("None activated.")
        else:
            tty.msg("%d activated:" % len(activated))
            cmd.display_specs(activated.values(), args)
