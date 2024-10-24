# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util.filesystem import working_dir

from spack.util.git import get_modified_files


def test_modified_files(mock_git_version_info, monkeypatch):
    repo_path, filename, commits = mock_git_version_info

    with working_dir(repo_path):
        files = get_modified_files(from_ref="HEAD~1", to_ref="HEAD")
        assert len(files) == 1
        assert files[0] == filename
