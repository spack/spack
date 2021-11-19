# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test for multi_method dispatch."""
import pytest

import spack.platforms
import spack.repo
from spack.multimethod import NoSuchMethodError

pytestmark = pytest.mark.usefixtures('mock_packages')


@pytest.fixture(scope='module',
                params=['multimethod', 'multimethod-inheritor'])
def pkg_name(request):
    """Make tests run on both multimethod and multimethod-inheritor.

    This means we test all of our @when methods on a class that uses them
    directly, AND on a class that inherits them.
    """
    return request.param


def test_no_version_match(pkg_name):
    pkg = spack.repo.get(pkg_name + '@2.0')
    with pytest.raises(NoSuchMethodError):
        pkg.no_version_2()


def test_one_version_match(pkg_name):
    pkg = spack.repo.get(pkg_name + '@1.0')
    assert pkg.no_version_2() == 1

    pkg = spack.repo.get(pkg_name + '@3.0')
    assert pkg.no_version_2() == 3

    pkg = spack.repo.get(pkg_name + '@4.0')
    assert pkg.no_version_2() == 4


def test_version_overlap(pkg_name):
    pkg = spack.repo.get(pkg_name + '@2.0')
    assert pkg.version_overlap() == 1

    pkg = spack.repo.get(pkg_name + '@5.0')
    assert pkg.version_overlap() == 2


def test_mpi_version(pkg_name):
    pkg = spack.repo.get(pkg_name + '^mpich@3.0.4')
    assert pkg.mpi_version() == 3

    pkg = spack.repo.get(pkg_name + '^mpich2@1.2')
    assert pkg.mpi_version() == 2

    pkg = spack.repo.get(pkg_name + '^mpich@1.0')
    assert pkg.mpi_version() == 1


def test_undefined_mpi_version(pkg_name):
    pkg = spack.repo.get(pkg_name + '^mpich@0.4')
    assert pkg.mpi_version() == 1

    pkg = spack.repo.get(pkg_name + '^mpich@1.4')
    assert pkg.mpi_version() == 1


def test_default_works(pkg_name):
    pkg = spack.repo.get(pkg_name + '%gcc')
    assert pkg.has_a_default() == 'gcc'

    pkg = spack.repo.get(pkg_name + '%intel')
    assert pkg.has_a_default() == 'intel'

    pkg = spack.repo.get(pkg_name + '%pgi')
    assert pkg.has_a_default() == 'default'


def test_target_match(pkg_name):
    platform = spack.platforms.host()
    targets = list(platform.targets.values())
    for target in targets[:-1]:
        pkg = spack.repo.get(pkg_name + ' target=' + target.name)
        assert pkg.different_by_target() == target.name

    pkg = spack.repo.get(pkg_name + ' target=' + targets[-1].name)
    if len(targets) == 1:
        assert pkg.different_by_target() == targets[-1].name
    else:
        with pytest.raises(NoSuchMethodError):
            pkg.different_by_target()


def test_dependency_match(pkg_name):
    pkg = spack.repo.get(pkg_name + '^zmpi')
    assert pkg.different_by_dep() == 'zmpi'

    pkg = spack.repo.get(pkg_name + '^mpich')
    assert pkg.different_by_dep() == 'mpich'

    # If we try to switch on some entirely different dep, it's ambiguous,
    # but should take the first option
    pkg = spack.repo.get(pkg_name + '^foobar')
    assert pkg.different_by_dep() == 'mpich'


def test_virtual_dep_match(pkg_name):
    pkg = spack.repo.get(pkg_name + '^mpich2')
    assert pkg.different_by_virtual_dep() == 2

    pkg = spack.repo.get(pkg_name + '^mpich@1.0')
    assert pkg.different_by_virtual_dep() == 1


def test_multimethod_with_base_class(pkg_name):
    pkg = spack.repo.get(pkg_name + '@3')
    assert pkg.base_method() == pkg.spec.name

    pkg = spack.repo.get(pkg_name + '@1')
    assert pkg.base_method() == "base_method"


def test_multimethod_inherited_and_overridden():
    pkg = spack.repo.get('multimethod-inheritor@1.0')
    assert pkg.inherited_and_overridden() == 'inheritor@1.0'

    pkg = spack.repo.get('multimethod-inheritor@2.0')
    assert pkg.inherited_and_overridden() == 'base@2.0'

    pkg = spack.repo.get('multimethod@1.0')
    assert pkg.inherited_and_overridden() == 'base@1.0'

    pkg = spack.repo.get('multimethod@2.0')
    assert pkg.inherited_and_overridden() == 'base@2.0'


def test_multimethod_diamond_inheritance():
    pkg = spack.repo.get('multimethod-diamond@1.0')
    assert pkg.diamond_inheritance() == 'base_package'

    pkg = spack.repo.get('multimethod-base@1.0')
    assert pkg.diamond_inheritance() == 'base_package'

    pkg = spack.repo.get('multimethod-diamond@2.0')
    assert pkg.diamond_inheritance() == 'first_parent'

    pkg = spack.repo.get('multimethod-inheritor@2.0')
    assert pkg.diamond_inheritance() == 'first_parent'

    pkg = spack.repo.get('multimethod-diamond@3.0')
    assert pkg.diamond_inheritance() == 'second_parent'

    pkg = spack.repo.get('multimethod-diamond-parent@3.0')
    assert pkg.diamond_inheritance() == 'second_parent'

    pkg = spack.repo.get('multimethod-diamond@4.0')
    assert pkg.diamond_inheritance() == 'subclass'


def test_multimethod_boolean(pkg_name):
    pkg = spack.repo.get(pkg_name)
    assert pkg.boolean_true_first() == 'True'
    assert pkg.boolean_false_first() == 'True'
