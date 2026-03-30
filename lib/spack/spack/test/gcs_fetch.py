# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.fetch_strategy
import spack.stage
import spack.util.gcs


def test_gcsfetchstrategy_downloaded(tmp_path: pathlib.Path):
    """Ensure fetch with archive file already downloaded is a noop."""
    archive = tmp_path / "gcs.tar.gz"

    class Archived_GCSFS(spack.fetch_strategy.GCSFetchStrategy):
        @property
        def archive_file(self):
            return str(archive)

    fetcher = Archived_GCSFS(url="gs://example/gcs.tar.gz")
    with spack.stage.Stage(fetcher, path=str(tmp_path)):
        fetcher.fetch()


class GCSTestImportError(Exception):
    pass


def test_gcs_client_env_var(monkeypatch, working_env):
    """Ensure gcs_client sets GCE_METADATA_MTLS_MODE to none."""

    def mock_try_gcs_import():
        raise GCSTestImportError("Custom GCS import error for testing")

    monkeypatch.setattr(spack.util.gcs, "try_gcs_import", mock_try_gcs_import)

    if "GCE_METADATA_MTLS_MODE" in os.environ:
        del os.environ["GCE_METADATA_MTLS_MODE"]

    with pytest.raises(GCSTestImportError):
        spack.util.gcs.gcs_client()

    assert os.environ.get("GCE_METADATA_MTLS_MODE") == "none"
