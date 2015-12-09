##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import unittest
import itertools

import spack
test_install = __import__("spack.cmd.test-install", 
    fromlist=["BuildId", "create_test_output", "TestResult"])

class MockOutput(object):
    def __init__(self):
        self.results = {}
    
    def add_test(self, buildId, passed=True, buildInfo=None):
        self.results[buildId] = passed
    
    def write_to(self, stream):
        pass

class MockSpec(object):
    def __init__(self, name, version, hashStr=None):
        self.dependencies = {}
        self.name = name
        self.version = version
        self.hash = hashStr if hashStr else hash((name, version))
    
    def traverse(self, order=None):
        allDeps = itertools.chain.from_iterable(i.traverse() for i in 
            self.dependencies.itervalues())
        return set(itertools.chain([self], allDeps))
    
    def dag_hash(self):
        return self.hash 

    def to_yaml(self):
        return "<<<MOCK YAML {0}>>>".format(test_install.BuildId(self).stringId())

class MockPackage(object):
    def __init__(self, buildLogPath):
        self.installed = False
        self.build_log_path = buildLogPath

specX = MockSpec("X", "1.2.0")
specY = MockSpec("Y", "2.3.8")
specX.dependencies['Y'] = specY
pkgX = MockPackage('logX')
pkgY = MockPackage('logY')
bIdX = test_install.BuildId(specX)
bIdY = test_install.BuildId(specY)

class UnitInstallTest(unittest.TestCase):
    """Tests test-install where X->Y"""

    def setUp(self):
        super(UnitInstallTest, self).setUp()
        
        pkgX.installed = False
        pkgY.installed = False

        pkgDb = MockPackageDb({specX:pkgX, specY:pkgY})
        spack.db = pkgDb

    def tearDown(self):
        super(UnitInstallTest, self).tearDown()
        
    def test_installing_both(self):
        mo = MockOutput()
        
        pkgX.installed = True
        pkgY.installed = True
        test_install.create_test_output(specX, [specX, specY], mo, getLogFunc=test_fetch_log)
        
        self.assertEqual(mo.results, 
            {bIdX:test_install.TestResult.PASSED, 
            bIdY:test_install.TestResult.PASSED})

    def test_dependency_already_installed(self):
        mo = MockOutput()
        
        pkgX.installed = True
        pkgY.installed = True
        test_install.create_test_output(specX, [specX], mo, getLogFunc=test_fetch_log)
        
        self.assertEqual(mo.results, {bIdX:test_install.TestResult.PASSED})

    #TODO: add test(s) where Y fails to install

class MockPackageDb(object):
    def __init__(self, init=None):
        self.specToPkg = {}
        if init:
            self.specToPkg.update(init)
        
    def get(self, spec):
        return self.specToPkg[spec]

def test_fetch_log(path):
    return []

