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
from external import argparse
import xml.etree.ElementTree as ET
import itertools
import re

import llnl.util.tty as tty
from llnl.util.filesystem import *

import spack
import spack.cmd

description = "Build and install packages"

def setup_parser(subparser):
    subparser.add_argument(
        '-j', '--jobs', action='store', type=int,
        help="Explicitly set number of make jobs.  Default is #cpus.")
    
    subparser.add_argument(
        '-n', '--no-checksum', action='store_true', dest='no_checksum',
        help="Do not check packages against checksum")
    
    subparser.add_argument(
        'output', help="test output goes in this file")
    
    subparser.add_argument(
        'package', help="spec of package to install")


class JunitResultFormat(object):
    def __init__(self):
        self.root = ET.Element('testsuite')
        self.tests = []
        
    def add_test(self, buildId, passed=True, buildInfo=None):
        self.tests.append((buildId, passed, buildInfo))
    
    def write_to(self, stream):
        self.root.set('tests', '{0}'.format(len(self.tests)))
        for buildId, passed, buildInfo in self.tests:
            testcase = ET.SubElement(self.root, 'testcase')
            testcase.set('classname', buildId.name)
            testcase.set('name', buildId.stringId())
            if not passed:
                failure = ET.SubElement(testcase, 'failure')
                failure.set('type', "Build Error")
                failure.text = buildInfo
        ET.ElementTree(self.root).write(stream)


class BuildId(object):
    def __init__(self, name, version, hashId):
        self.name = name
        self.version = version
        self.hashId = hashId
    
    def stringId(self):
        return "-".join(str(x) for x in (self.name, self.version, self.hashId))


def create_test_output(topSpec, newInstalls, output):
    # Post-order traversal is not strictly required but it makes sense to output 
    # tests for dependencies first.
    for spec in topSpec.traverse(order='post'):
        if spec not in newInstalls:
            continue

        if not all(spack.db.get(childSpec).installed for childSpec in 
                spec.dependencies.itervalues()):
            #TODO: create a failed test if a dependency didn't install?
            continue
                
        bId = BuildId(spec.name, spec.version, spec.dag_hash())

        package = spack.db.get(spec)
        if package.installed:
            buildLogPath = spack.install_layout.build_log_path(spec)
        else:
            #TODO: search recursively under stage.path instead of only within
            #    stage.source_path
            buildLogPath = join_path(package.stage.source_path, 'spack-build.out')            

        with open(buildLogPath, 'rb') as F:
            lines = F.readlines()
            errMessages = list(line for line in lines if
                re.search('error:', line, re.IGNORECASE))
            errOutput = errMessages if errMessages else lines[-10:]
            errOutput = '\n'.join(itertools.chain(
                    [spec.to_yaml(), "Errors:"], errOutput, 
                    ["Build Log:", buildLogPath]))
            
            output.add_test(bId, package.installed, errOutput)
        

def test_install(parser, args):
    if not args.package:
        tty.die("install requires a package argument")

    if args.jobs is not None:
        if args.jobs <= 0:
            tty.die("The -j option must be a positive integer!")

    if args.no_checksum:
        spack.do_checksum = False        # TODO: remove this global.

    #TODO: should a single argument be wrapped in a list?
    specs = spack.cmd.parse_specs(args.package, concretize=True)
    newInstalls = set()
    for spec in itertools.chain.from_iterable(spec.traverse() 
            for spec in specs):
        package = spack.db.get(spec)
        if not package.installed:
            newInstalls.add(spec)
    
    try:
        for spec in specs:
            package = spack.db.get(spec)
            if not package.installed:
                package.do_install(
                    keep_prefix=False,
                    keep_stage=False,
                    ignore_deps=False,
                    make_jobs=args.jobs,
                    verbose=True,
                    fake=False)
    finally:        
        jrf = JunitResultFormat()
        handled = {}
        for spec in specs:
            create_test_output(spec, newInstalls, jrf)

        with open(args.output, 'wb') as F:
            jrf.write_to(F)
