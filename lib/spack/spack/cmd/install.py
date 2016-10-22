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
import argparse

import llnl.util.tty as tty

import spack
import spack.cmd

description = "Build and install packages"


def setup_parser(subparser):
    subparser.add_argument(
        '--only',
        default='package,dependencies',
        dest='things_to_install',
        choices=['package', 'dependencies', 'package,dependencies'],
        help="""Select the mode of installation.
The default is to install the package along with all its dependencies.
Alternatively one can decide to install only the package or only
the dependencies."""
    )
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="Explicitly set number of make jobs.  Default is #cpus.")
    subparser.add_argument(
        '--keep-prefix', action='store_true', dest='keep_prefix',
        help="Don't remove the install prefix if installation fails.")
    subparser.add_argument(
        '--keep-stage', action='store_true', dest='keep_stage',
        help="Don't remove the build stage if installation succeeds.")
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="Do not check packages against checksum")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="Display verbose build output while installing.")
    subparser.add_argument(
        '--fake', action='store_true', dest='fake',
        help="Fake install. Just remove prefix and create a fake file.")
    subparser.add_argument(
        '--dirty', action='store_true', dest='dirty',
        help="Install a package *without* cleaning the environment.")
    subparser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="spec of the package to install"
    )
    subparser.add_argument(
        '--run-tests', action='store_true', dest='run_tests',
        help="Run tests during installation of a package.")


def install(parser, args, **kwargs):
    if not args.package:
        tty.die("install requires at least one package argument")

    if args.jobs is not None:
        if args.jobs <= 0:
            tty.die("The -j option must be a positive integer!")

    if args.no_checksum:
        spack.do_checksum = False        # TODO: remove this global.

    # Parse cli arguments and construct a dictionary
    # that will be passed to Package.do_install API
    kwargs.update({
        'keep_prefix': args.keep_prefix,
        'keep_stage': args.keep_stage,
        'install_deps': 'dependencies' in args.things_to_install,
        'make_jobs': args.jobs,
        'run_tests': args.run_tests,
        'verbose': args.verbose,
        'fake': args.fake,
        'dirty': args.dirty
    })

    # Spec from cli
    specs = spack.cmd.parse_specs(args.package, concretize=True)
    if len(specs) != 1:
        tty.error('only one spec can be installed at a time.')
    spec = specs.pop()

    if args.things_to_install == 'dependencies':
        # Install dependencies as-if they were installed
        # for root (explicit=False in the DB)
        kwargs['explicit'] = False
        for s in spec.dependencies():
            p = spack.repo.get(s)
            p.do_install(**kwargs)
    else:
        package = spack.repo.get(spec)
        kwargs['explicit'] = True
        package.do_install(**kwargs)
