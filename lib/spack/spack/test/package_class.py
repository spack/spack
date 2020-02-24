# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test class methods on Package objects.

This doesn't include methods on package *instances* (like do_install(),
etc.).  Only methods like ``possible_dependencies()`` that deal with the
static DSL metadata for packages.
"""

import pytest
import spack.repo


@pytest.fixture
def mpileaks_possible_deps(mock_packages):
    mpi_names = [spec.name for spec in spack.repo.path.providers_for('mpi')]
    possible = {
        'callpath': set(['dyninst'] + mpi_names),
        'dyninst': set(['libdwarf', 'libelf']),
        'fake': set(),
        'libdwarf': set(['libelf']),
        'libelf': set(),
        'mpich': set(),
        'mpich2': set(),
        'mpileaks': set(['callpath'] + mpi_names),
        'multi-provider-mpi': set(),
        'zmpi': set(['fake']),
    }
    return possible


def test_possible_dependencies(mock_packages, mpileaks_possible_deps):
    mpileaks = spack.repo.get('mpileaks')
    assert (mpileaks.possible_dependencies(expand_virtuals=True) ==
            mpileaks_possible_deps)

    assert mpileaks.possible_dependencies(expand_virtuals=False) == {
        'callpath': set(['dyninst']),
        'dyninst': set(['libdwarf', 'libelf']),
        'libdwarf': set(['libelf']),
        'libelf': set(),
        'mpi': set(),
        'mpileaks': set(['callpath']),
    }


def test_possible_dependencies_missing(mock_packages):
    md = spack.repo.get("missing-dependency")
    missing = {}
    md.possible_dependencies(transitive=True, missing=missing)
    assert missing["missing-dependency"] == set([
        "this-is-a-missing-dependency"
    ])


def test_possible_dependencies_with_deptypes(mock_packages):
    dtbuild1 = spack.repo.get('dtbuild1')

    assert dtbuild1.possible_dependencies(deptype=('link', 'run')) == {
        'dtbuild1': set(['dtrun2', 'dtlink2']),
        'dtlink2': set(),
        'dtrun2': set(),
    }

    assert dtbuild1.possible_dependencies(deptype=('build')) == {
        'dtbuild1': set(['dtbuild2', 'dtlink2']),
        'dtbuild2': set(),
        'dtlink2': set(),
    }

    assert dtbuild1.possible_dependencies(deptype=('link')) == {
        'dtbuild1': set(['dtlink2']),
        'dtlink2': set(),
    }


def test_possible_dependencies_with_multiple_classes(
        mock_packages, mpileaks_possible_deps):
    pkgs = ['dt-diamond', 'mpileaks']
    expected = mpileaks_possible_deps.copy()
    expected.update({
        'dt-diamond': set(['dt-diamond-left', 'dt-diamond-right']),
        'dt-diamond-left': set(['dt-diamond-bottom']),
        'dt-diamond-right': set(['dt-diamond-bottom']),
        'dt-diamond-bottom': set(),
    })

    assert spack.package.possible_dependencies(*pkgs) == expected
