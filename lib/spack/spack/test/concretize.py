import unittest
from spack.spec import Spec
from spack.test.mock_packages_test import *

class ConcretizeTest(MockPackagesTest):

    def check_spec(self, abstract, concrete):
        if abstract.versions.concrete:
            self.assertEqual(abstract.versions, concrete.versions)

        if abstract.variants:
            self.assertEqual(abstract.versions, concrete.versions)

        if abstract.compiler and abstract.compiler.concrete:
            self.assertEqual(abstract.compiler, concrete.compiler)

        if abstract.architecture and abstract.architecture.concrete:
            self.assertEqual(abstract.architecture, concrete.architecture)


    def check_concretize(self, abstract_spec):
        abstract = Spec(abstract_spec)
        concrete = abstract.concretized()

        self.assertFalse(abstract.concrete)
        self.assertTrue(concrete.concrete)
        self.check_spec(abstract, concrete)

        return concrete


    def test_concretize_no_deps(self):
        self.check_concretize('libelf')
        self.check_concretize('libelf@0.8.13')


    def test_concretize_dag(self):
        spec = Spec('mpileaks')
        spec.normalize()

        self.check_concretize('callpath')
        self.check_concretize('mpileaks')
