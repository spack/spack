# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cdhit(MakefilePackage):
    """CD-HIT is a very widely used program for clustering and comparing
       protein or nucleotide sequences."""

    homepage = "http://cd-hit.org/"
    url      = "https://github.com/weizhongli/cdhit/archive/V4.6.8.tar.gz"

    version('4.8.1', sha256='f8bc3cdd7aebb432fcd35eed0093e7a6413f1e36bbd2a837ebc06e57cdb20b70')
    version('4.6.8', 'bdd73ec0cceab6653aab7b31b57c5a8b')

    variant('openmp', default=True, description='Compile with multi-threading support')

    depends_on('perl', type=('build', 'run'))

    def build(self, spec, prefix):
        mkdirp(prefix.bin)
        if '~openmp' in spec:
            make('openmp=no')
        else:
            make()

    def setup_environment(self, spack_env, run_env):
        spack_env.set('PREFIX', prefix.bin)
