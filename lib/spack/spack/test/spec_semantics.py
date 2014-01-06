import unittest
from spack.spec import *
from spack.test.mock_packages_test import *

class SpecSematicsTest(MockPackagesTest):
    """This tests satisfies(), constrain() and other semantic operations
       on specs."""

    # ================================================================================
    # Utility functions to set everything up.
    # ================================================================================
    def check_satisfies(self, spec, anon_spec):
        left = Spec(spec)
        right = parse_anonymous_spec(anon_spec, left.name)

        self.assertTrue(left.satisfies(right))
        self.assertTrue(left.satisfies(anon_spec))
        self.assertTrue(right.satisfies(left))

        try:
            left.copy().constrain(right)
            left.copy().constrain(anon_spec)
            right.copy().constrain(left)
        except SpecError, e:
            self.fail("Got a SpecError in constrain!  " + e.message)


    def check_unsatisfiable(self, spec, anon_spec):
        left = Spec(spec)
        right = parse_anonymous_spec(anon_spec, left.name)

        self.assertFalse(left.satisfies(right))
        self.assertFalse(left.satisfies(anon_spec))

        self.assertFalse(right.satisfies(left))

        self.assertRaises(UnsatisfiableSpecError, left.constrain, right)
        self.assertRaises(UnsatisfiableSpecError, left.constrain, anon_spec)
        self.assertRaises(UnsatisfiableSpecError, right.constrain, left)


    def check_constrain(self, expected, constrained, constraint):
        exp = Spec(expected)
        constrained = Spec(constrained)
        constraint = Spec(constraint)
        constrained.constrain(constraint)
        self.assertEqual(exp, constrained)


    def check_invalid_constraint(self, constrained, constraint):
        constrained = Spec(constrained)
        constraint = Spec(constraint)
        self.assertRaises(UnsatisfiableSpecError, constrained.constrain, constraint)


    # ================================================================================
    # Satisfiability and constraints
    # ================================================================================
    def test_satisfies(self):
        self.check_satisfies('libelf@0.8.13', '@0:1')
        self.check_satisfies('libdwarf^libelf@0.8.13', '^libelf@0:1')


    def test_satisfies_compiler(self):
        self.check_satisfies('foo%gcc', '%gcc')
        self.check_satisfies('foo%intel', '%intel')
        self.check_unsatisfiable('foo%intel', '%gcc')
        self.check_unsatisfiable('foo%intel', '%pgi')


    def test_satisfies_compiler_version(self):
        self.check_satisfies('foo%gcc', '%gcc@4.7.2')
        self.check_satisfies('foo%intel', '%intel@4.7.2')

        self.check_satisfies('foo%pgi@4.5', '%pgi@4.4:4.6')
        self.check_satisfies('foo@2.0%pgi@4.5', '@1:3%pgi@4.4:4.6')

        self.check_unsatisfiable('foo%pgi@4.3', '%pgi@4.4:4.6')
        self.check_unsatisfiable('foo@4.0%pgi', '@1:3%pgi')
        self.check_unsatisfiable('foo@4.0%pgi@4.5', '@1:3%pgi@4.4:4.6')


    def test_satisfies_architecture(self):
        self.check_satisfies('foo=chaos_5_x86_64_ib', '=chaos_5_x86_64_ib')
        self.check_satisfies('foo=bgqos_0', '=bgqos_0')

        self.check_unsatisfiable('foo=bgqos_0', '=chaos_5_x86_64_ib')
        self.check_unsatisfiable('foo=chaos_5_x86_64_ib', '=bgqos_0')


    def test_satisfies_dependencies(self):
        self.check_satisfies('mpileaks^mpich', '^mpich')
        self.check_satisfies('mpileaks^zmpi', '^zmpi')

        self.check_unsatisfiable('mpileaks^mpich', '^zmpi')
        self.check_unsatisfiable('mpileaks^zmpi', '^mpich')


    def test_satisfies_dependency_versions(self):
        self.check_satisfies('mpileaks^mpich@2.0', '^mpich@1:3')
        self.check_unsatisfiable('mpileaks^mpich@1.2', '^mpich@2.0')

        self.check_satisfies('mpileaks^mpich@2.0^callpath@1.5', '^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable('mpileaks^mpich@4.0^callpath@1.5', '^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable('mpileaks^mpich@2.0^callpath@1.7', '^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable('mpileaks^mpich@4.0^callpath@1.7', '^mpich@1:3^callpath@1.4:1.6')


    def test_satisfies_virtual_dependencies(self):
        self.check_satisfies('mpileaks^mpi', '^mpi')
        self.check_satisfies('mpileaks^mpi', '^mpich')

        self.check_satisfies('mpileaks^mpi', '^zmpi')
        self.check_unsatisfiable('mpileaks^mpich', '^zmpi')


    def test_satisfies_virtual_dependency_versions(self):
        self.check_satisfies('mpileaks^mpi@1.5', '^mpi@1.2:1.6')
        self.check_unsatisfiable('mpileaks^mpi@3', '^mpi@1.2:1.6')

        self.check_satisfies('mpileaks^mpi@2:', '^mpich')
        self.check_satisfies('mpileaks^mpi@2:', '^mpich@3.0.4')
        self.check_satisfies('mpileaks^mpi@2:', '^mpich2@1.4')

        self.check_satisfies('mpileaks^mpi@1:', '^mpich2')
        self.check_satisfies('mpileaks^mpi@2:', '^mpich2')

        self.check_unsatisfiable('mpileaks^mpi@3:', '^mpich2@1.4')
        self.check_unsatisfiable('mpileaks^mpi@3:', '^mpich2')
        self.check_unsatisfiable('mpileaks^mpi@3:', '^mpich@1.0')


    def test_constrain(self):
        self.check_constrain('libelf@2.1:2.5', 'libelf@0:2.5', 'libelf@2.1:3')
        self.check_constrain('libelf@2.1:2.5%gcc@4.5:4.6',
                             'libelf@0:2.5%gcc@2:4.6', 'libelf@2.1:3%gcc@4.5:4.7')

        self.check_constrain('libelf+debug+foo', 'libelf+debug', 'libelf+foo')
        self.check_constrain('libelf+debug+foo', 'libelf+debug', 'libelf+debug+foo')

        self.check_constrain('libelf+debug~foo', 'libelf+debug', 'libelf~foo')
        self.check_constrain('libelf+debug~foo', 'libelf+debug', 'libelf+debug~foo')

        self.check_constrain('libelf=bgqos_0', 'libelf=bgqos_0', 'libelf=bgqos_0')
        self.check_constrain('libelf=bgqos_0', 'libelf', 'libelf=bgqos_0')


    def test_invalid_constraint(self):
        self.check_invalid_constraint('libelf@0:2.0', 'libelf@2.1:3')
        self.check_invalid_constraint('libelf@0:2.5%gcc@4.8:4.9', 'libelf@2.1:3%gcc@4.5:4.7')

        self.check_invalid_constraint('libelf+debug', 'libelf~debug')
        self.check_invalid_constraint('libelf+debug~foo', 'libelf+debug+foo')

        self.check_invalid_constraint('libelf=bgqos_0', 'libelf=x86_54')
