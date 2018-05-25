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
import argparse
import os
import shutil
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.paths
import spack.build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.fetch_strategy
import spack.report
from spack.error import SpackError


description = "build and install packages"
section = "build"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        '--only',
        default='package,dependencies',
        dest='things_to_install',
        choices=['package', 'dependencies'],
        help="""select the mode of installation.
the default is to install the package along with all its dependencies.
alternatively one can decide to install only the package or only
the dependencies"""
    )
    arguments.add_common_arguments(subparser, ['jobs'])
    subparser.add_argument(
        '--overwrite', action='store_true',
        help="reinstall an existing spec, even if it has dependents")
    subparser.add_argument(
        '--keep-prefix', action='store_true',
        help="don't remove the install prefix if installation fails")
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="don't remove the build stage if installation succeeds")
    subparser.add_argument(
        '--dont-restage', action='store_true',
        help="if a partial install is detected, don't delete prior state")
    subparser.add_argument(
        '--use-cache', action='store_true', dest='use_cache',
        help="check for pre-built Spack packages in mirrors")
    subparser.add_argument(
        '--show-log-on-error', action='store_true',
        help="print full build log to stderr if build fails")
    subparser.add_argument(
        '--source', action='store_true', dest='install_source',
        help="install source files in prefix")
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '-v', '--verbose', action='store_true',
        help="display verbose build output while installing")
    subparser.add_argument(
        '--fake', action='store_true',
        help="fake install for debug purposes.")
    subparser.add_argument(
        '-f', '--file', action='append', default=[],
        dest='specfiles', metavar='SPEC_YAML_FILE',
        help="install from file. Read specs to install from .yaml files")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])

    subparser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="spec of the package to install"
    )
    testing = subparser.add_mutually_exclusive_group()
    testing.add_argument(
        '--test', default=None,
        choices=['root', 'all'],
        help="""If 'root' is chosen, run package tests during
installation for top-level packages (but skip tests for dependencies).
if 'all' is chosen, run package tests during installation for all
packages. If neither are chosen, don't run tests for any packages."""
    )
    testing.add_argument(
        '--run-tests', action='store_true',
        help='run package tests during installation (same as --test=all)'
    )
    subparser.add_argument(
        '--log-format',
        default=None,
        choices=spack.report.valid_formats,
        help="format to be used for log files"
    )
    subparser.add_argument(
        '--log-file',
        default=None,
        help="filename for the log file. if not passed a default will be used"
    )
    subparser.add_argument(
        '--cdash-upload-url',
        default=None,
        help="CDash URL where reports will be uploaded"
    )
    arguments.add_common_arguments(subparser, ['yes_to_all'])


def default_log_file(spec):
    """Computes the default filename for the log file and creates
    the corresponding directory if not present
    """
    fmt = 'test-{x.name}-{x.version}-{hash}.xml'
    basename = fmt.format(x=spec, hash=spec.dag_hash())
    dirname = fs.os.path.join(spack.paths.var_path, 'junit-report')
    fs.mkdirp(dirname)
    return fs.os.path.join(dirname, basename)


def install_spec(cli_args, kwargs, spec):
    # Do the actual installation
    try:
        if cli_args.things_to_install == 'dependencies':
            # Install dependencies as-if they were installed
            # for root (explicit=False in the DB)
            kwargs['explicit'] = False
            for s in spec.dependencies():
                s.package.do_install(**kwargs)
        else:
            kwargs['explicit'] = True
            spec.package.do_install(**kwargs)

    except spack.build_environment.InstallError as e:
        if cli_args.show_log_on_error:
            e.print_context()
            if not os.path.exists(e.pkg.build_log_path):
                tty.error("'spack install' created no log.")
            else:
                sys.stderr.write('Full build log:\n')
                with open(e.pkg.build_log_path) as log:
                    shutil.copyfileobj(log, sys.stderr)
        raise


def install(parser, args, **kwargs):
    if not args.package and not args.specfiles:
        tty.die("install requires at least one package argument or yaml file")

    if args.jobs is not None:
        if args.jobs <= 0:
            tty.die("The -j option must be a positive integer!")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    # Parse cli arguments and construct a dictionary
    # that will be passed to Package.do_install API
    kwargs.update({
        'keep_prefix': args.keep_prefix,
        'keep_stage': args.keep_stage,
        'restage': not args.dont_restage,
        'install_source': args.install_source,
        'install_deps': 'dependencies' in args.things_to_install,
        'make_jobs': args.jobs,
        'verbose': args.verbose,
        'fake': args.fake,
        'dirty': args.dirty,
        'use_cache': args.use_cache
    })

    if args.run_tests:
        tty.warn("Deprecated option: --run-tests: use --test=all instead")

    # 1. Abstract specs from cli
    reporter = spack.report.collect_info(args.log_format,
                                         ' '.join(args.package),
                                         args.cdash_upload_url)
    if args.log_file:
        reporter.filename = args.log_file

    specs = spack.cmd.parse_specs(args.package)
    tests = False
    if args.test == 'all' or args.run_tests:
        tests = True
    elif args.test == 'root':
        tests = [spec.name for spec in specs]
    kwargs['tests'] = tests

    try:
        specs = spack.cmd.parse_specs(
            args.package, concretize=True, tests=tests)
    except SpackError as e:
        reporter.concretization_report(e.message)
        raise

    # 2. Concrete specs from yaml files
    for file in args.specfiles:
        with open(file, 'r') as f:
            s = spack.spec.Spec.from_yaml(f)

        if s.concretized().dag_hash() != s.dag_hash():
            msg = 'skipped invalid file "{0}". '
            msg += 'The file does not contain a concrete spec.'
            tty.warn(msg.format(file))
            continue

        specs.append(s.concretized())

    if len(specs) == 0:
        tty.die('The `spack install` command requires a spec to install.')

    if not args.log_file:
        reporter.filename = default_log_file(specs[0])
    reporter.specs = specs
    with reporter:
        if args.overwrite:
            # If we asked to overwrite an existing spec we must ensure that:
            # 1. We have only one spec
            # 2. The spec is already installed
            assert len(specs) == 1, \
                "only one spec is allowed when overwriting an installation"

            spec = specs[0]
            t = spack.store.db.query(spec)
            assert len(t) == 1, "to overwrite a spec you must install it first"

            # Give the user a last chance to think about overwriting an already
            # existing installation
            if not args.yes_to_all:
                tty.msg('The following package will be reinstalled:\n')

                display_args = {
                    'long': True,
                    'show_flags': True,
                    'variants': True
                }

                spack.cmd.display_specs(t, **display_args)
                answer = tty.get_yes_or_no(
                    'Do you want to proceed?', default=False
                )
                if not answer:
                    tty.die('Reinstallation aborted.')

            with fs.replace_directory_transaction(specs[0].prefix):
                install_spec(args, kwargs, specs[0])

        else:
            for spec in specs:
                install_spec(args, kwargs, spec)
