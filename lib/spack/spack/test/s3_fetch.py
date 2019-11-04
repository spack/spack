# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.fetch_strategy import S3FetchStrategy
from spack.stage import Stage


def test_s3fetchstrategy_sans_url():
    """Ensure constructor with no URL fails."""
    with pytest.raises(ValueError):
        with S3FetchStrategy(None):
            pass


def test_s3fetchstrategy_bad_url(tmpdir):
    """Ensure fetch with bad URL fails as expected."""
    testpath = str(tmpdir)

    with pytest.raises(ValueError):
        fetcher = S3FetchStrategy(url='file:///does-not-exist')
        assert fetcher is not None

        with Stage(fetcher, path=testpath) as stage:
            assert stage is not None
            assert fetcher.archive_file is None
            fetcher.fetch()
