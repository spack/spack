# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.config
import spack.fetch_strategy
import spack.stage
from spack.util.web import FetchError


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_gcsfetchstrategy_without_url(_fetch_method):
    """Ensure constructor with no URL fails."""
    with spack.config.override("config:url_fetch_method", _fetch_method):
        with pytest.raises(ValueError):
            spack.fetch_strategy.GCSFetchStrategy(None)


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_gcsfetchstrategy_bad_url(tmpdir, _fetch_method):
    """Ensure fetch with bad URL fails as expected."""
    testpath = str(tmpdir)

    with spack.config.override("config:url_fetch_method", _fetch_method):
        fetcher = spack.fetch_strategy.GCSFetchStrategy(url="file:///does-not-exist")
        assert fetcher is not None

        with spack.stage.Stage(fetcher, path=testpath) as stage:
            assert stage is not None
            assert fetcher.archive_file is None
            with pytest.raises(FetchError):
                fetcher.fetch()


@pytest.mark.parametrize("_fetch_method", ["curl", "urllib"])
def test_gcsfetchstrategy_downloaded(tmpdir, _fetch_method):
    """Ensure fetch with archive file already downloaded is a noop."""
    testpath = str(tmpdir)
    archive = os.path.join(testpath, "gcs.tar.gz")

    with spack.config.override("config:url_fetch_method", _fetch_method):

        class Archived_GCSFS(spack.fetch_strategy.GCSFetchStrategy):
            @property
            def archive_file(self):
                return archive

        url = "gcs:///{0}".format(archive)
        fetcher = Archived_GCSFS(url=url)
        with spack.stage.Stage(fetcher, path=testpath):
            fetcher.fetch()
