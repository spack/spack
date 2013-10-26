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


    def check_concretize(self, abstract_spec, *presets):
        abstract = Spec(abstract_spec)
        concrete = abstract.concretized(*presets)

        self.assertFalse(abstract.concrete)
        self.assertTrue(concrete.concrete)
        self.check_spec(abstract, concrete)

        return concrete


    def check_presets(self, abstract, *presets):
        abstract = Spec(abstract)
        concrete = self.check_concretize(abstract, *presets)

        flat_deps = concrete.flat_dependencies()
        for preset in presets:
            preset_spec = Spec(preset)
            name = preset_spec.name

            self.assertTrue(name in flat_deps)
            self.check_spec(preset_spec, flat_deps[name])

        return concrete


    def test_concretize_no_deps(self):
        self.check_concretize('libelf')
        self.check_concretize('libelf@0.8.13')


    def test_concretize_dag(self):
        self.check_concretize('mpileaks')
        self.check_concretize('callpath')


    def test_concretize_with_presets(self):
        self.check_presets('mpileaks', 'callpath@0.8')
        self.check_presets('mpileaks', 'callpath@0.9', 'dyninst@8.0+debug')
        self.check_concretize('callpath', 'libelf@0.8.13+debug~foo', 'mpich@1.0')
