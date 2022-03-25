# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitTestCommit(Package):
    """Mock package that tests installing specific commit"""
    homepage = "http://www.git-fetch-example.com"
    # git='to-be-filled-in-by-test'

    version('1.0', tag='v1.0')
    version('1.1', tag='v1.1')
    version('1.2', tag='1.2')  # not a typo
    version('2.0', tag='v2.0')

    def install(self, spec, prefix):
        # assert spec.satisfies('@:0')
        mkdir(prefix.bin)

        # This will only exist for some second commit
        install('file.txt', prefix.bin)
