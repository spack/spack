# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.fetch_strategy as spack_fs
import spack.stage as spack_stage


def test_s3fetchstrategy_sans_url():
    """Ensure constructor with no URL fails."""
    with pytest.raises(ValueError):
        spack_fs.S3FetchStrategy(None)


def test_s3fetchstrategy_bad_url(tmpdir):
    """Ensure fetch with bad URL fails as expected."""
    testpath = str(tmpdir)

    fetcher = spack_fs.S3FetchStrategy(url='file:///does-not-exist')
    assert fetcher is not None

    with spack_stage.Stage(fetcher, path=testpath) as stage:
        assert stage is not None
        assert fetcher.archive_file is None
        with pytest.raises(spack_fs.FetchError):
            fetcher.fetch()
