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
@pytest.mark.usefixtures('database')
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
