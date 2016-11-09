##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import spack.architecture
from spack.spec import *
from spack.test.mock_packages_test import *


class SpecSematicsTest(MockPackagesTest):
    """This tests satisfies(), constrain() and other semantic operations
       on specs."""

    # ========================================================================
    # Utility functions to set everything up.
    # ========================================================================
    def check_satisfies(self, spec, anon_spec, concrete=False):
        left = Spec(spec, concrete=concrete)
        try:
            right = Spec(anon_spec)  # if it's not anonymous, allow it.
        except:
            right = parse_anonymous_spec(anon_spec, left.name)

        # Satisfies is one-directional.
        self.assertTrue(left.satisfies(right))
        self.assertTrue(left.satisfies(anon_spec))

        # if left satisfies right, then we should be able to consrain
        # right by left.  Reverse is not always true.
        right.copy().constrain(left)

    def check_unsatisfiable(self, spec, anon_spec, concrete=False):
        left = Spec(spec, concrete=concrete)
        try:
            right = Spec(anon_spec)  # if it's not anonymous, allow it.
        except:
            right = parse_anonymous_spec(anon_spec, left.name)

        self.assertFalse(left.satisfies(right))
        self.assertFalse(left.satisfies(anon_spec))

        self.assertRaises(UnsatisfiableSpecError, right.copy().constrain, left)

    def check_constrain(self, expected, spec, constraint):
        exp = Spec(expected)
        spec = Spec(spec)
        constraint = Spec(constraint)
        spec.constrain(constraint)
        self.assertEqual(exp, spec)

    def check_constrain_changed(self, spec, constraint):
        spec = Spec(spec)
        self.assertTrue(spec.constrain(constraint))

    def check_constrain_not_changed(self, spec, constraint):
        spec = Spec(spec)
        self.assertFalse(spec.constrain(constraint))

    def check_invalid_constraint(self, spec, constraint):
        spec = Spec(spec)
        constraint = Spec(constraint)
        self.assertRaises(UnsatisfiableSpecError, spec.constrain, constraint)

    # ========================================================================
    # Satisfiability
    # ========================================================================
    def test_satisfies(self):
        self.check_satisfies('libelf@0.8.13', '@0:1')
        self.check_satisfies('libdwarf^libelf@0.8.13', '^libelf@0:1')

    def test_satisfies_namespace(self):
        self.check_satisfies('builtin.mpich', 'mpich')
        self.check_satisfies('builtin.mock.mpich', 'mpich')

        # TODO: only works for deps now, but shouldn't we allow for root spec?
        # self.check_satisfies('builtin.mock.mpich', 'mpi')

        self.check_satisfies('builtin.mock.mpich', 'builtin.mock.mpich')

        self.check_unsatisfiable('builtin.mock.mpich', 'builtin.mpich')

    def test_satisfies_namespaced_dep(self):
        """Ensure spec from same or unspecified namespace satisfies namespace
           constraint."""
        self.check_satisfies('mpileaks ^builtin.mock.mpich', '^mpich')

        self.check_satisfies('mpileaks ^builtin.mock.mpich', '^mpi')
        self.check_satisfies(
            'mpileaks ^builtin.mock.mpich', '^builtin.mock.mpich')

        self.check_unsatisfiable(
            'mpileaks ^builtin.mock.mpich', '^builtin.mpich')

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

        self.check_satisfies('foo %gcc@4.7.3', '%gcc@4.7')
        self.check_unsatisfiable('foo %gcc@4.7', '%gcc@4.7.3')

    def test_satisfies_architecture(self):
        self.check_satisfies(
            'foo platform=test',
            'platform=test')
        self.check_satisfies(
            'foo platform=test',
            'platform=test target=frontend')
        self.check_satisfies(
            'foo platform=test',
            'platform=test os=frontend target=frontend')
        self.check_satisfies(
            'foo platform=test os=frontend target=frontend',
            'platform=test')
        self.check_unsatisfiable(
            'foo platform=test',
            'platform=linux os=frontend target=frontend')

        self.check_satisfies(
            'foo arch=test-None-None',
            'platform=test')
        self.check_satisfies(
            'foo arch=test-None-frontend',
            'platform=test target=frontend')
        self.check_satisfies(
            'foo arch=test-frontend-frontend',
            'platform=test os=frontend target=frontend')
        self.check_satisfies(
            'foo arch=test-frontend-frontend',
            'platform=test')
        self.check_unsatisfiable(
            'foo arch=test-frontend-frontend',
            'platform=test os=frontend target=backend')

        self.check_satisfies(
            'foo platform=test target=frontend os=frontend',
            'platform=test target=frontend os=frontend')
        self.check_satisfies(
            'foo platform=test target=backend os=backend',
            'platform=test target=backend os=backend')
        self.check_satisfies(
            'foo platform=test target=default_target os=default_os',
            'platform=test os=default_os')
        self.check_unsatisfiable(
            'foo platform=test target=default_target os=default_os',
            'platform=linux target=default_target os=default_os')

    def test_satisfies_dependencies(self):
        self.check_satisfies('mpileaks^mpich', '^mpich')
        self.check_satisfies('mpileaks^zmpi', '^zmpi')

        self.check_unsatisfiable('mpileaks^mpich', '^zmpi')
        self.check_unsatisfiable('mpileaks^zmpi', '^mpich')

    def test_satisfies_dependency_versions(self):
        self.check_satisfies('mpileaks^mpich@2.0', '^mpich@1:3')
        self.check_unsatisfiable('mpileaks^mpich@1.2', '^mpich@2.0')

        self.check_satisfies(
            'mpileaks^mpich@2.0^callpath@1.5', '^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable(
            'mpileaks^mpich@4.0^callpath@1.5', '^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable(
            'mpileaks^mpich@2.0^callpath@1.7', '^mpich@1:3^callpath@1.4:1.6')
        self.check_unsatisfiable(
            'mpileaks^mpich@4.0^callpath@1.7', '^mpich@1:3^callpath@1.4:1.6')

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

    def test_satisfies_matching_variant(self):
        self.check_satisfies('mpich+foo', 'mpich+foo')
        self.check_satisfies('mpich~foo', 'mpich~foo')
        self.check_satisfies('mpich foo=1', 'mpich foo=1')

        # confirm that synonymous syntax works correctly
        self.check_satisfies('mpich+foo', 'mpich foo=True')
        self.check_satisfies('mpich foo=true', 'mpich+foo')
        self.check_satisfies('mpich~foo', 'mpich foo=FALSE')
        self.check_satisfies('mpich foo=False', 'mpich~foo')

    def test_satisfies_unconstrained_variant(self):
        # only asked for mpich, no constraints.  Either will do.
        self.check_satisfies('mpich+foo', 'mpich')
        self.check_satisfies('mpich~foo', 'mpich')
        self.check_satisfies('mpich foo=1', 'mpich')

    def test_unsatisfiable_variants(self):
        # This case is different depending on whether the specs are concrete.

        # 'mpich' is not concrete:
        self.check_satisfies('mpich', 'mpich+foo', False)
        self.check_satisfies('mpich', 'mpich~foo', False)
        self.check_satisfies('mpich', 'mpich foo=1', False)

        # 'mpich' is concrete:
        self.check_unsatisfiable('mpich', 'mpich+foo', True)
        self.check_unsatisfiable('mpich', 'mpich~foo', True)
        self.check_unsatisfiable('mpich', 'mpich foo=1', True)

    def test_unsatisfiable_variant_mismatch(self):
        # No matchi in specs
        self.check_unsatisfiable('mpich~foo', 'mpich+foo')
        self.check_unsatisfiable('mpich+foo', 'mpich~foo')
        self.check_unsatisfiable('mpich foo=1', 'mpich foo=2')

    def test_satisfies_matching_compiler_flag(self):
        self.check_satisfies('mpich cppflags="-O3"', 'mpich cppflags="-O3"')
        self.check_satisfies('mpich cppflags="-O3 -Wall"',
                             'mpich cppflags="-O3 -Wall"')

    def test_satisfies_unconstrained_compiler_flag(self):
        # only asked for mpich, no constraints.  Any will do.
        self.check_satisfies('mpich cppflags="-O3"', 'mpich')

    def test_unsatisfiable_compiler_flag(self):
        # This case is different depending on whether the specs are concrete.

        # 'mpich' is not concrete:
        self.check_satisfies('mpich', 'mpich cppflags="-O3"', False)

        # 'mpich' is concrete:
        self.check_unsatisfiable('mpich', 'mpich cppflags="-O3"', True)

    def test_unsatisfiable_compiler_flag_mismatch(self):
        # No matchi in specs
        self.check_unsatisfiable(
            'mpich cppflags="-O3"', 'mpich cppflags="-O2"')

    def test_satisfies_virtual(self):
        # Don't use check_satisfies: it checks constrain() too, and
        # you can't constrain a non-virtual by a virtual.
        self.assertTrue(Spec('mpich').satisfies(Spec('mpi')))
        self.assertTrue(Spec('mpich2').satisfies(Spec('mpi')))
        self.assertTrue(Spec('zmpi').satisfies(Spec('mpi')))

    def test_satisfies_virtual_dep_with_virtual_constraint(self):
        """Ensure we can satisfy virtual constraints when there are multiple
           vdep providers in the specs."""
        self.assertTrue(
            Spec('netlib-lapack ^openblas').satisfies(
                'netlib-lapack ^openblas'))
        self.assertFalse(
            Spec('netlib-lapack ^netlib-blas').satisfies(
                'netlib-lapack ^openblas'))

        self.assertFalse(
            Spec('netlib-lapack ^openblas').satisfies(
                'netlib-lapack ^netlib-blas'))
        self.assertTrue(
            Spec('netlib-lapack ^netlib-blas').satisfies(
                'netlib-lapack ^netlib-blas'))

    # ========================================================================
    # Indexing specs
    # ========================================================================
    def test_self_index(self):
        s = Spec('callpath')
        self.assertTrue(s['callpath'] == s)

    def test_dep_index(self):
        s = Spec('callpath')
        s.normalize()

        self.assertTrue(s['callpath'] == s)
        self.assertTrue(type(s['dyninst']) == Spec)
        self.assertTrue(type(s['libdwarf']) == Spec)
        self.assertTrue(type(s['libelf']) == Spec)
        self.assertTrue(type(s['mpi']) == Spec)

        self.assertTrue(s['dyninst'].name  == 'dyninst')
        self.assertTrue(s['libdwarf'].name == 'libdwarf')
        self.assertTrue(s['libelf'].name   == 'libelf')
        self.assertTrue(s['mpi'].name      == 'mpi')

    def test_spec_contains_deps(self):
        s = Spec('callpath')
        s.normalize()
        self.assertTrue('dyninst' in s)
        self.assertTrue('libdwarf' in s)
        self.assertTrue('libelf' in s)
        self.assertTrue('mpi' in s)

    def test_virtual_index(self):
        s = Spec('callpath')
        s.concretize()

        s_mpich = Spec('callpath ^mpich')
        s_mpich.concretize()

        s_mpich2 = Spec('callpath ^mpich2')
        s_mpich2.concretize()

        s_zmpi = Spec('callpath ^zmpi')
        s_zmpi.concretize()

        self.assertTrue(s['mpi'].name != 'mpi')
        self.assertTrue(s_mpich['mpi'].name == 'mpich')
        self.assertTrue(s_mpich2['mpi'].name == 'mpich2')
        self.assertTrue(s_zmpi['zmpi'].name == 'zmpi')

        for spec in [s, s_mpich, s_mpich2, s_zmpi]:
            self.assertTrue('mpi' in spec)

    # ========================================================================
    # Constraints
    # ========================================================================
    def test_constrain_variants(self):
        self.check_constrain('libelf@2.1:2.5', 'libelf@0:2.5', 'libelf@2.1:3')
        self.check_constrain('libelf@2.1:2.5%gcc@4.5:4.6',
                             'libelf@0:2.5%gcc@2:4.6',
                             'libelf@2.1:3%gcc@4.5:4.7')

        self.check_constrain('libelf+debug+foo', 'libelf+debug', 'libelf+foo')
        self.check_constrain('libelf+debug+foo',
                             'libelf+debug', 'libelf+debug+foo')

        self.check_constrain('libelf debug=2 foo=1',
                             'libelf debug=2', 'libelf foo=1')
        self.check_constrain('libelf debug=2 foo=1',
                             'libelf debug=2', 'libelf debug=2 foo=1')

        self.check_constrain('libelf+debug~foo', 'libelf+debug', 'libelf~foo')
        self.check_constrain('libelf+debug~foo',
                             'libelf+debug', 'libelf+debug~foo')

    def test_constrain_compiler_flags(self):
        self.check_constrain('libelf cflags="-O3" cppflags="-Wall"',
                             'libelf cflags="-O3"', 'libelf cppflags="-Wall"')
        self.check_constrain('libelf cflags="-O3" cppflags="-Wall"',
                             'libelf cflags="-O3"',
                             'libelf cflags="-O3" cppflags="-Wall"')

    def test_constrain_architecture(self):
        self.check_constrain('libelf target=default_target os=default_os',
                             'libelf target=default_target os=default_os',
                             'libelf target=default_target os=default_os')
        self.check_constrain('libelf target=default_target os=default_os',
                             'libelf',
                             'libelf target=default_target os=default_os')

    def test_constrain_compiler(self):
        self.check_constrain('libelf %gcc@4.4.7',
                             'libelf %gcc@4.4.7', 'libelf %gcc@4.4.7')
        self.check_constrain('libelf %gcc@4.4.7',
                             'libelf', 'libelf %gcc@4.4.7')

    def test_invalid_constraint(self):
        self.check_invalid_constraint('libelf@0:2.0', 'libelf@2.1:3')
        self.check_invalid_constraint(
            'libelf@0:2.5%gcc@4.8:4.9', 'libelf@2.1:3%gcc@4.5:4.7')

        self.check_invalid_constraint('libelf+debug', 'libelf~debug')
        self.check_invalid_constraint('libelf+debug~foo', 'libelf+debug+foo')
        self.check_invalid_constraint('libelf debug=2', 'libelf debug=1')

        self.check_invalid_constraint(
            'libelf cppflags="-O3"', 'libelf cppflags="-O2"')
        self.check_invalid_constraint('libelf platform=test target=be os=be',
                                      'libelf target=fe os=fe')

    def test_constrain_changed(self):
        self.check_constrain_changed('libelf', '@1.0')
        self.check_constrain_changed('libelf', '@1.0:5.0')
        self.check_constrain_changed('libelf', '%gcc')
        self.check_constrain_changed('libelf%gcc', '%gcc@4.5')
        self.check_constrain_changed('libelf', '+debug')
        self.check_constrain_changed('libelf', '~debug')
        self.check_constrain_changed('libelf', 'debug=2')
        self.check_constrain_changed('libelf', 'cppflags="-O3"')

        platform = spack.architecture.platform()
        self.check_constrain_changed(
            'libelf', 'target=' + platform.target('default_target').name)
        self.check_constrain_changed(
            'libelf', 'os=' + platform.operating_system('default_os').name)

    def test_constrain_not_changed(self):
        self.check_constrain_not_changed('libelf', 'libelf')
        self.check_constrain_not_changed('libelf@1.0', '@1.0')
        self.check_constrain_not_changed('libelf@1.0:5.0', '@1.0:5.0')
        self.check_constrain_not_changed('libelf%gcc', '%gcc')
        self.check_constrain_not_changed('libelf%gcc@4.5', '%gcc@4.5')
        self.check_constrain_not_changed('libelf+debug', '+debug')
        self.check_constrain_not_changed('libelf~debug', '~debug')
        self.check_constrain_not_changed('libelf debug=2', 'debug=2')
        self.check_constrain_not_changed(
            'libelf cppflags="-O3"', 'cppflags="-O3"')

        platform = spack.architecture.platform()
        default_target = platform.target('default_target').name
        self.check_constrain_not_changed(
            'libelf target=' + default_target, 'target=' + default_target)

    def test_constrain_dependency_changed(self):
        self.check_constrain_changed('libelf^foo', 'libelf^foo@1.0')
        self.check_constrain_changed('libelf^foo', 'libelf^foo@1.0:5.0')
        self.check_constrain_changed('libelf^foo', 'libelf^foo%gcc')
        self.check_constrain_changed('libelf^foo%gcc', 'libelf^foo%gcc@4.5')
        self.check_constrain_changed('libelf^foo', 'libelf^foo+debug')
        self.check_constrain_changed('libelf^foo', 'libelf^foo~debug')

        platform = spack.architecture.platform()
        default_target = platform.target('default_target').name
        self.check_constrain_changed(
            'libelf^foo', 'libelf^foo target=' + default_target)

    def test_constrain_dependency_not_changed(self):
        self.check_constrain_not_changed('libelf^foo@1.0', 'libelf^foo@1.0')
        self.check_constrain_not_changed(
            'libelf^foo@1.0:5.0', 'libelf^foo@1.0:5.0')
        self.check_constrain_not_changed('libelf^foo%gcc', 'libelf^foo%gcc')
        self.check_constrain_not_changed(
            'libelf^foo%gcc@4.5', 'libelf^foo%gcc@4.5')
        self.check_constrain_not_changed(
            'libelf^foo+debug', 'libelf^foo+debug')
        self.check_constrain_not_changed(
            'libelf^foo~debug', 'libelf^foo~debug')
        self.check_constrain_not_changed(
            'libelf^foo cppflags="-O3"', 'libelf^foo cppflags="-O3"')

        platform = spack.architecture.platform()
        default_target = platform.target('default_target').name
        self.check_constrain_not_changed(
            'libelf^foo target=' + default_target,
            'libelf^foo target=' + default_target)
