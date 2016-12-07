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

import StringIO

import llnl.util.lang
import pytest
import spack
import spack.architecture
import spack.fetch_strategy
import spack.platforms.test

##########
# Monkey-patching that is applied to all tests
##########


@pytest.fixture(autouse=True)
def no_stdin_duplication(monkeypatch):
    """Duplicating stdin (or any other stream) returns an empty
    StringIO object.
    """
    monkeypatch.setattr(
        llnl.util.lang,
        'duplicate_stream',
        lambda x: StringIO.StringIO()
    )


@pytest.fixture(autouse=True)
def mock_fetch_cache(monkeypatch):
    """Substitutes spack.fetch_cache with a mock object that does nothing
    and raises on fetch.
    """
    class MockCache(object):
        def store(self, copyCmd, relativeDst):
            pass

        def fetcher(self, targetPath, digest, **kwargs):
            return MockCacheFetcher()

    class MockCacheFetcher(object):
        def set_stage(self, stage):
            pass

        def fetch(self):
            raise spack.fetch_strategy.FetchError(
                'Mock cache always fails for tests'
            )

        def __str__(self):
            return "[mock fetcher]"

    monkeypatch.setattr(spack, 'fetch_cache', MockCache())


# FIXME: The lines below should better be added to a fixture with
# FIXME: session-scope. Anyhow doing it is not easy, as it seems
# FIXME: there's some weird interaction with compilers during concretization.
spack.architecture.real_platform = spack.architecture.platform
spack.architecture.platform = lambda: spack.platforms.test.Test()
