# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
