##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
