##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import argparse

import os
import re
import llnl.util.tty as tty

import spack
import spack.cmd
import spack.binary_distribution as bindist
from spack.binary_distribution import NoOverwriteException, NoGpgException
from spack.binary_distribution import NoKeyException, PickKeyException
from spack.binary_distribution import NoVerifyException, NoChecksumException

description = "Create, download and install build cache files."
section = "caching"
level = "long"

# Arguments for display_specs when we find ambiguity
display_args = {
    'long': True,
    'show_flags': True,
    'variants': True
}

error_message = """You can either:
    a) use a more specific spec or /hash , 
    b) use -y to use all matches
"""

def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='buildcache sub-commands')

    create = subparsers.add_parser('create')
    create.add_argument('-r', '--rel', action='store_true',
                        help="make all rpaths relative" +
                             " before creating tarballs.")
    create.add_argument('-f', '--force', action='store_true',
                        help="overwrite tarball if it exists.")
    create.add_argument('-y', '--yes-to-all', action='store_true',
                        help="answer yes to all create unsigned " +
                             "buildcache questions")
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

    install = subparsers.add_parser('install')
    install.add_argument('-f', '--force', action='store_true',
                         help="overwrite install directory if it exists.")
    install.add_argument('-y', '--yes-to-all', action='store_true',
                         help="answer yes to all install unsigned " +
                              "buildcache questions")
    install.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to install biuldache for")
    install.set_defaults(func=installtarball)

    listcache = subparsers.add_parser('list')
    listcache.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to search for")
    listcache.set_defaults(func=listspecs)

    dlkeys = subparsers.add_parser('keys')
    dlkeys.add_argument(
        '-i', '--install', action='store_true',
        help="install Keys pulled from mirror")
    dlkeys.add_argument(
        '-y', '--yes-to-all', action='store_true',
        help="answer yes to all trust questions")
    dlkeys.set_defaults(func=getkeys)

def match_installed_specs(specs, allow_multiple_matches=False, force=False):
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
    for spec in specs:
        matching = spack.store.db.query(spec)
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error('{0} matches multiple packages:'.format(spec))
            print()
            spack.cmd.display_specs(matching, **display_args)
            print()
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not any:
            tty.error('{0} does not match any installed packages.'.format(
                spec))
            has_errors = True

        specs_from_cli.extend(matching)
    if has_errors:
        tty.die(error_message)

    return specs_from_cli

def match_downloaded_specs(pkgs, allow_multiple_matches=False):
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
    specs, links = bindist.get_specs()
    for pkg in pkgs:
        matches = []
        tty.msg("buildcache spec(s) matching %s \n" % pkg)
        for spec in sorted(specs):
            if spec.satisfies(pkg):
                matches.append(spec)
        # For each pkg provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matches) > 1:
            tty.error('{0} matches multiple downloaded packages:'.format(pkg))
            print()
            spack.cmd.display_specs(matches, **display_args)
            print()
            has_errors = True

        # No downloaded package matches the query
        if len(matches) == 0 :
            tty.error('{0} does not match any downloaded packages.'.format(
                      pkg))
            has_errors = True

        specs_from_cli.extend(matches)
    if has_errors:
        tty.die(error_message)

    return specs_from_cli

def createtarball(args):
    if not args.packages:
        tty.die("build cache file creation requires at least one" +
                " installed package argument")
    pkgs = set(args.packages)
    specs = set()
    outdir = os.getcwd()
    if args.directory:
        outdir = args.directory
    signkey = None
    if args.key:
        signkey = args.key
    yes_to_all = False
    force = False
    relative = False
    if args.yes_to_all:
        yes_to_all = True
    if args.force:
        force = True
    if args.rel:
        relative = True

    matches=match_installed_specs(pkgs, yes_to_all, force)
    for match in matches:
        tty.msg('adding matching spec %s' % match.format())
        specs.add(match)
        tty.msg('recursing dependencies')
        for d, node in match.traverse(order='post',
                                     depth=True,
                                     deptype=('link', 'run')):
            if not node.external:
                tty.msg('adding dependency %s' % node.format())
                specs.add(node)

    for spec in specs:
        tty.msg('creating binary cache file for package %s ' % spec.format())
        try:
            bindist.build_tarball(spec, outdir, force,
                                  relative, yes_to_all, signkey)
        except NoOverwriteException as e:
            tty.warn("%s exists, use -f to force overwrite." % e)
        except NoGpgException:
            tty.warn("gpg2 is not available,"
                     " use -y to create unsigned build caches")
        except NoKeyException:
            tty.warn("no default key available for signing,"
                     " use -y to create unsigned build caches"
                     " or spack gpg init to create a default key")
        except PickKeyException:
            tty.warn("multi keys available for signing,"
                     " use -y to create unsigned build caches"
                     " or -k <key hash> to pick a key")


def installtarball(args):
    if not args.packages:
        tty.die("build cache file installation requires" +
                " at least one package spec argument")
    pkgs = set(args.packages)
    yes_to_all = False
    if args.yes_to_all:
        yes_to_all = True
    matches = match_downloaded_specs(pkgs,yes_to_all)

    for match in matches:
        install_tarball(match, args)


def install_tarball(spec, args):
    s = spack.spec.Spec(spec)
    yes_to_all = False
    force = False
    if args.yes_to_all:
        yes_to_all = True
    if args.force:
        force = True
    for d in s.dependencies():
        tty.msg("Installing buildcache for dependency spec %s" % d)
        install_tarball(d, args)
    package = spack.repo.get(spec)
    if s.concrete and package.installed and not force:
        tty.warn("Package for spec %s already installed." % spec.format(),
                 " Use -f flag to overwrite.")
    else:
        tarball = bindist.download_tarball(spec)
        if tarball:
            tty.msg('Installing buildcache for spec %s' % spec.format())
            try:
                bindist.extract_tarball(spec, tarball, yes_to_all, force)
            except NoOverwriteException as e:
                tty.warn("%s exists. use -f to force overwrite." % e.args)
            except NoVerifyException:
                tty.die("Package spec file failed signature verification,"
                        " use -y flag to install build cache")
            except NoChecksumException:
                tty.die("Package tarball failed checksum verification,"
                        " use -y flag to install build cache")
            finally:
                spack.store.db.reindex(spack.store.layout)
        else:
            tty.die('Download of binary cache file for spec %s failed.' %
                    spec.format())


def listspecs(args):
    specs, links = bindist.get_specs()
    if args.packages:
        pkgs = set(args.packages)
        for pkg in pkgs:
            tty.msg("buildcache spec(s) matching %s \n" % pkgs)
            for spec in sorted(specs):
                if spec.satisfies(pkg):
                    tty.msg('run "spack buildcache install /%s"' %
                            spec.dag_hash(7) + ' to install  %s\n' %
                            spec.format())
    else:
        tty.msg("buildcache specs ")
        for spec in sorted(specs):
            tty.msg('run "spack buildcache install /%s" to install  %s\n' %
                    (spec.dag_hash(7), spec.format()))


def getkeys(args):
    install = False
    if args.install:
        install = True
    yes_to_all = False
    if args.yes_to_all:
        yes_to_all = True
    bindist.get_keys(install, yes_to_all)


def buildcache(parser, args):
    if args.func:
        args.func(args)
