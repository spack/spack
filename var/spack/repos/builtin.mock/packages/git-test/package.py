# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GitTest(Package):
    """Mock package that uses git for fetching."""
    homepage = "http://www.git-fetch-example.com"
    # To be set by test
    git = 'to-be-filled-in-by-test'

    submodules = True

    version('git', branch='git')
