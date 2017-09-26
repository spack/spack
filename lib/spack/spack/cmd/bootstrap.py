##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import llnl.util.tty as tty
import spack
import spack.cmd
import spack.cmd.common.arguments as arguments

description = "Bootstrap packages needed for spack to run smoothly"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="explicitly set number of make jobs. default is #cpus")
    subparser.add_argument(
        '--keep-prefix', action='store_true', dest='keep_prefix',
        help="don't remove the install prefix if installation fails")
    subparser.add_argument(
        '--keep-stage', action='store_true', dest='keep_stage',
        help="don't remove the build stage if installation succeeds")
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="do not check packages against checksum")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="display verbose build output while installing")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])

    subparser.add_argument(
        '--run-tests', action='store_true', dest='run_tests',
        help="run package level tests during installation"
    )


def bootstrap(parser, args, **kwargs):
    kwargs.update({
        'keep_prefix': args.keep_prefix,
        'keep_stage': args.keep_stage,
        'install_deps': 'dependencies',
        'make_jobs': args.jobs,
        'run_tests': args.run_tests,
        'verbose': args.verbose,
        'dirty': args.dirty
    })

    # Define requirement dictionary defining general specs which need
    # to be satisfied, and the specs to install when the general spec
    # isn't satisfied.
    requirement_dict = {'environment-modules': 'environment-modules~X'}

    for requirement in requirement_dict:
        installed_specs = spack.store.db.query(requirement)
        if(len(installed_specs) > 0):
            tty.msg("Requirement %s is satisfied with installed "
                    "package %s" % (requirement, installed_specs[0]))
        else:
            # Install requirement
            spec_to_install = spack.Spec(requirement_dict[requirement])
            spec_to_install.concretize()
            tty.msg("Installing %s to satisfy requirement for %s" %
                    (spec_to_install, requirement))
            kwargs['explicit'] = True
            package = spack.repo.get(spec_to_install)
            package.do_install(**kwargs)
