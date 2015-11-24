##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
import xml.etree.ElementTree as ET
import itertools
import re
import os
import codecs

import llnl.util.tty as tty
from llnl.util.filesystem import *

import spack
from spack.build_environment import InstallError
from spack.fetch_strategy import FetchError
import spack.cmd

description = "Treat package installations as unit tests and output formatted test results"

def setup_parser(subparser):
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="Explicitly set number of make jobs.  Default is #cpus.")
    
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="Do not check packages against checksum")
    
    subparser.add_argument(
        '-o', '--output', action='store', help="test output goes in this file")
    
    subparser.add_argument(
        'package', nargs=argparse.REMAINDER, help="spec of package to install")


class JunitResultFormat(object):
    def __init__(self):
        self.root = ET.Element('testsuite')
        self.tests = []
        
    def add_test(self, buildId, testResult, buildInfo=None):
        self.tests.append((buildId, testResult, buildInfo))
    
    def write_to(self, stream):
        self.root.set('tests', '{0}'.format(len(self.tests)))
        for buildId, testResult, buildInfo in self.tests:
            testcase = ET.SubElement(self.root, 'testcase')
            testcase.set('classname', buildId.name)
            testcase.set('name', buildId.stringId())
            if testResult == TestResult.FAILED:
                failure = ET.SubElement(testcase, 'failure')
                failure.set('type', "Build Error")
                failure.text = buildInfo
            elif testResult == TestResult.SKIPPED:
                skipped = ET.SubElement(testcase, 'skipped')
                skipped.set('type', "Skipped Build")
                skipped.text = buildInfo
        ET.ElementTree(self.root).write(stream)


class TestResult(object):
    PASSED = 0
    FAILED = 1
    SKIPPED = 2
    

class BuildId(object):
    def __init__(self, spec):
        self.name = spec.name
        self.version = spec.version
        self.hashId = spec.dag_hash()
    
    def stringId(self):
        return "-".join(str(x) for x in (self.name, self.version, self.hashId))

    def __hash__(self):
        return hash((self.name, self.version, self.hashId))
    
    def __eq__(self, other):
        if not isinstance(other, BuildId):
            return False
            
        return ((self.name, self.version, self.hashId) == 
            (other.name, other.version, other.hashId))


def fetch_log(path):
    if not os.path.exists(path):
        return list()
    with codecs.open(path, 'rb', 'utf-8') as F:
        return list(line.strip() for line in F.readlines())


def failed_dependencies(spec):
    return set(childSpec for childSpec in spec.dependencies.itervalues() if not 
        spack.db.get(childSpec).installed)


def create_test_output(topSpec, newInstalls, output, getLogFunc=fetch_log):
    # Post-order traversal is not strictly required but it makes sense to output 
    # tests for dependencies first.
    for spec in topSpec.traverse(order='post'):
        if spec not in newInstalls:
            continue

        failedDeps = failed_dependencies(spec)
        package = spack.db.get(spec)
        if failedDeps:
            result = TestResult.SKIPPED
            dep = iter(failedDeps).next()
            depBID = BuildId(dep)
            errOutput = "Skipped due to failed dependency: {0}".format(
                depBID.stringId())
        elif (not package.installed) and (not package.stage.source_path):
            result = TestResult.FAILED
            errOutput = "Failure to fetch package resources."
        elif not package.installed:
            result = TestResult.FAILED
            lines = getLogFunc(package.build_log_path)
            errMessages = list(line for line in lines if
                re.search('error:', line, re.IGNORECASE))
            errOutput = errMessages if errMessages else lines[-10:]
            errOutput = '\n'.join(itertools.chain(
                    [spec.to_yaml(), "Errors:"], errOutput, 
                    ["Build Log:", package.build_log_path]))
        else:
            result = TestResult.PASSED
            errOutput = None
        
        bId = BuildId(spec)
        output.add_test(bId, result, errOutput)


def test_install(parser, args):
    if not args.package:
        tty.die("install requires a package argument")

    if args.jobs is not None:
        if args.jobs <= 0:
            tty.die("The -j option must be a positive integer!")

    if args.no_checksum:
        spack.do_checksum = False        # TODO: remove this global.
    
    specs = spack.cmd.parse_specs(args.package, concretize=True)
    if len(specs) > 1:
        tty.die("Only 1 top-level package can be specified")
    topSpec = iter(specs).next()
    
    newInstalls = set()
    for spec in topSpec.traverse():
        package = spack.db.get(spec)
        if not package.installed:
            newInstalls.add(spec)
    
    if not args.output:
        bId = BuildId(topSpec)
        outputDir = join_path(os.getcwd(), "test-output")
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        outputFpath = join_path(outputDir, "test-{0}.xml".format(bId.stringId()))
    else:
        outputFpath = args.output
    
    for spec in topSpec.traverse(order='post'):
        # Calling do_install for the top-level package would be sufficient but
        # this attempts to keep going if any package fails (other packages which
        # are not dependents may succeed)
        package = spack.db.get(spec)
        if (not failed_dependencies(spec)) and (not package.installed):
            try:
                package.do_install(
                    keep_prefix=False,
                    keep_stage=True,
                    ignore_deps=False,
                    make_jobs=args.jobs,
                    verbose=True,
                    fake=False)
            except InstallError:
                pass
            except FetchError:
                pass
   
    jrf = JunitResultFormat()
    handled = {}
    create_test_output(topSpec, newInstalls, jrf)

    with open(outputFpath, 'wb') as F:
            jrf.write_to(F)
