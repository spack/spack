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
import spack.repository
import pytest


@pytest.fixture()
def mock_repository():
    return spack.repository.RepoPath('$spack/var/spack/repos/builtin.mock')


class TestRepoPath(object):

    def test_error_during_construction(self):

        # If the repository has no repo.yaml, raise BadRepoError
        with pytest.raises(spack.repository.BadRepoError):
            spack.repository.RepoPath('/foo/bar')

    def test_magic_methods(self, mock_repository):

        # We constructed a RepoPath with only one item in it,
        # pointing to the mock repository we use for tests
        assert len(mock_repository) == 1

        # Get a single item
        a = mock_repository[0]
        assert isinstance(a, spack.repository.Repo)

        # Get a Slice
        b = mock_repository[:]
        assert isinstance(b, spack.repository.RepoPath)
        assert b == mock_repository

        b.append_from_path('$spack/var/spack/repos/builtin')
        assert len(b) == 2

        c = b[:]
        assert c == b
        assert c != mock_repository

        c = b[:1]
        assert c != b
        assert c == mock_repository

        # Set an item passing from the mock repository
        # to the builtin one
        c = mock_repository[:]
        c[0] = spack.repository.Repo('$spack/var/spack/repos/builtin')

        d = b[1:]
        assert c == d

        # Set a slice to a RepoPath
        a = spack.repository.RepoPath()

        assert len(a) == 0

        # Check that we can go out of bounds as in built-in lists
        a[0:6] = spack.repository.RepoPath(
            '$spack/var/spack/repos/builtin',
            '$spack/var/spack/repos/builtin.mock'
        )

        assert len(a) == 2

        # Delete a slice of items, check that we treat nicely
        # requests that go out of bounds
        del a[1:100]
        assert len(a) == 1

        del a[0:]
        assert len(a) == 0

        # Delete an single item
        b = mock_repository[:]
        b.append_from_path('$spack/var/spack/repos/builtin')
        expected = spack.repository.RepoPath('$spack/var/spack/repos/builtin')
        del b[0]

        assert b == expected

        # Check that the '__contains__' semantic is correctly used to check
        # if a package can be found in a repository
        assert 'a' in mock_repository
        assert 'boost' in mock_repository

        # Check that instead the iteration semantic steps through
        # the repositories
        b = mock_repository[:]
        b.append_from_path('$spack/var/spack/repos/builtin')
        counter = 0

        for _ in b:
            counter += 1

        assert counter == 2
