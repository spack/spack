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
import spack
import spack.architecture
from spack.spec import Spec, CompilerSpec
from spack.version import ver
from spack.concretize import find_spec
from spack.test.mock_packages_test import *


class ConcretizeTest(MockPackagesTest):

    def check_spec(self, abstract, concrete):
        if abstract.versions.concrete:
            self.assertEqual(abstract.versions, concrete.versions)

        if abstract.variants:
            for name in abstract.variants:
                avariant = abstract.variants[name]
                cvariant = concrete.variants[name]
                self.assertEqual(avariant.value, cvariant.value)

        if abstract.compiler_flags:
            for flag in abstract.compiler_flags:
                aflag = abstract.compiler_flags[flag]
                cflag = concrete.compiler_flags[flag]
                self.assertTrue(set(aflag) <= set(cflag))

        for name in abstract.package.variants:
            self.assertTrue(name in concrete.variants)

        for flag in concrete.compiler_flags.valid_compiler_flags():
            self.assertTrue(flag in concrete.compiler_flags)

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
        self.check_concretize('callpath')
        self.check_concretize('mpileaks')
        self.check_concretize('libelf')

    def test_concretize_variant(self):
        self.check_concretize('mpich+debug')
        self.check_concretize('mpich~debug')
        self.check_concretize('mpich debug=2')
        self.check_concretize('mpich')

    def test_conretize_compiler_flags(self):
        self.check_concretize('mpich cppflags="-O3"')

    def test_concretize_preferred_version(self):
        spec = self.check_concretize('python')
        self.assertEqual(spec.versions, ver('2.7.11'))

        spec = self.check_concretize('python@3.5.1')
        self.assertEqual(spec.versions, ver('3.5.1'))

    def test_concretize_with_virtual(self):
        self.check_concretize('mpileaks ^mpi')
        self.check_concretize('mpileaks ^mpi@:1.1')
        self.check_concretize('mpileaks ^mpi@2:')
        self.check_concretize('mpileaks ^mpi@2.1')
        self.check_concretize('mpileaks ^mpi@2.2')
        self.check_concretize('mpileaks ^mpi@2.2')
        self.check_concretize('mpileaks ^mpi@:1')
        self.check_concretize('mpileaks ^mpi@1.2:2')

    def test_concretize_with_restricted_virtual(self):
        self.check_concretize('mpileaks ^mpich2')

        concrete = self.check_concretize('mpileaks   ^mpich2@1.1')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.1'))

        concrete = self.check_concretize('mpileaks   ^mpich2@1.2')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.2'))

        concrete = self.check_concretize('mpileaks   ^mpich2@:1.5')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@:1.5'))

        concrete = self.check_concretize('mpileaks   ^mpich2@:1.3')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@:1.3'))

        concrete = self.check_concretize('mpileaks   ^mpich2@:1.2')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@:1.2'))

        concrete = self.check_concretize('mpileaks   ^mpich2@:1.1')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@:1.1'))

        concrete = self.check_concretize('mpileaks   ^mpich2@1.1:')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.1:'))

        concrete = self.check_concretize('mpileaks   ^mpich2@1.5:')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.5:'))

        concrete = self.check_concretize('mpileaks   ^mpich2@1.3.1:1.4')
        self.assertTrue(concrete['mpich2'].satisfies('mpich2@1.3.1:1.4'))

    def test_concretize_with_provides_when(self):
        """Make sure insufficient versions of MPI are not in providers list when
           we ask for some advanced version.
        """
        self.assertTrue(
            not any(spec.satisfies('mpich2@:1.0')
                    for spec in spack.repo.providers_for('mpi@2.1')))

        self.assertTrue(
            not any(spec.satisfies('mpich2@:1.1')
                    for spec in spack.repo.providers_for('mpi@2.2')))

        self.assertTrue(
            not any(spec.satisfies('mpich@:1')
                    for spec in spack.repo.providers_for('mpi@2')))

        self.assertTrue(
            not any(spec.satisfies('mpich@:1')
                    for spec in spack.repo.providers_for('mpi@3')))

        self.assertTrue(
            not any(spec.satisfies('mpich2')
                    for spec in spack.repo.providers_for('mpi@3')))

    def test_concretize_two_virtuals(self):
        """Test a package with multiple virtual dependencies."""
        Spec('hypre').concretize()

    def test_concretize_two_virtuals_with_one_bound(self):
        """Test a package with multiple virtual dependencies and one preset."""
        Spec('hypre ^openblas').concretize()

    def test_concretize_two_virtuals_with_two_bound(self):
        """Test a package with multiple virtual deps and two of them preset."""
        Spec('hypre ^openblas ^netlib-lapack').concretize()

    def test_concretize_two_virtuals_with_dual_provider(self):
        """Test a package with multiple virtual dependencies and force a provider
           that provides both."""
        Spec('hypre ^openblas-with-lapack').concretize()

    def test_concretize_two_virtuals_with_dual_provider_and_a_conflict(self):
        """Test a package with multiple virtual dependencies and force a
           provider that provides both, and another conflicting package that
           provides one.
        """
        s = Spec('hypre ^openblas-with-lapack ^netlib-lapack')
        self.assertRaises(spack.spec.MultipleProviderError, s.concretize)

    def test_virtual_is_fully_expanded_for_callpath(self):
        # force dependence on fake "zmpi" by asking for MPI 10.0
        spec = Spec('callpath ^mpi@10.0')
        self.assertTrue('mpi' in spec._dependencies)
        self.assertFalse('fake' in spec)

        spec.concretize()

        self.assertTrue('zmpi' in spec._dependencies)
        self.assertTrue(all('mpi' not in d._dependencies
                            for d in spec.traverse()))
        self.assertTrue('zmpi' in spec)
        self.assertTrue('mpi' in spec)

        self.assertTrue('fake' in spec._dependencies['zmpi'].spec)

    def test_virtual_is_fully_expanded_for_mpileaks(self):
        spec = Spec('mpileaks ^mpi@10.0')
        self.assertTrue('mpi' in spec._dependencies)
        self.assertFalse('fake' in spec)

        spec.concretize()

        self.assertTrue('zmpi' in spec._dependencies)
        self.assertTrue('callpath' in spec._dependencies)
        self.assertTrue(
            'zmpi' in spec._dependencies['callpath']
            .spec._dependencies)
        self.assertTrue(
            'fake' in spec._dependencies['callpath']
            .spec._dependencies['zmpi']
            .spec._dependencies)

        self.assertTrue(
            all('mpi' not in d._dependencies for d in spec.traverse()))
        self.assertTrue('zmpi' in spec)
        self.assertTrue('mpi' in spec)

    def test_my_dep_depends_on_provider_of_my_virtual_dep(self):
        spec = Spec('indirect_mpich')
        spec.normalize()
        spec.concretize()

    def test_compiler_inheritance(self):
        spec = Spec('mpileaks')
        spec.normalize()

        spec['dyninst'].compiler = CompilerSpec('clang')
        spec.concretize()

        # TODO: not exactly the syntax I would like.
        self.assertTrue(spec['libdwarf'].compiler.satisfies('clang'))
        self.assertTrue(spec['libelf'].compiler.satisfies('clang'))

    def test_external_package(self):
        spec = Spec('externaltool%gcc')
        spec.concretize()

        self.assertEqual(
            spec['externaltool'].external, '/path/to/external_tool')
        self.assertFalse('externalprereq' in spec)
        self.assertTrue(spec['externaltool'].compiler.satisfies('gcc'))

    def test_external_package_module(self):
        # No tcl modules on darwin/linux machines
        # TODO: improved way to check for this.
        platform = spack.architecture.real_platform().name
        if (platform == 'darwin' or platform == 'linux'):
            return

        spec = Spec('externalmodule')
        spec.concretize()
        self.assertEqual(
            spec['externalmodule'].external_module, 'external-module')
        self.assertFalse('externalprereq' in spec)
        self.assertTrue(spec['externalmodule'].compiler.satisfies('gcc'))

    def test_nobuild_package(self):
        got_error = False
        spec = Spec('externaltool%clang')
        try:
            spec.concretize()
        except spack.concretize.NoBuildError:
            got_error = True
        self.assertTrue(got_error)

    def test_external_and_virtual(self):
        spec = Spec('externaltest')
        spec.concretize()
        self.assertEqual(
            spec['externaltool'].external, '/path/to/external_tool')
        self.assertEqual(
            spec['stuff'].external, '/path/to/external_virtual_gcc')
        self.assertTrue(spec['externaltool'].compiler.satisfies('gcc'))
        self.assertTrue(spec['stuff'].compiler.satisfies('gcc'))

    def test_find_spec_parents(self):
        """Tests the spec finding logic used by concretization. """
        s = Spec('a +foo',
                 Spec('b +foo',
                      Spec('c'),
                      Spec('d +foo')),
                 Spec('e +foo'))

        self.assertEqual('a', find_spec(s['b'], lambda s: '+foo' in s).name)

    def test_find_spec_children(self):
        s = Spec('a',
                 Spec('b +foo',
                      Spec('c'),
                      Spec('d +foo')),
                 Spec('e +foo'))
        self.assertEqual('d', find_spec(s['b'], lambda s: '+foo' in s).name)
        s = Spec('a',
                 Spec('b +foo',
                      Spec('c +foo'),
                      Spec('d')),
                 Spec('e +foo'))
        self.assertEqual('c', find_spec(s['b'], lambda s: '+foo' in s).name)

    def test_find_spec_sibling(self):
        s = Spec('a',
                 Spec('b +foo',
                      Spec('c'),
                      Spec('d')),
                 Spec('e +foo'))
        self.assertEqual('e', find_spec(s['b'], lambda s: '+foo' in s).name)
        self.assertEqual('b', find_spec(s['e'], lambda s: '+foo' in s).name)

        s = Spec('a',
                 Spec('b +foo',
                      Spec('c'),
                      Spec('d')),
                 Spec('e',
                      Spec('f +foo')))
        self.assertEqual('f', find_spec(s['b'], lambda s: '+foo' in s).name)

    def test_find_spec_self(self):
        s = Spec('a',
                 Spec('b +foo',
                      Spec('c'),
                      Spec('d')),
                 Spec('e'))
        self.assertEqual('b', find_spec(s['b'], lambda s: '+foo' in s).name)

    def test_find_spec_none(self):
        s = Spec('a',
                 Spec('b',
                      Spec('c'),
                      Spec('d')),
                 Spec('e'))
        self.assertEqual(None, find_spec(s['b'], lambda s: '+foo' in s))

    def test_compiler_child(self):
        s = Spec('mpileaks%clang ^dyninst%gcc')
        s.concretize()
        self.assertTrue(s['mpileaks'].satisfies('%clang'))
        self.assertTrue(s['dyninst'].satisfies('%gcc'))
