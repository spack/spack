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
"""Test for multi_method dispatch."""
import spack
import pytest
from spack.multimethod import *
from spack.version import *


def test_no_version_match(builtin_mock):
    pkg = spack.repo.get('multimethod@2.0')
    with pytest.raises(NoSuchMethodError):
        pkg.no_version_2()


def test_one_version_match(builtin_mock):
    pkg = spack.repo.get('multimethod@1.0')
    assert pkg.no_version_2() == 1

    pkg = spack.repo.get('multimethod@3.0')
    assert pkg.no_version_2() == 3

    pkg = spack.repo.get('multimethod@4.0')
    assert pkg.no_version_2() == 4


def test_version_overlap(builtin_mock):
    pkg = spack.repo.get('multimethod@2.0')
    assert pkg.version_overlap() == 1

    pkg = spack.repo.get('multimethod@5.0')
    assert pkg.version_overlap() == 2


def test_mpi_version(builtin_mock):
    pkg = spack.repo.get('multimethod^mpich@3.0.4')
    assert pkg.mpi_version() == 3

    pkg = spack.repo.get('multimethod^mpich2@1.2')
    assert pkg.mpi_version() == 2

    pkg = spack.repo.get('multimethod^mpich@1.0')
    assert pkg.mpi_version() == 1


def test_undefined_mpi_version(builtin_mock):
    pkg = spack.repo.get('multimethod^mpich@0.4')
    assert pkg.mpi_version() == 1

    pkg = spack.repo.get('multimethod^mpich@1.4')
    assert pkg.mpi_version() == 1


def test_default_works(builtin_mock):
    pkg = spack.repo.get('multimethod%gcc')
    assert pkg.has_a_default() == 'gcc'

    pkg = spack.repo.get('multimethod%intel')
    assert pkg.has_a_default() == 'intel'

    pkg = spack.repo.get('multimethod%pgi')
    assert pkg.has_a_default() == 'default'


def test_target_match(builtin_mock):
    platform = spack.architecture.platform()
    targets = platform.targets.values()
    for target in targets[:-1]:
        pkg = spack.repo.get('multimethod target=' + target.name)
        assert pkg.different_by_target() == target.name

    pkg = spack.repo.get('multimethod target=' + targets[-1].name)
    if len(targets) == 1:
        assert pkg.different_by_target() == targets[-1].name
    else:
        with pytest.raises(NoSuchMethodError):
            pkg.different_by_target()


def test_dependency_match(builtin_mock):
    pkg = spack.repo.get('multimethod^zmpi')
    assert pkg.different_by_dep() == 'zmpi'

    pkg = spack.repo.get('multimethod^mpich')
    assert pkg.different_by_dep() == 'mpich'

    # If we try to switch on some entirely different dep, it's ambiguous,
    # but should take the first option
    pkg = spack.repo.get('multimethod^foobar')
    assert pkg.different_by_dep() == 'mpich'


def test_virtual_dep_match(builtin_mock):
    pkg = spack.repo.get('multimethod^mpich2')
    assert pkg.different_by_virtual_dep() == 2

    pkg = spack.repo.get('multimethod^mpich@1.0')
    assert pkg.different_by_virtual_dep() == 1


def test_multimethod_with_base_class(builtin_mock):
    pkg = spack.repo.get('multimethod@3')
    assert pkg.base_method() == "subclass_method"

    pkg = spack.repo.get('multimethod@1')
    assert pkg.base_method() == "base_method"
