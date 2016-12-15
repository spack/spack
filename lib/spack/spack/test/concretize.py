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
import pytest

import spack
import spack.architecture
from spack.spec import Spec, CompilerSpec
from spack.version import ver
from spack.concretize import find_spec


def check_spec(abstract, concrete):
    if abstract.versions.concrete:
        assert abstract.versions == concrete.versions

    if abstract.variants:
        for name in abstract.variants:
            avariant = abstract.variants[name]
            cvariant = concrete.variants[name]
            assert avariant.value == cvariant.value

    if abstract.compiler_flags:
        for flag in abstract.compiler_flags:
            aflag = abstract.compiler_flags[flag]
            cflag = concrete.compiler_flags[flag]
            assert set(aflag) <= set(cflag)

    for name in abstract.package.variants:
        assert name in concrete.variants

    for flag in concrete.compiler_flags.valid_compiler_flags():
        assert flag in concrete.compiler_flags

    if abstract.compiler and abstract.compiler.concrete:
        assert abstract.compiler == concrete.compiler

    if abstract.architecture and abstract.architecture.concrete:
        assert abstract.architecture == concrete.architecture


def check_concretize(abstract_spec):
    abstract = Spec(abstract_spec)
    concrete = abstract.concretized()
    assert not abstract.concrete
    assert concrete.concrete
    check_spec(abstract, concrete)
    return concrete


@pytest.fixture(
    params=[
        # no_deps
        'libelf', 'libelf@0.8.13',
        # dag
        'callpath', 'mpileaks', 'libelf',
        # variant
        'mpich+debug', 'mpich~debug', 'mpich debug=2', 'mpich',
        # compiler flags
        'mpich cppflags="-O3"',
        # with virtual
        'mpileaks ^mpi', 'mpileaks ^mpi@:1.1', 'mpileaks ^mpi@2:',
        'mpileaks ^mpi@2.1', 'mpileaks ^mpi@2.2', 'mpileaks ^mpi@2.2',
        'mpileaks ^mpi@:1', 'mpileaks ^mpi@1.2:2'
    ]
)
def spec(request):
    """Spec to be concretized"""
    return request.param


def test_concretize(spec, config, builtin_mock):
    check_concretize(spec)


def test_concretize_mention_build_dep(config, builtin_mock):
    spec = check_concretize('cmake-client ^cmake@3.4.3')
    # Check parent's perspective of child
    dependency = spec.dependencies_dict()['cmake']
    assert set(dependency.deptypes) == set(['build'])
    # Check child's perspective of parent
    cmake = spec['cmake']
    dependent = cmake.dependents_dict()['cmake-client']
    assert set(dependent.deptypes) == set(['build'])


def test_concretize_preferred_version(config, builtin_mock):
    spec = check_concretize('python')
    assert spec.versions == ver('2.7.11')
    spec = check_concretize('python@3.5.1')
    assert spec.versions == ver('3.5.1')


def test_concretize_with_restricted_virtual(config, builtin_mock):
    check_concretize('mpileaks ^mpich2')

    concrete = check_concretize('mpileaks   ^mpich2@1.1')
    assert concrete['mpich2'].satisfies('mpich2@1.1')

    concrete = check_concretize('mpileaks   ^mpich2@1.2')
    assert concrete['mpich2'].satisfies('mpich2@1.2')

    concrete = check_concretize('mpileaks   ^mpich2@:1.5')
    assert concrete['mpich2'].satisfies('mpich2@:1.5')

    concrete = check_concretize('mpileaks   ^mpich2@:1.3')
    assert concrete['mpich2'].satisfies('mpich2@:1.3')

    concrete = check_concretize('mpileaks   ^mpich2@:1.2')
    assert concrete['mpich2'].satisfies('mpich2@:1.2')

    concrete = check_concretize('mpileaks   ^mpich2@:1.1')
    assert concrete['mpich2'].satisfies('mpich2@:1.1')

    concrete = check_concretize('mpileaks   ^mpich2@1.1:')
    assert concrete['mpich2'].satisfies('mpich2@1.1:')

    concrete = check_concretize('mpileaks   ^mpich2@1.5:')
    assert concrete['mpich2'].satisfies('mpich2@1.5:')

    concrete = check_concretize('mpileaks   ^mpich2@1.3.1:1.4')
    assert concrete['mpich2'].satisfies('mpich2@1.3.1:1.4')


def test_concretize_with_provides_when(config, builtin_mock):
    """Make sure insufficient versions of MPI are not in providers list when
    we ask for some advanced version.
    """
    repo = spack.repo
    assert not any(
        s.satisfies('mpich2@:1.0') for s in repo.providers_for('mpi@2.1')
    )
    assert not any(
        s.satisfies('mpich2@:1.1') for s in repo.providers_for('mpi@2.2')
    )
    assert not any(
        s.satisfies('mpich@:1') for s in repo.providers_for('mpi@2')
    )
    assert not any(
        s.satisfies('mpich@:1') for s in repo.providers_for('mpi@3')
    )
    assert not any(
        s.satisfies('mpich2') for s in repo.providers_for('mpi@3')
    )


def test_concretize_two_virtuals(config, builtin_mock):
    """Test a package with multiple virtual dependencies."""
    Spec('hypre').concretize()


def test_concretize_two_virtuals_with_one_bound(config, refresh_builtin_mock):
    """Test a package with multiple virtual dependencies and one preset."""
    Spec('hypre ^openblas').concretize()


def test_concretize_two_virtuals_with_two_bound(config, builtin_mock):
    """Test a package with multiple virtual deps and two of them preset."""
    Spec('hypre ^openblas ^netlib-lapack').concretize()


def test_concretize_two_virtuals_with_dual_provider(config, builtin_mock):
    """Test a package with multiple virtual dependencies and force a provider
    that provides both.
    """
    Spec('hypre ^openblas-with-lapack').concretize()


def test_concretize_two_virtuals_with_dual_provider_and_a_conflict(
        config, builtin_mock
):
    """Test a package with multiple virtual dependencies and force a
    provider that provides both, and another conflicting package that
    provides one.
    """
    s = Spec('hypre ^openblas-with-lapack ^netlib-lapack')
    with pytest.raises(spack.spec.MultipleProviderError):
        s.concretize()


def test_virtual_is_fully_expanded_for_callpath(config, builtin_mock):
    # force dependence on fake "zmpi" by asking for MPI 10.0
    spec = Spec('callpath ^mpi@10.0')
    assert 'mpi' in spec._dependencies
    assert 'fake' not in spec
    spec.concretize()
    assert 'zmpi' in spec._dependencies
    assert all('mpi' not in d._dependencies for d in spec.traverse())
    assert 'zmpi' in spec
    assert 'mpi' in spec
    assert 'fake' in spec._dependencies['zmpi'].spec


def test_virtual_is_fully_expanded_for_mpileaks(
        config, builtin_mock
):
    spec = Spec('mpileaks ^mpi@10.0')
    assert 'mpi' in spec._dependencies
    assert 'fake' not in spec
    spec.concretize()
    assert 'zmpi' in spec._dependencies
    assert 'callpath' in spec._dependencies
    assert 'zmpi' in spec._dependencies['callpath'].spec._dependencies
    assert 'fake' in spec._dependencies['callpath'].spec._dependencies['zmpi'].spec._dependencies  # NOQA: ignore=E501
    assert all('mpi' not in d._dependencies for d in spec.traverse())
    assert 'zmpi' in spec
    assert 'mpi' in spec


def test_my_dep_depends_on_provider_of_my_virtual_dep(config, builtin_mock):
    spec = Spec('indirect_mpich')
    spec.normalize()
    spec.concretize()


def test_compiler_inheritance(config, builtin_mock):
    spec = Spec('mpileaks')
    spec.normalize()
    spec['dyninst'].compiler = CompilerSpec('clang')
    spec.concretize()
    # TODO: not exactly the syntax I would like.
    assert spec['libdwarf'].compiler.satisfies('clang')
    assert spec['libelf'].compiler.satisfies('clang')


def test_external_package(config, builtin_mock):
    spec = Spec('externaltool%gcc')
    spec.concretize()
    assert spec['externaltool'].external == '/path/to/external_tool'
    assert 'externalprereq' not in spec
    assert spec['externaltool'].compiler.satisfies('gcc')


def test_external_package_module(config, builtin_mock):
    # No tcl modules on darwin/linux machines
    # TODO: improved way to check for this.
    platform = spack.architecture.real_platform().name
    if platform == 'darwin' or platform == 'linux':
        return

    spec = Spec('externalmodule')
    spec.concretize()
    assert spec['externalmodule'].external_module == 'external-module'
    assert 'externalprereq' not in spec
    assert spec['externalmodule'].compiler.satisfies('gcc')


def test_nobuild_package(config, builtin_mock):
    got_error = False
    spec = Spec('externaltool%clang')
    try:
        spec.concretize()
    except spack.concretize.NoBuildError:
        got_error = True
    assert got_error


def test_external_and_virtual(config, builtin_mock):
    spec = Spec('externaltest')
    spec.concretize()
    assert spec['externaltool'].external == '/path/to/external_tool'
    assert spec['stuff'].external == '/path/to/external_virtual_gcc'
    assert spec['externaltool'].compiler.satisfies('gcc')
    assert spec['stuff'].compiler.satisfies('gcc')


def test_find_spec_parents(config, builtin_mock):
    """Tests the spec finding logic used by concretization. """
    s = Spec('a +foo',
             Spec('b +foo',
                  Spec('c'),
                  Spec('d +foo')),
             Spec('e +foo'))

    assert 'a' == find_spec(s['b'], lambda s: '+foo' in s).name


def test_find_spec_children(config, builtin_mock):
    s = Spec('a',
             Spec('b +foo',
                  Spec('c'),
                  Spec('d +foo')),
             Spec('e +foo'))
    assert 'd' == find_spec(s['b'], lambda s: '+foo' in s).name
    s = Spec('a',
             Spec('b +foo',
                  Spec('c +foo'),
                  Spec('d')),
             Spec('e +foo'))
    assert 'c' == find_spec(s['b'], lambda s: '+foo' in s).name


def test_find_spec_sibling(config, builtin_mock):
    s = Spec('a',
             Spec('b +foo',
                  Spec('c'),
                  Spec('d')),
             Spec('e +foo'))
    assert 'e' == find_spec(s['b'], lambda s: '+foo' in s).name
    assert 'b' == find_spec(s['e'], lambda s: '+foo' in s).name

    s = Spec('a',
             Spec('b +foo',
                  Spec('c'),
                  Spec('d')),
             Spec('e',
                  Spec('f +foo')))
    assert 'f' == find_spec(s['b'], lambda s: '+foo' in s).name


def test_find_spec_self(config, builtin_mock):
    s = Spec('a',
             Spec('b +foo',
                  Spec('c'),
                  Spec('d')),
             Spec('e'))
    assert 'b' == find_spec(s['b'], lambda s: '+foo' in s).name


def test_find_spec_none(config, builtin_mock):
    s = Spec('a',
             Spec('b',
                  Spec('c'),
                  Spec('d')),
             Spec('e'))
    assert find_spec(s['b'], lambda s: '+foo' in s) is None


def test_compiler_child(config, builtin_mock):
    s = Spec('mpileaks%clang ^dyninst%gcc')
    s.concretize()
    assert s['mpileaks'].satisfies('%clang')
    assert s['dyninst'].satisfies('%gcc')
