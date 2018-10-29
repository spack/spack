# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpiblast(AutotoolsPackage):
    """mpiBLAST is a freely available, open-source, parallel implementation of
       NCBI BLAST"""

    homepage = "http://www.mpiblast.org/"
    url      = "http://www.mpiblast.org/downloads/files/mpiBLAST-1.6.0.tgz"

    version('1.6.0', '707105ccd56825db776b50bfd81cecd5')

    patch('mpiBLAST-1.6.0-patch-110806')

    depends_on('mpi')

    def configure_args(self):
        args = ['--with-mpi=%s' % self.spec['mpi'].prefix]
        return args

    def build(self, spec, prefix):
        make('ncbi')
        make()

    def setup_environment(self, spack_env, run_env):
        spack_env.set('ac_cv_path_CC', self.spec['mpi'].mpicc)
        spack_env.set('ac_cv_path_CXX', self.spec['mpi'].mpicxx)
