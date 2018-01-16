##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import codecs
import functools
import os
import platform
import shutil
import sys
import time
import xml.dom.minidom
import xml.etree.ElementTree as ET

import llnl.util.filesystem as fs
import llnl.util.tty as tty
import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
from spack.build_environment import InstallError
from spack.fetch_strategy import FetchError
from spack.package import PackageBase

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
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="explicitly set number of make jobs. default is #cpus")
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
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true',
        help="do not check packages against checksum")
    subparser.add_argument(
        '-v', '--verbose', action='store_true',
        help="display verbose build output while installing")
    subparser.add_argument(
        '--fake', action='store_true',
        help="fake install for debug purposes.")
    subparser.add_argument(
        '-f', '--file', action='store_true',
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
        choices=['junit'],
        help="format to be used for log files"
    )
    subparser.add_argument(
        '--log-file',
        default=None,
        help="filename for the log file. if not passed a default will be used"
    )
    arguments.add_common_arguments(subparser, ['yes_to_all'])


# Needed for test cases
class TestResult(object):
    PASSED = 0
    FAILED = 1
    SKIPPED = 2
    ERRORED = 3


class TestSuite(object):
    def __init__(self, spec):
        self.root = ET.Element('testsuite')
        self.tests = []
        self.spec = spec

    def append(self, item):
        if not isinstance(item, TestCase):
            raise TypeError(
                'only TestCase instances may be appended to TestSuite'
            )
        self.tests.append(item)  # Append the item to the list of tests

    def dump(self, filename):
        # Prepare the header for the entire test suite
        number_of_errors = sum(
            x.result_type == TestResult.ERRORED for x in self.tests
        )
        self.root.set('errors', str(number_of_errors))
        number_of_failures = sum(
            x.result_type == TestResult.FAILED for x in self.tests
        )
        self.root.set('failures', str(number_of_failures))
        self.root.set('tests', str(len(self.tests)))
        self.root.set('name', self.spec.short_spec)
        self.root.set('hostname', platform.node())

        for item in self.tests:
            self.root.append(item.element)

        with codecs.open(filename, 'wb', 'utf-8') as file:
            xml_string = ET.tostring(self.root)
            xml_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
            file.write(xml_string)


class TestCase(object):

    results = {
        TestResult.PASSED: None,
        TestResult.SKIPPED: 'skipped',
        TestResult.FAILED: 'failure',
        TestResult.ERRORED: 'error',
    }

    def __init__(self, classname, name):
        self.element = ET.Element('testcase')
        self.element.set('classname', str(classname))
        self.element.set('name', str(name))
        self.result_type = None

    def set_duration(self, duration):
        self.element.set('time', str(duration))

    def set_result(self, result_type,
                   message=None, error_type=None, text=None):
        self.result_type = result_type
        result = TestCase.results[self.result_type]
        if result is not None and result is not TestResult.PASSED:
            subelement = ET.SubElement(self.element, result)
            if error_type is not None:
                subelement.set('type', error_type)
            if message is not None:
                subelement.set('message', str(message))
            if text is not None:
                subelement.text = text


def fetch_text(path):
    if not os.path.exists(path):
        return ''

    with codecs.open(path, 'rb', 'utf-8') as f:
        return '\n'.join(
            list(line.strip() for line in f.readlines())
        )


def junit_output(spec, test_suite):
    # Cycle once and for all on the dependencies and skip
    # the ones that are already installed. This ensures that
    # for the same spec, the same number of entries will be
    # displayed in the XML report
    for x in spec.traverse(order='post'):
        package = spack.repo.get(x)
        if package.installed:
            test_case = TestCase(package.name, x.short_spec)
            test_case.set_duration(0.0)
            test_case.set_result(
                TestResult.SKIPPED,
                message='Skipped [already installed]',
                error_type='already_installed'
            )
            test_suite.append(test_case)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, ** kwargs):

            # Check if the package has been installed already
            if self.installed:
                return

            test_case = TestCase(self.name, self.spec.short_spec)
            # Try to install the package
            try:
                # If already installed set the spec as skipped
                start_time = time.time()
                # PackageBase.do_install
                func(self, *args, **kwargs)
                duration = time.time() - start_time
                test_case.set_duration(duration)
                test_case.set_result(TestResult.PASSED)
            except InstallError:
                # Check if the package relies on dependencies that
                # did not install
                duration = time.time() - start_time
                test_case.set_duration(duration)
                if [x for x in self.spec.dependencies(('link', 'run')) if not spack.repo.get(x).installed]:  # NOQA: ignore=E501
                    test_case.set_duration(0.0)
                    test_case.set_result(
                        TestResult.SKIPPED,
                        message='Skipped [failed dependencies]',
                        error_type='dep_failed'
                    )
                else:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    text = fetch_text(self.build_log_path)
                    test_case.set_result(
                        TestResult.FAILED,
                        message='Installation failure',
                        text=text
                    )
            except FetchError:
                # A FetchError is considered an error as
                # we didn't even start building
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.FAILED,
                    message='Unable to fetch package',
                    text=text
                )
            except Exception:
                # Anything else is also an error
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.FAILED,
                    message='Unexpected exception thrown during install',
                    text=text
                )
            except BaseException:
                # Anything else is also an error
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.FAILED,
                    message='Unknown error',
                    text=text
                )

            # Try to get the log
            test_suite.append(test_case)
        return wrapper
    return decorator


def default_log_file(spec):
    """Computes the default filename for the log file and creates
    the corresponding directory if not present
    """
    fmt = 'test-{x.name}-{x.version}-{hash}.xml'
    basename = fmt.format(x=spec, hash=spec.dag_hash())
    dirname = fs.join_path(spack.var_path, 'junit-report')
    fs.mkdirp(dirname)
    return fs.join_path(dirname, basename)


def install_spec(cli_args, kwargs, spec):

    saved_do_install = PackageBase.do_install
    decorator = lambda fn: fn

    # Check if we were asked to produce some log for dashboards
    if cli_args.log_format is not None:
        # Compute the filename for logging
        log_filename = cli_args.log_file
        if not log_filename:
            log_filename = default_log_file(spec)

        # Create the test suite in which to log results
        test_suite = TestSuite(spec)

        # Temporarily decorate PackageBase.do_install to monitor
        # recursive calls.
        decorator = junit_output(spec, test_suite)

    # Do the actual installation
    try:
        # decorate the install if necessary
        PackageBase.do_install = decorator(PackageBase.do_install)

        if cli_args.things_to_install == 'dependencies':
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

    except InstallError as e:
        if cli_args.show_log_on_error:
            e.print_context()
            if not os.path.exists(e.pkg.build_log_path):
                tty.error("'spack install' created no log.")
            else:
                sys.stderr.write('Full build log:\n')
                with open(e.pkg.build_log_path) as log:
                    shutil.copyfileobj(log, sys.stderr)
        raise

    finally:
        PackageBase.do_install = saved_do_install

    # Dump test output if asked to
    if cli_args.log_format is not None:
        test_suite.dump(log_filename)


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

    specs = spack.cmd.parse_specs(args.package)
    if args.test == 'all' or args.run_tests:
        spack.package_testing.test_all()
    elif args.test == 'root':
        for spec in specs:
            spack.package_testing.test(spec.name)

    # Spec from cli
    specs = []
    if args.file:
        for file in args.package:
            with open(file, 'r') as f:
                specs.append(spack.spec.Spec.from_yaml(f))
    else:
        specs = spack.cmd.parse_specs(args.package, concretize=True)
    if len(specs) == 0:
        tty.error('The `spack install` command requires a spec to install.')

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
