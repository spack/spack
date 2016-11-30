##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
import argparse

import llnl.util.tty as tty
import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
from spack.hooks.dashboards import test_suites, dashboard_output
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
        '--keep-prefix', action='store_true', dest='keep_prefix',
        help="don't remove the install prefix if installation fails")
    subparser.add_argument(
        '--keep-stage', action='store_true', dest='keep_stage',
        help="don't remove the build stage if installation succeeds")
    subparser.add_argument(
        '--restage', action='store_true', dest='restage',
        help="if a partial install is detected, delete prior state")
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="do not check packages against checksum")
    subparser.add_argument(
        '-v', '--verbose', action='store_true', dest='verbose',
        help="display verbose build output while installing")
    subparser.add_argument(
        '--fake', action='store_true', dest='fake',
        help="fake install. just remove prefix and create a fake file")
    subparser.add_argument(
        '-f', '--file', action='store_true', dest='file',
        help="install from file. Read specs to install from .yaml files")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])

    subparser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="spec of the package to install"
    )
    subparser.add_argument(
        '--run-tests', action='store_true', dest='run_tests',
        help="run package level tests during installation"
    )
    subparser.add_argument(
        '--log-format',
        default=None,
        choices=test_suites.keys(),
        help="format to be used for log files"
    )
    subparser.add_argument(
        '--log-file',
        default=None,
        help="filename for the log file. if not passed a default will be used"
    )


# Needed for test cases
class TestResult(object):
    PASSED = 0
    FAILED = 1
    SKIPPED = 2
    ERRORED = 3


class JUnitTestSuite(object):
    def __init__(self, spec, logfile):
        self.spec = spec
        self.root = ET.Element('testsuite')
        self.tests = []
        if logfile is not None:
            self.logfile = logfile
        else:
            fmt = 'test-{x.name}-{x.version}-{hash}.xml'
            basename = fmt.format(x=spec, hash=spec.dag_hash())
            dirname = fs.join_path(spack.var_path, 'junit-report')
            fs.mkdirp(dirname)
            self.logfile = fs.join_path(dirname, basename)

    def create_testcase(self, name, spec):
        item = JUnitTestCase(name, spec)
        self.tests.append(item)
        return item

    def dump(self):
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
        self.root.set('name', str(self.spec))
        self.root.set('hostname', platform.node())

        for item in self.tests:
            self.root.append(item.element)

        with codecs.open(self.logfile, 'wb', 'utf-8') as file:
            xml_string = ET.tostring(self.root)
            xml_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
            file.write(xml_string)


class JUnitTestCase(object):

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
        result = JUnitTestCase.results[self.result_type]
        if result is not None and result is not TestResult.PASSED:
            subelement = ET.SubElement(self.element, result)
            if error_type is not None:
                subelement.set('type', error_type)
            if message is not None:
                subelement.set('message', str(message))
            if text is not None:
                subelement.text = text


class CDashTestCase(object):

    results = {
        TestResult.PASSED: 'passed',
        TestResult.SKIPPED: 'notrun',
        TestResult.FAILED: 'failed',
        TestResult.ERRORED: 'failed',
    }

    def __init__(self, classname, name):
        self.name = name
        self.element = ET.Element('Test')
        name_element = ET.SubElement(self.element, 'Name')
        name_element.text = name
        path_element = ET.SubElement(self.element, 'Path')
        path_element.text = ""
        cmd_line_element = ET.SubElement(self.element, 'FullCommandLine')
        cmd_line_element.text = "spack install"
        self.result = ET.SubElement(self.element, 'Results')

    def set_duration(self, duration):
        execution_time = ET.SubElement(self.result, 'NamedMeasurement')
        execution_time.set('type', 'numeric/double')
        execution_time.set('name', 'Execution Time')
        value = ET.SubElement(execution_time, 'Value')
        value.text = str(duration)

    def set_result(self, result_type,
                   message=None, error_type=None, text=None):
        self.element.set('Status', CDashTestCase.results[result_type])
        # Completion Status
        completion_status = ET.SubElement(self.result, 'NamedMeasurement')
        completion_status.set('type', 'text/string')
        completion_status.set('name', 'Completion Status')
        value = ET.SubElement(completion_status, 'Value')
        value.text = 'Completed'
        # Command line
        cmd_line = ET.SubElement(self.result, 'NamedMeasurement')
        cmd_line.set('type', 'text/string')
        cmd_line.set('name', 'Command Line')
        value = ET.SubElement(cmd_line, 'Value')
        value.text = "spack install"
        # Logs
        logs = ET.SubElement(self.result, 'Measurement')
        value = ET.SubElement(logs, 'Value')
        value.text = message


def fetch_text(path):
    if not os.path.exists(path):
        return ''

    with codecs.open(path, 'rb', 'utf-8') as f:
        return '\n'.join(
            list(line.strip() for line in f.readlines())
        )


class CDashTestSuite(object):
    def __init__(self, spec, filename, slot='Experimental'):
        self.spec = spec
        self.slot = slot
        self.tests = []
        self.buildstamp = "%s-%s" % (time.strftime("%Y%d%m-%H:%M:%S"), slot)
        self.configure_report = self.prepare_configure_report_()
        self.filename = filename

    def create_filename(self, spec, subdir, step):
        if self.filename is not None:
            return "%s.%s.xml" % (self.filename, step)
        else:
            fmt = '%s-{x.name}-{x.version}-{hash}.xml' % step
            basename = fmt.format(x=spec, hash=spec.dag_hash())
            dirname = fs.join_path(spack.var_path, subdir)
            fs.mkdirp(dirname)
            return fs.join_path(dirname, basename)

    def create_template(self):
        template = ET.Element('Site')
        template.set('BuildName', str(self.spec.short_spec))
        template.set('Name', platform.node())
        template.set('Type', self.slot)
        template.set('BuildStamp', self.buildstamp)
        return template

    def create_testcase(self, name, spec):
        item = CDashTestCase(name, spec)
        self.tests.append(item)
        return item

    def dump(self):
        filename = self.create_filename(self.spec, 'cdash', 'configure')
        self.dump_report(self.configure_report, filename)
        build_report = self.prepare_build_report()
        filename = self.create_filename(self.spec, 'cdash', 'build')
        self.dump_report(build_report, filename)
        test_report = self.prepare_test_report()
        filename = self.create_filename(self.spec, 'cdash', 'test')
        self.dump_report(test_report, filename)

    def dump_report(self, report, filename):
        with codecs.open(filename, 'wb', 'utf-8') as file:
            xml_string = ET.tostring(report)
            xml_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
            file.write(xml_string)

    def now(self):
        return time.strftime("%a %b %d %H:%M:%S %Z")

    def prepare_configure_report_(self):
        report = self.create_template()
        configure = ET.SubElement(report, 'Configure')
        start_time = ET.SubElement(configure, 'StartDateTime')
        start_time.text = self.now()
        end_time = ET.SubElement(configure, 'EndDateTime')
        end_time.text = self.now()
        command = ET.SubElement(configure, "ConfigureCommand")
        command.text = "spack install"
        status = ET.SubElement(configure, "ConfigureStatus")
        status.text = '0'
        minutes = ET.SubElement(configure, "ElapsedMinutes")
        minutes.text = '0.0'
        log = ET.SubElement(configure, 'Log')
        log.text = str(self.spec)
        return report

    def prepare_build_report(self):
        report = self.create_template()
        build = ET.SubElement(report, 'Build')
        start_element = ET.SubElement(build, 'StartDateTime')
        start_element.text = self.now()
        command_element = ET.SubElement(build, 'BuildCommand')
        command_element.text = 'spack install'
        log_element = ET.SubElement(build, 'Log')
        log_element.set('Encoding', 'base64')
        stop_element = ET.SubElement(build, 'EndDateTime')
        stop_element.text = self.now()
        return report

    def prepare_test_report(self):
        report = self.create_template()
        testing = ET.SubElement(report, 'Testing')
        testlist = ET.SubElement(testing, 'TestList')
        for item in self.tests:
            test_element = ET.SubElement(testlist, "Test")
            test_element.text = item.name
            testing.append(item.element)
        return report


def dashboard_output(spec, test_suite):
    # Cycle once and for all on the dependencies and skip
    # the ones that are already installed. This ensures that
    # for the same spec, the same number of entries will be
    # displayed in the XML report
    for x in spec.traverse(order='post'):
        package = spack.repo.get(x)
        if package.installed:
            test_case = test_suite.create_testcase(package.name, x.short_spec)
            test_case.set_duration(0.0)
            test_case.set_result(
                TestResult.SKIPPED,
                message='Skipped [already installed]',
                error_type='already_installed'
            )

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, ** kwargs):

            # Check if the package has been installed already
            if self.installed:
                return

            test_case = test_suite.create_testcase(self.name,
                                                   self.spec.short_spec)
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
                    TestResult.ERRORED,
                    message='Unable to fetch package',
                    text=text
                )
            except Exception:
                # Anything else is also an error
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.ERRORED,
                    message='Unexpected exception thrown during install',
                    text=text
                )
            except:
                # Anything else is also an error
                duration = time.time() - start_time
                test_case.set_duration(duration)
                text = fetch_text(self.build_log_path)
                test_case.set_result(
                    TestResult.ERRORED,
                    message='Unknown error',
                    text=text
                )

        return wrapper
    return decorator


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
        'restage': args.restage,
        'install_deps': 'dependencies' in args.things_to_install,
        'make_jobs': args.jobs,
        'run_tests': args.run_tests,
        'verbose': args.verbose,
        'fake': args.fake,
        'dirty': args.dirty
    })

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

    test_suites = {"junit": JUnitTestSuite,
                   "cdash": CDashTestSuite}

    for spec in specs:
        # Check if we were asked to produce some log for dashboards
        if args.log_format is not None:
            # Create the test suite in which to log results
            test_suite = test_suites[args.log_format](spec, args.log_file)
            # Decorate PackageBase.do_install to get installation status
            PackageBase.do_install = dashboard_output(
                spec, test_suite
            )(PackageBase.do_install)

        # Do the actual installation
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

        # Dump log file if asked to
        if args.log_format is not None:
            test_suite.dump()
