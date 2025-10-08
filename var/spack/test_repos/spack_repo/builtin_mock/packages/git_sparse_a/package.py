# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class GitSparseA(Package):
    """Partal clone of the mock_git_repository fixture"""

    # git='to-be-filled-in-by-test'

    # ----------------------------
    # -- mock_git_repository
    version("main", branch="many_dirs")
    homepage = "http://www.git-fetch-example.com"

    submodules = True
    git_sparse_paths = ["dir0"]
