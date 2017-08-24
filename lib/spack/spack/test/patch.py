##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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

import os.path

import pytest
import sys

import spack
import spack.stage


@pytest.fixture()
def mock_apply(monkeypatch):
    """Monkeypatches ``Patch.apply`` to test only the additional behavior of
    derived classes.
    """

    m = sys.modules['spack.patch']

    def check_expand(self, *args, **kwargs):
        # Check tarball expansion
        file = os.path.join(self.path, 'foo.txt')
        if self.expand:
            assert os.path.exists(file)
        else:
            assert not os.path.exists(file)

        # Check tarball fetching
        dirname = os.path.dirname(self.path)
        tarball = os.path.join(dirname, 'foo.tgz')
        assert os.path.exists(tarball)

    monkeypatch.setattr(m.Patch, 'apply', check_expand)


@pytest.fixture()
def mock_stage(tmpdir, monkeypatch):

    monkeypatch.setattr(spack, 'stage_path', str(tmpdir))

    class MockStage(object):
        def __init__(self):
            self.mirror_path = str(tmpdir)

    return MockStage()


@pytest.mark.usefixtures('mock_apply')
@pytest.mark.parametrize('expand', [True, False])
def test_url_patch_expansion(mock_stage, expand):

    m = sys.modules['spack.patch']
    filename = os.path.join(spack.test_path, 'data', 'patch', 'foo.tgz')
    url = 'file://' + filename
    patch = m.Patch.create(
        None, url, 0, md5='bff717ca9cbbb293bdf188e44c540758', expand=expand
    )

    patch.apply(mock_stage)