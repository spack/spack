"""
These tests check validation of dummy packages.  You can find the dummy
packages directories that these tests use in:

    spack/lib/spack/spack/test/mock_packages

Each test validates conditions with the packages in those directories.
"""
import spack
import spack.package
import spack.packages as packages

from spack.util.lang import new_path, list_modules
from spack.spec import Spec
from spack.test.mock_packages_test import *

mock_packages_path = new_path(spack.module_path, 'test', 'mock_packages')


class ValidationTest(MockPackagesTest):

    def test_conflicting_package_constraints(self):
        set_pkg_dep('mpileaks', 'mpich@1.0')
        set_pkg_dep('callpath', 'mpich@2.0')

        spec = Spec('mpileaks ^mpich ^callpath ^dyninst ^libelf ^libdwarf')
        self.assertRaises(spack.package.InvalidPackageDependencyError,
                          spec.package.validate_dependencies)


    def test_conflicting_spec_constraints(self):
        mpileaks = Spec('mpileaks ^mpich ^callpath ^dyninst ^libelf ^libdwarf')
        try:
            mpileaks.package.validate_dependencies()
        except spack.package.InvalidPackageDependencyError, e:
            self.fail("validate_dependencies raised an exception: %s", e.message)

        # Normalize then add conflicting constraints to the DAG (this is an
        # extremely unlikely scenario, but we test for it anyway)
        mpileaks.normalize()
        mpileaks.dependencies['mpich'] = Spec('mpich@1.0')
        mpileaks.dependencies['callpath'].dependencies['mpich'] = Spec('mpich@2.0')

        self.assertRaises(spack.spec.InconsistentSpecError, mpileaks.flatten)


    def test_normalize_twice(self):
        """Make sure normalize can be run twice on the same spec,
           and that it is idempotent."""
        spec = Spec('mpileaks')
        spec.normalize()
        n1 = spec.copy()

        spec.normalize()
        self.assertEqual(n1, spec)


    def test_normalize_a_lot(self):
        spec = Spec('mpileaks')
        spec.normalize()
        spec.normalize()
        spec.normalize()
        spec.normalize()


    def test_unsatisfiable_version(self):
        set_pkg_dep('mpileaks', 'mpich@1.0')
        spec = Spec('mpileaks ^mpich@2.0 ^callpath ^dyninst ^libelf ^libdwarf')
        self.assertRaises(spack.spec.UnsatisfiableVersionSpecError, spec.normalize)


    def test_unsatisfiable_compiler(self):
        set_pkg_dep('mpileaks', 'mpich%gcc')
        spec = Spec('mpileaks ^mpich%intel ^callpath ^dyninst ^libelf ^libdwarf')
        self.assertRaises(spack.spec.UnsatisfiableCompilerSpecError, spec.normalize)


    def test_unsatisfiable_compiler_version(self):
        set_pkg_dep('mpileaks', 'mpich%gcc@4.6')
        spec = Spec('mpileaks ^mpich%gcc@4.5 ^callpath ^dyninst ^libelf ^libdwarf')
        self.assertRaises(spack.spec.UnsatisfiableCompilerSpecError, spec.normalize)


    def test_unsatisfiable_variant(self):
        set_pkg_dep('mpileaks', 'mpich+debug')
        spec = Spec('mpileaks ^mpich~debug ^callpath ^dyninst ^libelf ^libdwarf')
        self.assertRaises(spack.spec.UnsatisfiableVariantSpecError, spec.normalize)


    def test_unsatisfiable_architecture(self):
        set_pkg_dep('mpileaks', 'mpich=bgqos_0')
        spec = Spec('mpileaks ^mpich=sles_10_ppc64 ^callpath ^dyninst ^libelf ^libdwarf')
        self.assertRaises(spack.spec.UnsatisfiableArchitectureSpecError, spec.normalize)


    def test_invalid_dep(self):
        spec = Spec('libelf ^mpich')
        self.assertRaises(spack.spec.InvalidDependencyException, spec.normalize)

        spec = Spec('libelf ^libdwarf')
        self.assertRaises(spack.spec.InvalidDependencyException, spec.normalize)

        spec = Spec('mpich ^dyninst ^libelf')
        self.assertRaises(spack.spec.InvalidDependencyException, spec.normalize)


    def test_equal(self):
        spec = Spec('mpileaks ^callpath ^libelf ^libdwarf')
        self.assertNotEqual(spec, Spec(
            'mpileaks', Spec('callpath',
                             Spec('libdwarf',
                                  Spec('libelf')))))
        self.assertNotEqual(spec, Spec(
            'mpileaks', Spec('callpath',
                             Spec('libelf',
                                  Spec('libdwarf')))))

        self.assertEqual(spec, Spec(
            'mpileaks', Spec('callpath'), Spec('libdwarf'), Spec('libelf')))

        self.assertEqual(spec, Spec(
            'mpileaks', Spec('libelf'), Spec('libdwarf'), Spec('callpath')))


    def test_normalize_mpileaks(self):
        spec = Spec('mpileaks ^mpich ^callpath ^dyninst ^libelf@1.8.11 ^libdwarf')

        expected_flat = Spec(
            'mpileaks', Spec('mpich'), Spec('callpath'), Spec('dyninst'),
            Spec('libelf@1.8.11'), Spec('libdwarf'))

        mpich = Spec('mpich')
        libelf = Spec('libelf@1.8.11')
        expected_normalized = Spec(
            'mpileaks',
            Spec('callpath',
                 Spec('dyninst', Spec('libdwarf', libelf),
                      libelf),
                 mpich), mpich)

        expected_non_dag = Spec(
            'mpileaks',
            Spec('callpath',
                 Spec('dyninst', Spec('libdwarf', Spec('libelf@1.8.11')),
                      Spec('libelf@1.8.11')),
                 mpich), Spec('mpich'))

        self.assertEqual(expected_normalized, expected_non_dag)

        self.assertEqual(str(expected_normalized), str(expected_non_dag))
        self.assertEqual(str(spec), str(expected_non_dag))
        self.assertEqual(str(expected_normalized), str(spec))

        self.assertEqual(spec, expected_flat)
        self.assertNotEqual(spec, expected_normalized)
        self.assertNotEqual(spec, expected_non_dag)

        spec.normalize()

        self.assertNotEqual(spec, expected_flat)
        self.assertEqual(spec, expected_normalized)
        self.assertEqual(spec, expected_non_dag)
