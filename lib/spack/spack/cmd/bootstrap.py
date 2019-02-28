# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.repo
import spack.spec
import spack.cmd.common.arguments as arguments

description = "Bootstrap packages needed for spack to run smoothly"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="explicitly set number of make jobs (default: #cpus)")
    subparser.add_argument(
        '--keep-prefix', action='store_true', dest='keep_prefix',
        help="don't remove the install prefix if installation fails")
    subparser.add_argument(
        '--keep-stage', action='store_true', dest='keep_stage',
        help="don't remove the build stage if installation succeeds")
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="display verbose build output while installing")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])


def bootstrap(parser, args, **kwargs):
    kwargs.update({
        'keep_prefix': args.keep_prefix,
        'keep_stage': args.keep_stage,
        'install_deps': 'dependencies',
        'make_jobs': args.jobs,
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
            spec_to_install = spack.spec.Spec(requirement_dict[requirement])
            spec_to_install.concretize()
            tty.msg("Installing %s to satisfy requirement for %s" %
                    (spec_to_install, requirement))
            kwargs['explicit'] = True
            package = spack.repo.get(spec_to_install)
            package.do_install(**kwargs)
