# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.environment as ev
import spack.cmd
import spack.cmd.find
import spack.repo
import spack.store
from spack.filesystem_view import YamlFilesystemView

description = "list extensions for package"
section = "extensions"
level = "long"


def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        '-l', '--long', action='store_true', dest='long',
        help='show dependency hashes as well as versions')
    format_group.add_argument(
        '-p', '--paths', action='store_const', dest='mode', const='paths',
        help='show paths to extension install directories')
    format_group.add_argument(
        '-d', '--deps', action='store_const', dest='mode', const='deps',
        help='show full dependency DAG of extensions')
    subparser.add_argument(
        '-s', '--show', dest='show', metavar='TYPE', type=str,
        default='all',
        help="one of packages, installed, activated, all")
    subparser.add_argument(
        '-v', '--view', metavar='VIEW', type=str,
        help="the view to operate on")

    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help='spec of package to list extensions for')


def extensions(parser, args):
    if not args.spec:
        tty.die("extensions requires a package spec.")

    show_packages = False
    show_installed = False
    show_activated = False
    show_all = False
    if args.show == 'packages':
        show_packages = True
    elif args.show == 'installed':
        show_installed = True
    elif args.show == 'activated':
        show_activated = True
    elif args.show == 'all':
        show_packages = True
        show_installed = True
        show_activated = True
        show_all = True
    else:
        tty.die('unrecognized show type: %s' % args.show)

    #
    # Checks
    #
    spec = spack.cmd.parse_specs(args.spec)
    if len(spec) > 1:
        tty.die("Can only list extensions for one package.")

    if not spec[0].package.extendable:
        tty.die("%s is not an extendable package." % spec[0].name)

    env = ev.get_env(args, 'extensions')
    spec = spack.cmd.disambiguate_spec(spec[0], env)

    if not spec.package.extendable:
        tty.die("%s does not have extensions." % spec.short_spec)

    if not args.mode:
        args.mode = 'short'

    if show_packages:
        #
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

    if show_installed:
        #
        # List specs of installed extensions.
        #
        installed = [
            s.spec for s in spack.store.db.installed_extensions_for(spec)]

        if show_all:
            print
        if not installed:
            tty.msg("None installed.")
        else:
            tty.msg("%d installed:" % len(installed))
            spack.cmd.find.display_specs(installed, mode=args.mode)

    if show_activated:
        #
        # List specs of activated extensions.
        #
        activated = view.extensions_layout.extension_map(spec)
        if show_all:
            print
        if not activated:
            tty.msg("None activated.")
        else:
            tty.msg("%d currently activated:" % len(activated))
            spack.cmd.find.display_specs(
                activated.values(), mode=args.mode, long=args.long)
