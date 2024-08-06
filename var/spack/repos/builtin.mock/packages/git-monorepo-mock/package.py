# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GitMonorepoMock(Package):
    """Mock package that tests installing specific commit"""

    homepage = "http://www.git-fetch-example.com"
    # git='to-be-filled-in-by-test'
    git = None

    version("1.0", tag="v1.0")
    version("git", git=None)

    git_sparse_paths = ["foo", "bar", "bing/bang"]
