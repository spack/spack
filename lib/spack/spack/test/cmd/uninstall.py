# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import spack.store
from spack.main import SpackCommand, SpackCommandError

uninstall = SpackCommand('uninstall')


class MockArgs(object):

    def __init__(self, packages, all=False, force=False, dependents=False):
        self.packages = packages
        self.all = all
        self.force = force
        self.dependents = dependents
        self.yes_to_all = True


@pytest.mark.db
@pytest.mark.usefixtures('database')
def test_multiple_matches():
    """Test unable to uninstall when multiple matches."""
    with pytest.raises(SpackCommandError):
        uninstall('-y', 'mpileaks')


@pytest.mark.db
@pytest.mark.usefixtures('database')
def test_installed_dependents():
    """Test can't uninstall when ther are installed dependents."""
    with pytest.raises(SpackCommandError):
        uninstall('-y', 'libelf')


@pytest.mark.db
@pytest.mark.usefixtures('mutable_database')
def test_recursive_uninstall():
    """Test recursive uninstall."""
    uninstall('-y', '-a', '--dependents', 'callpath')

    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == 8
    # query specs with multiple configurations
    mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
    callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
    mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

    assert len(mpileaks_specs) == 0
    assert len(callpath_specs) == 0
    assert len(mpi_specs) == 3


@pytest.mark.db
@pytest.mark.regression('3690')
@pytest.mark.usefixtures('mutable_database')
@pytest.mark.parametrize('constraint,expected_number_of_specs', [
    ('dyninst', 7), ('libelf', 5)
])
def test_uninstall_spec_with_multiple_roots(
        constraint, expected_number_of_specs
):
    uninstall('-y', '-a', '--dependents', constraint)

    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == expected_number_of_specs


@pytest.mark.db
@pytest.mark.usefixtures('mutable_database')
@pytest.mark.parametrize('constraint,expected_number_of_specs', [
    ('dyninst', 13), ('libelf', 13)
])
def test_force_uninstall_spec_with_ref_count_not_zero(
        constraint, expected_number_of_specs
):
    uninstall('-f', '-y', constraint)

    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == expected_number_of_specs
