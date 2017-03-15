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
import os

import pytest
import spack
from llnl.util.filesystem import *
from spack.spec import Spec
from spack.version import ver


@pytest.fixture(params=['default', 'rev0'])
def type_of_test(request):
    """Returns one of the test type available for the mock_hg_repository"""
    return request.param


def test_fetch(
        type_of_test,
        mock_svn_repository,
        config,
        refresh_builtin_mock
):
    """Tries to:

    1. Fetch the repo using a fetch strategy constructed with
       supplied args (they depend on type_of_test).
    2. Check if the test_file is in the checked out repository.
    3. Assert that the repository is at the revision supplied.
    4. Add and remove some files, then reset the repo, and
       ensure it's all there again.
    """
    # Retrieve the right test parameters
    t = mock_svn_repository.checks[type_of_test]
    h = mock_svn_repository.hash
    # Construct the package under test
    spec = Spec('hg-test')
    spec.concretize()
    pkg = spack.repo.get(spec, new=True)
    pkg.versions[ver('hg')] = t.args
    # Enter the stage directory and check some properties
    with pkg.stage:
        pkg.do_stage()
        assert h() == t.revision

        file_path = join_path(pkg.stage.source_path, t.file)
        assert os.path.isdir(pkg.stage.source_path)
        assert os.path.isfile(file_path)

        os.unlink(file_path)
        assert not os.path.isfile(file_path)

        untracked_file = 'foobarbaz'
        touch(untracked_file)
        assert os.path.isfile(untracked_file)
        pkg.do_restage()
        assert not os.path.isfile(untracked_file)

        assert os.path.isdir(pkg.stage.source_path)
        assert os.path.isfile(file_path)

        assert h() == t.revision
