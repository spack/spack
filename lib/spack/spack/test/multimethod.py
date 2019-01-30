# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test for multi_method dispatch."""
import pytest

import spack.repo
from spack.multimethod import NoSuchMethodError


def test_no_version_match(mock_packages):
    pkg = spack.repo.get('multimethod@2.0')
    with pytest.raises(NoSuchMethodError):
        pkg.no_version_2()


def test_one_version_match(mock_packages):
    pkg = spack.repo.get('multimethod@1.0')
    assert pkg.no_version_2() == 1

    pkg = spack.repo.get('multimethod@3.0')
    assert pkg.no_version_2() == 3

    pkg = spack.repo.get('multimethod@4.0')
    assert pkg.no_version_2() == 4


def test_version_overlap(mock_packages):
    pkg = spack.repo.get('multimethod@2.0')
    assert pkg.version_overlap() == 1

    pkg = spack.repo.get('multimethod@5.0')
    assert pkg.version_overlap() == 2


def test_mpi_version(mock_packages):
    pkg = spack.repo.get('multimethod^mpich@3.0.4')
    assert pkg.mpi_version() == 3

    pkg = spack.repo.get('multimethod^mpich2@1.2')
    assert pkg.mpi_version() == 2

    pkg = spack.repo.get('multimethod^mpich@1.0')
    assert pkg.mpi_version() == 1


def test_undefined_mpi_version(mock_packages):
    pkg = spack.repo.get('multimethod^mpich@0.4')
    assert pkg.mpi_version() == 1

    pkg = spack.repo.get('multimethod^mpich@1.4')
    assert pkg.mpi_version() == 1


def test_default_works(mock_packages):
    pkg = spack.repo.get('multimethod%gcc')
    assert pkg.has_a_default() == 'gcc'

    pkg = spack.repo.get('multimethod%intel')
    assert pkg.has_a_default() == 'intel'

    pkg = spack.repo.get('multimethod%pgi')
    assert pkg.has_a_default() == 'default'


def test_target_match(mock_packages):
    platform = spack.architecture.platform()
    targets = list(platform.targets.values())
    for target in targets[:-1]:
        pkg = spack.repo.get('multimethod target=' + target.name)
        assert pkg.different_by_target() == target.name

    pkg = spack.repo.get('multimethod target=' + targets[-1].name)
    if len(targets) == 1:
        assert pkg.different_by_target() == targets[-1].name
    else:
        with pytest.raises(NoSuchMethodError):
            pkg.different_by_target()


def test_dependency_match(mock_packages):
    pkg = spack.repo.get('multimethod^zmpi')
    assert pkg.different_by_dep() == 'zmpi'

    pkg = spack.repo.get('multimethod^mpich')
    assert pkg.different_by_dep() == 'mpich'

    # If we try to switch on some entirely different dep, it's ambiguous,
    # but should take the first option
    pkg = spack.repo.get('multimethod^foobar')
    assert pkg.different_by_dep() == 'mpich'


def test_virtual_dep_match(mock_packages):
    pkg = spack.repo.get('multimethod^mpich2')
    assert pkg.different_by_virtual_dep() == 2

    pkg = spack.repo.get('multimethod^mpich@1.0')
    assert pkg.different_by_virtual_dep() == 1


def test_multimethod_with_base_class(mock_packages):
    pkg = spack.repo.get('multimethod@3')
    assert pkg.base_method() == "subclass_method"

    pkg = spack.repo.get('multimethod@1')
    assert pkg.base_method() == "base_method"
