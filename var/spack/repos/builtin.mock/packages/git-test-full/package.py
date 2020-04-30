# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitTestFull(Package):
    """Mock package that uses git for fetching."""
    homepage = "http://www.git-fetch-example.com"

    version('git', branch='master', git='to-be-filled-in-by-test', submodules=True)

    def install(self, spec, prefix):
        pass
