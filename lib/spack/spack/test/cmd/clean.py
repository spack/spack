##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import pytest
import spack.stage
import spack.caches
import spack.main
import spack.package

clean = spack.main.SpackCommand('clean')


@pytest.fixture()
def mock_calls_for_clean(monkeypatch):

    class Counter(object):
        def __init__(self):
            self.call_count = 0

        def __call__(self, *args, **kwargs):
            self.call_count += 1

    monkeypatch.setattr(spack.package.PackageBase, 'do_clean', Counter())
    monkeypatch.setattr(spack.stage, 'purge', Counter())
    monkeypatch.setattr(
        spack.caches.fetch_cache, 'destroy', Counter(), raising=False)
    monkeypatch.setattr(
        spack.caches.misc_cache, 'destroy', Counter())


@pytest.mark.usefixtures(
    'mock_packages', 'config', 'mock_calls_for_clean'
)
@pytest.mark.parametrize('command_line,counters', [
    ('mpileaks', [1, 0, 0, 0]),
    ('-s',       [0, 1, 0, 0]),
    ('-sd',      [0, 1, 1, 0]),
    ('-m',       [0, 0, 0, 1]),
    ('-a',       [0, 1, 1, 1]),
    ('',         [0, 0, 0, 0]),
])
def test_function_calls(command_line, counters):

    # Call the command with the supplied command line
    clean(command_line)

    # Assert that we called the expected functions the correct
    # number of times
    assert spack.package.PackageBase.do_clean.call_count == counters[0]
    assert spack.stage.purge.call_count == counters[1]
    assert spack.caches.fetch_cache.destroy.call_count == counters[2]
    assert spack.caches.misc_cache.destroy.call_count == counters[3]
