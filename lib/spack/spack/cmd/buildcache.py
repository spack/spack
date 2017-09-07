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
    for pkg in pkgs:
        for spec in spack.cmd.parse_specs(pkg, concretize=True):
            specs.add(spec)
            tty.msg('recursing dependencies')
            for d, node in spec.traverse(order='post',
                                         depth=True,
                                         deptype=('link', 'run'),
                                         deptype_query='run'):
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
    specs, links = bindist.get_specs()
    matches = set()
    for spec in specs:
        for pkg in pkgs:
            if re.match(re.escape(pkg), str(spec)):
                matches.add(spec)
            if re.match(re.escape(pkg), '/%s' % spec.dag_hash()):
                matches.add(spec)

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
            tty.msg("buildcache spec(s) matching %s \n" % pkg)
            for spec in sorted(specs):
                if re.search("^" + re.escape(pkg), str(spec)):
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
