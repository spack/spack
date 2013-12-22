"""
Test for multi_method dispatch.
"""
import unittest

import spack.packages as packages
from spack.multimethod import *
from spack.version import *
from spack.spec import Spec
from spack.multimethod import when
from spack.test.mock_packages_test import *


class MultiMethodTest(MockPackagesTest):

    def test_no_version_match(self):
        pkg = packages.get('multimethod@2.0')
        self.assertRaises(NoSuchMethodVersionError, pkg.no_version_2)

    def test_one_version_match(self):
        pkg = packages.get('multimethod@1.0')
        self.assertEqual(pkg.no_version_2(), 1)

        pkg = packages.get('multimethod@3.0')
        self.assertEqual(pkg.no_version_2(), 3)

        pkg = packages.get('multimethod@4.0')
        self.assertEqual(pkg.no_version_2(), 4)


    def test_multiple_matches(self):
        pkg = packages.get('multimethod@3.0')
        self.assertRaises(AmbiguousMethodVersionError, pkg.version_overlap)

