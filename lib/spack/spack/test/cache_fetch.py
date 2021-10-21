# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

from llnl.util.filesystem import mkdirp, touch

import spack.config
from spack.fetch_strategy import CacheURLFetchStrategy, NoCacheError
from spack.stage import Stage


@pytest.mark.parametrize('_fetch_method', ['curl', 'urllib'])
def test_fetch_missing_cache(tmpdir, _fetch_method):
    """Ensure raise a missing cache file."""
    testpath = str(tmpdir)
    with spack.config.override('config:url_fetch_method', _fetch_method):
        fetcher = CacheURLFetchStrategy(url='file:///not-a-real-cache-file')
        with Stage(fetcher, path=testpath):
            with pytest.raises(NoCacheError, match=r'No cache'):
                fetcher.fetch()


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
@pytest.mark.parametrize('_fetch_method', ['curl', 'urllib'])
def test_fetch(tmpdir, _fetch_method):
    """Ensure a fetch after expanding is effectively a no-op."""
    testpath = str(tmpdir)
    cache = os.path.join(testpath, 'cache.tar.gz')
    touch(cache)
    url = 'file:///{0}'.format(cache)
    with spack.config.override('config:url_fetch_method', _fetch_method):
        fetcher = CacheURLFetchStrategy(url=url)
        with Stage(fetcher, path=testpath) as stage:
            source_path = stage.source_path
            mkdirp(source_path)
            fetcher.fetch()
