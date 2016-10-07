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
import codecs
import os
import time
import xml.dom.minidom
import xml.etree.ElementTree as ET

import llnl.util.tty as tty
import spack
import spack.cmd
from llnl.util.filesystem import *
from spack.build_environment import InstallError
from spack.fetch_strategy import FetchError

description = "Run package install as a unit test, output formatted results."


def setup_parser(subparser):
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="Explicitly set number of make jobs.  Default is #cpus.")

    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="Do not check packages against checksum")

    subparser.add_argument(
        '-o', '--output', action='store',
        help="test output goes in this file")

    subparser.add_argument(
        'package', nargs=argparse.REMAINDER,
        help="spec of package to install")


class TestResult(object):
    PASSED = 0
    FAILED = 1
    SKIPPED = 2
    ERRORED = 3


class TestSuite(object):

    def __init__(self, filename):
        self.filename = filename
        self.root = ET.Element('testsuite')
        self.tests = []

    def __enter__(self):
        return self

    def append(self, item):
        if not isinstance(item, TestCase):
            raise TypeError(
                'only TestCase instances may be appended to TestSuite')
        self.tests.append(item)  # Append the item to the list of tests

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Prepare the header for the entire test suite
        number_of_errors = sum(
            x.result_type == TestResult.ERRORED for x in self.tests)
        self.root.set('errors', str(number_of_errors))
        number_of_failures = sum(
            x.result_type == TestResult.FAILED for x in self.tests)
        self.root.set('failures', str(number_of_failures))
        self.root.set('tests', str(len(self.tests)))

        for item in self.tests:
            self.root.append(item.element)

        with open(self.filename, 'wb') as file:
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

    def __init__(self, classname, name, time=None):
        self.element = ET.Element('testcase')
        self.element.set('classname', str(classname))
        self.element.set('name', str(name))
        if time is not None:
            self.element.set('time', str(time))
        self.result_type = None

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


def fetch_log(path):
    if not os.path.exists(path):
        return list()
    with codecs.open(path, 'rb', 'utf-8') as F:
        return list(line.strip() for line in F.readlines())


def failed_dependencies(spec):
    def get_deps(deptype):
        return set(item for item in spec.dependencies(deptype)
                   if not spack.repo.get(item).installed)
    link_deps = get_deps('link')
    run_deps = get_deps('run')
    return link_deps.union(run_deps)


def get_top_spec_or_die(args):
    specs = spack.cmd.parse_specs(args.package, concretize=True)
    if len(specs) > 1:
        tty.die("Only 1 top-level package can be specified")
    top_spec = iter(specs).next()
    return top_spec


def install_single_spec(spec, number_of_jobs):
    package = spack.repo.get(spec)

    # If it is already installed, skip the test
    if spack.repo.get(spec).installed:
        testcase = TestCase(package.name, package.spec.short_spec, time=0.0)
        testcase.set_result(
            TestResult.SKIPPED,
            message='Skipped [already installed]',
            error_type='already_installed')
        return testcase

    # If it relies on dependencies that did not install, skip
    if failed_dependencies(spec):
        testcase = TestCase(package.name, package.spec.short_spec, time=0.0)
        testcase.set_result(
            TestResult.SKIPPED,
            message='Skipped [failed dependencies]',
            error_type='dep_failed')
        return testcase

    # Otherwise try to install the spec
    try:
        start_time = time.time()
        package.do_install(keep_prefix=False,
                           keep_stage=True,
                           install_deps=True,
                           make_jobs=number_of_jobs,
                           verbose=True,
                           fake=False)
        duration = time.time() - start_time
        testcase = TestCase(package.name, package.spec.short_spec, duration)
        testcase.set_result(TestResult.PASSED)
    except InstallError:
        # An InstallError is considered a failure (the recipe didn't work
        # correctly)
        duration = time.time() - start_time
        # Try to get the log
        lines = fetch_log(package.build_log_path)
        text = '\n'.join(lines)
        testcase = TestCase(package.name, package.spec.short_spec, duration)
        testcase.set_result(TestResult.FAILED,
                            message='Installation failure', text=text)

    except FetchError:
        # A FetchError is considered an error (we didn't even start building)
        duration = time.time() - start_time
        testcase = TestCase(package.name, package.spec.short_spec, duration)
        testcase.set_result(TestResult.ERRORED,
                            message='Unable to fetch package')

    return testcase


def get_filename(args, top_spec):
    if not args.output:
        fname = 'test-{x.name}-{x.version}-{hash}.xml'.format(
            x=top_spec, hash=top_spec.dag_hash())
        output_directory = join_path(os.getcwd(), 'test-output')
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)
        output_filename = join_path(output_directory, fname)
    else:
        output_filename = args.output
    return output_filename


def test_install(parser, args):
    # Check the input
    if not args.package:
        tty.die("install requires a package argument")

    if args.jobs is not None:
        if args.jobs <= 0:
            tty.die("The -j option must be a positive integer!")

    if args.no_checksum:
        spack.do_checksum = False  # TODO: remove this global.

    # Get the one and only top spec
    top_spec = get_top_spec_or_die(args)
    # Get the filename of the test
    output_filename = get_filename(args, top_spec)
    # TEST SUITE
    with TestSuite(output_filename) as test_suite:
        # Traverse in post order : each spec is a test case
        for spec in top_spec.traverse(order='post'):
            test_case = install_single_spec(spec, args.jobs)
            test_suite.append(test_case)
