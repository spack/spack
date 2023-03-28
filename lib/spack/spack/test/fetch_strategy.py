# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from unittest.mock import MagicMock, patch

import pytest

from spack import fetch_strategy, stage

def test_fetchstrategy_bad_url_scheme():
    """Ensure that trying to make a fetch strategy from a URL with an
    unsupported scheme fails as expected."""

    with pytest.raises(ValueError):
        fetcher = fetch_strategy.from_url_scheme("bogus-scheme://example.com/a/b/c")  # noqa: F841


archive_test_data = [
    ("cvs", fetch_strategy.CvsFetchStrategy, "CVS", False),
    ("cvs", fetch_strategy.CvsFetchStrategy, "CVS", True),
    ("git", fetch_strategy.GitFetchStrategy, ".git", False),
    ("git", fetch_strategy.GitFetchStrategy, ".git", True),
    ("go", fetch_strategy.GoFetchStrategy, ".git", False),
    ("go", fetch_strategy.GoFetchStrategy, ".git", True),
    ("hg", fetch_strategy.HgFetchStrategy, ".hg", False),
    ("hg", fetch_strategy.HgFetchStrategy, ".hg", True),
    ("svn", fetch_strategy.SvnFetchStrategy, ".svn", False),
    ("svn", fetch_strategy.SvnFetchStrategy, ".svn", True),
]


@pytest.mark.parametrize("vcs,strategy,exclude_dir,archive_vcs_info", archive_test_data)
def test_archive_vcs_info(tmpdir, vcs, strategy, exclude_dir, archive_vcs_info):
    """
    Ensure that the VCS info dir is excluded by default, archived when requested
    """
    strategy_args = {vcs: "https://your-vcs-url-here"}
    if archive_vcs_info:
        strategy_args["archive_vcs_info"] = True

    strategy = strategy(**strategy_args)
    archive = os.sep.join([str(tmpdir), "archive.tar.gz"])

    with stage.Stage(strategy):
        with patch("spack.fetch_strategy.which") as patched_which:
            tar = MagicMock()
            patched_which.return_value = tar
            strategy.archive(archive)
            if archive_vcs_info:
                tar.add_default_arg.assert_not_called()
            else:
                tar.add_default_arg.assert_called_once()
                tar.add_default_arg.assert_called_with(f"--exclude={exclude_dir}")
