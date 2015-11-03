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
import xml.etree.ElementTree as ET
import itertools
import os

from llnl.util.filesystem import *

class JunitResultFormat(object):
    def __init__(self):
        self.root = ET.Element('testsuite')
        self.tests = []
        
    def add_test(self, testId, testStatus, testInfo=None):
        self.tests.append((testId, testStatus, testInfo))
    
    def write_to(self, stream):
        self.root.set('tests', '{0}'.format(len(self.tests)))
        for testId, testStatus, testInfo in self.tests:
            testcase = ET.SubElement(self.root, 'testcase')
            testcase.set('classname', testId.groupId)
            testcase.set('name', testId.name)
            if testStatus == TestStatus.FAILED:
                failure = ET.SubElement(testcase, 'failure')
                failure.set('type', "Test Failure")
                failure.text = testInfo
            elif testStatus == TestStatus.SKIPPED:
                skipped = ET.SubElement(testcase, 'skipped')
                skipped.set('type', "Test Skipped")
                skipped.text = testInfo
            elif testStatus == TestStatus.ERROR:
                error = ET.SubElement(testcase, 'error')
                error.set('type', "Test Error")
                error.text = testInfo
        ET.ElementTree(self.root).write(stream)


def generate_output_format(suite, testResult, output):
    allTests = set(itertools.chain.from_iterable(suite))

    for testCase, tracebackMsg in testResult.failures:
        testId = TestId(str(testCase), testCase.__class__.__name__)
        output.add_test(testId, TestStatus.FAILED, tracebackMsg)
    
    for testCase, tracebackMsg in testResult.errors:
        testId = TestId(str(testCase), testCase.__class__.__name__)
        output.add_test(testId, TestStatus.ERROR, tracebackMsg)

    
    successfulTests = allTests - set(x for x, y in itertools.chain(
            testResult.failures, testResult.errors))
    
    for testCase in successfulTests:
        testId = TestId(str(testCase), testCase.__class__.__name__)
        output.add_test(testId, TestStatus.PASSED)


class TestStatus(object):
    PASSED = 0
    FAILED = 1
    SKIPPED = 2
    ERROR = 3
    

def test_output_path(fileName):
    """
    Given a file name, return a full path to a test file. Does not check if the
    file already exists.
    """
    outputDir = join_path(os.getcwd(), "test-output")
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    return join_path(outputDir, fileName)


class TestId(object):
    def __init__(self, name, groupId=None):
        self.name = name
        self.groupId = groupId if groupId else name
    
    def __hash__(self):
        return hash((self.name, self.groupId))
    
    def __eq__(self, other):
        if not isinstance(other, TestId):
            return False
            
        return ((self.name, self.groupId) == (other.name, other.groupId))
