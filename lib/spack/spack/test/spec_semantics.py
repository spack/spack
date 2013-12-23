import unittest
from spack.spec import *
from spack.test.mock_packages_test import *

class SpecSematicsTest(MockPackagesTest):
    """This tests satisfies(), constrain() and other semantic operations
       on specs."""

    # ================================================================================
    # Utility functions to set everything up.
    # ================================================================================
    def check_satisfies(self, lspec, rspec):
        l, r = Spec(lspec), Spec(rspec)
        self.assertTrue(l.satisfies(r))
        self.assertTrue(r.satisfies(l))

        try:
            l.constrain(r)
            r.constrain(l)
        except SpecError, e:
            self.fail("Got a SpecError in constrain!", e.message)


    def check_unsatisfiable(self, lspec, rspec):
        l, r = Spec(lspec), Spec(rspec)
        self.assertFalse(l.satisfies(r))
        self.assertFalse(r.satisfies(l))

        self.assertRaises(UnsatisfiableSpecError, l.constrain, r)
        self.assertRaises(UnsatisfiableSpecError, r.constrain, l)


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
        self.check_satisfies('libelf@0.8.13', 'libelf@0:1')
        self.check_satisfies('libdwarf^libelf@0.8.13', 'libdwarf^libelf@0:1')


    def test_satisfies_compiler(self):
        self.check_satisfies('foo%gcc', 'foo%gcc')
        self.check_satisfies('foo%intel', 'foo%intel')
        self.check_unsatisfiable('foo%intel', 'foo%gcc')
        self.check_unsatisfiable('foo%intel', 'foo%pgi')


    def test_satisfies_compiler_version(self):
        self.check_satisfies('foo%gcc', 'foo%gcc@4.7.2')
        self.check_satisfies('foo%intel', 'foo%intel@4.7.2')

        self.check_satisfies('foo%pgi@4.5', 'foo%pgi@4.4:4.6')
        self.check_satisfies('foo@2.0%pgi@4.5', 'foo@1:3%pgi@4.4:4.6')

        self.check_unsatisfiable('foo%pgi@4.3', 'foo%pgi@4.4:4.6')
        self.check_unsatisfiable('foo@4.0%pgi', 'foo@1:3%pgi')
        self.check_unsatisfiable('foo@4.0%pgi@4.5', 'foo@1:3%pgi@4.4:4.6')


    def test_satisfies_architecture(self):
        self.check_satisfies('foo=chaos_5_x86_64_ib', 'foo=chaos_5_x86_64_ib')
        self.check_satisfies('foo=bgqos_0', 'foo=bgqos_0')

        self.check_unsatisfiable('foo=bgqos_0', 'foo=chaos_5_x86_64_ib')
        self.check_unsatisfiable('foo=chaos_5_x86_64_ib', 'foo=bgqos_0')


    def test_satisfies_dependencies(self):
        self.check_satisfies('mpileaks^mpich', 'mpileaks^mpich')
        self.check_satisfies('mpileaks^zmpi', 'mpileaks^zmpi')

        self.check_unsatisfiable('mpileaks^mpich', 'mpileaks^zmpi')
        self.check_unsatisfiable('mpileaks^zmpi', 'mpileaks^mpich')


    def test_satisfies_dependency_versions(self):
        self.check_satisfies('mpileaks^mpich@2.0', 'mpileaks^mpich@1:3')
        self.check_unsatisfiable('mpileaks^mpich@1.2', 'mpileaks^mpich@2.0')

        self.check_satisfies('mpileaks^mpich@2.0^callpath@1.5', 'mpileaks^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable('mpileaks^mpich@4.0^callpath@1.5', 'mpileaks^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable('mpileaks^mpich@2.0^callpath@1.7', 'mpileaks^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable('mpileaks^mpich@4.0^callpath@1.7', 'mpileaks^mpich@1:3^callpath@1.4:1.6')


    def test_satisfies_virtual_dependencies(self):
        self.check_satisfies('mpileaks^mpi', 'mpileaks^mpi')
        self.check_satisfies('mpileaks^mpi', 'mpileaks^mpich')

        self.check_satisfies('mpileaks^mpi', 'mpileaks^zmpi')
        self.check_unsatisfiable('mpileaks^mpich', 'mpileaks^zmpi')


    def test_satisfies_virtual_dependency_versions(self):
        self.check_satisfies('mpileaks^mpi@1.5', 'mpileaks^mpi@1.2:1.6')
        self.check_unsatisfiable('mpileaks^mpi@3', 'mpileaks^mpi@1.2:1.6')

        self.check_satisfies('mpileaks^mpi@2:', 'mpileaks^mpich')
        self.check_satisfies('mpileaks^mpi@2:', 'mpileaks^mpich@3.0.4')
        self.check_satisfies('mpileaks^mpi@2:', 'mpileaks^mpich2@1.4')

        self.check_satisfies('mpileaks^mpi@1:', 'mpileaks^mpich2')
        self.check_satisfies('mpileaks^mpi@2:', 'mpileaks^mpich2')

        self.check_unsatisfiable('mpileaks^mpi@3:', 'mpileaks^mpich2@1.4')
        self.check_unsatisfiable('mpileaks^mpi@3:', 'mpileaks^mpich2')
        self.check_unsatisfiable('mpileaks^mpi@3:', 'mpileaks^mpich@1.0')


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
