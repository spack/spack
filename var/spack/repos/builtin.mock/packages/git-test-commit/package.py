# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitTestCommit(Package):
    """Mock package that tests installing specific commit"""
    homepage = "http://www.git-fetch-example.com"

    version('git', git='to-be-filled-in-by-test')

    def install(self, spec, prefix):
        mkdir(prefix.bin)

        # This will only exist for some second commit
        install('file1.txt', prefix.bin)
