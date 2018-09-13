##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import argparse

import llnl.util.tty as tty

import spack.cmd
import spack.repo
import spack.store
import spack.spec
import spack.binary_distribution as bindist

description = "create, download and install binary packages"
section = "packaging"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='buildcache sub-commands')

    create = subparsers.add_parser('create', help=createtarball.__doc__)
    create.add_argument('-r', '--rel', action='store_true',
                        help="make all rpaths relative" +
                             " before creating tarballs.")
    create.add_argument('-f', '--force', action='store_true',
                        help="overwrite tarball if it exists.")
    create.add_argument('-u', '--unsigned', action='store_true',
                        help="create unsigned buildcache" +
                             " tarballs for testing")
    create.add_argument('-a', '--allow_root', action='store_true',
                        help="allow install root string in binary files " +
                             "after RPATH substitution")
    create.add_argument('-k', '--key', metavar='key',
                        type=str, default=None,
                        help="Key for signing.")
    create.add_argument('-d', '--directory', metavar='directory',
                        type=str, default='.',
                        help="directory in which to save the tarballs.")
    create.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to create buildcache for")
    create.set_defaults(func=createtarball)

    install = subparsers.add_parser('install', help=installtarball.__doc__)
    install.add_argument('-f', '--force', action='store_true',
                         help="overwrite install directory if it exists.")
    install.add_argument('-m', '--multiple', action='store_true',
                         help="allow all matching packages ")
    install.add_argument('-a', '--allow_root', action='store_true',
                         help="allow install root string in binary files " +
                              "after RPATH substitution")
    install.add_argument('-u', '--unsigned', action='store_true',
                         help="install unsigned buildcache" +
                              " tarballs for testing")
    install.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to install biuldache for")
    install.set_defaults(func=installtarball)

    listcache = subparsers.add_parser('list', help=listspecs.__doc__)
    listcache.add_argument('-f', '--force', action='store_true',
                           help="force new download of specs")
    listcache.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to search for")
    listcache.set_defaults(func=listspecs)

    dlkeys = subparsers.add_parser('keys', help=getkeys.__doc__)
    dlkeys.add_argument(
        '-i', '--install', action='store_true',
        help="install Keys pulled from mirror")
    dlkeys.add_argument(
        '-t', '--trust', action='store_true',
        help="trust all downloaded keys")
    dlkeys.add_argument('-f', '--force', action='store_true',
                        help="force new download of keys")
    dlkeys.set_defaults(func=getkeys)


def find_matching_specs(pkgs, allow_multiple_matches=False, force=False):
    """Returns a list of specs matching the not necessarily
       concretized specs given from cli

    Args:
        specs: list of specs to be matched against installed packages
        allow_multiple_matches : if True multiple matches are admitted

    Return:
        list of specs
    """
    # List of specs that match expressions given via command line
    specs_from_cli = []
    has_errors = False
    specs = spack.cmd.parse_specs(pkgs)
    for spec in specs:
        matching = spack.store.db.query(spec)
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error('%s matches multiple installed packages:' % spec)
            for match in matching:
                tty.msg('"%s"' % match.format())
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not any:
            tty.error('{0} does not match any installed packages.'.format(
                spec))
            has_errors = True

        specs_from_cli.extend(matching)
    if has_errors:
        tty.die('use one of the matching specs above')

    return specs_from_cli


def match_downloaded_specs(pkgs, allow_multiple_matches=False, force=False):
    """Returns a list of specs matching the not necessarily
       concretized specs given from cli

    Args:
        specs: list of specs to be matched against buildcaches on mirror
        allow_multiple_matches : if True multiple matches are admitted

    Return:
        list of specs
    """
    # List of specs that match expressions given via command line
    specs_from_cli = []
    has_errors = False
    specs = bindist.get_specs(force)
    for pkg in pkgs:
        matches = []
        tty.msg("buildcache spec(s) matching %s \n" % pkg)
        for spec in sorted(specs):
            if pkg.startswith('/'):
                pkghash = pkg.replace('/', '')
                if spec.dag_hash().startswith(pkghash):
                    matches.append(spec)
            else:
                if spec.satisfies(pkg):
                    matches.append(spec)
        # For each pkg provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matches) > 1:
            tty.error('%s matches multiple downloaded packages:' % pkg)
            for match in matches:
                tty.msg('"%s"' % match.format())
            has_errors = True

        # No downloaded package matches the query
        if len(matches) == 0:
            tty.error('%s does not match any downloaded packages.' % pkg)
            has_errors = True

        specs_from_cli.extend(matches)
    if has_errors:
        tty.die('use one of the matching specs above')

    return specs_from_cli


def createtarball(args):
    """create a binary package from an existing install"""
    if not args.packages:
        tty.die("build cache file creation requires at least one" +
                " installed package argument")
    pkgs = set(args.packages)
    specs = set()
    outdir = '.'
    if args.directory:
        outdir = args.directory
    signkey = None
    if args.key:
        signkey = args.key

    matches = find_matching_specs(pkgs, False, False)
    for match in matches:
        if match.external or match.virtual:
            tty.msg('skipping external or virtual spec %s' %
                    match.format())
        else:
            tty.msg('adding matching spec %s' % match.format())
            specs.add(match)
            tty.msg('recursing dependencies')
            for d, node in match.traverse(order='post',
                                          depth=True,
                                          deptype=('link', 'run')):
                if node.external or node.virtual:
                    tty.msg('skipping external or virtual dependency %s' %
                            node.format())
                else:
                    tty.msg('adding dependency %s' % node.format())
                    specs.add(node)

    tty.msg('writing tarballs to %s/build_cache' % outdir)

    for spec in specs:
        tty.msg('creating binary cache file for package %s ' % spec.format())
        bindist.build_tarball(spec, outdir, args.force, args.rel,
                              args.unsigned, args.allow_root, signkey)


def installtarball(args):
    """install from a binary package"""
    if not args.packages:
        tty.die("build cache file installation requires" +
                " at least one package spec argument")
    pkgs = set(args.packages)
    matches = match_downloaded_specs(pkgs, args.multiple, args.force)

    for match in matches:
        install_tarball(match, args)


def install_tarball(spec, args):
    s = spack.spec.Spec(spec)
    if s.external or s.virtual:
        tty.warn("Skipping external or virtual package %s" % spec.format())
        return
    for d in s.dependencies(deptype=('link', 'run')):
        tty.msg("Installing buildcache for dependency spec %s" % d)
        install_tarball(d, args)
    package = spack.repo.get(spec)
    if s.concrete and package.installed and not args.force:
        tty.warn("Package for spec %s already installed." % spec.format())
    else:
        tarball = bindist.download_tarball(spec)
        if tarball:
            tty.msg('Installing buildcache for spec %s' % spec.format())
            bindist.extract_tarball(spec, tarball, args.allow_root,
                                    args.unsigned, args.force)
            spack.store.store.reindex()
        else:
            tty.die('Download of binary cache file for spec %s failed.' %
                    spec.format())


def listspecs(args):
    """list binary packages available from mirrors"""
    specs = bindist.get_specs(args.force)
    if args.packages:
        pkgs = set(args.packages)
        for pkg in pkgs:
            tty.msg("buildcache spec(s) matching " +
                    "%s and commands to install them" % pkgs)
            for spec in sorted(specs):
                if spec.satisfies(pkg):
                    tty.msg('Enter\nspack buildcache install /%s\n' %
                            spec.dag_hash(7) +
                            ' to install "%s"' %
                            spec.format())
    else:
        tty.msg("buildcache specs and commands to install them")
        for spec in sorted(specs):
            tty.msg('Enter\nspack buildcache install /%s\n' %
                    spec.dag_hash(7) +
                    ' to install "%s"' %
                    spec.format())


def getkeys(args):
    """get public keys available on mirrors"""
    bindist.get_keys(args.install, args.trust, args.force)


def buildcache(parser, args):
    if args.func:
        args.func(args)
