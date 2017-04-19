##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os
import re

from spack.pkg.builtin.intel import IntelInstaller, filter_pick, \
    get_all_components


class IntelMpi(IntelInstaller):
    """Intel MPI"""

    homepage = "https://software.intel.com/en-us/intel-mpi-library"

    version('2017.2', '106a4b362c13ddc6978715e50f5f81c58c1a4c70cd2d20a99e94947b7e733b88',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11334/l_mpi_2017.2.174.tgz')
    version('2017.1', '8d30a63674fe05f17b0a908a9f7d54403018bfed2de03c208380b171ab99be82',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11014/l_mpi_2017.1.132.tgz')
    version('5.1.3', '544f4173b09609beba711fa3ba35567397ff3b8390e4f870a3307f819117dd9b',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9278/l_mpi_p_5.1.3.223.tgz')

    provides('mpi')

    def install(self, spec, prefix):
        # FIXME:
        raise RuntimeError('Install method is not implemented yet')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('I_MPI_CC', spack_cc)
        spack_env.set('I_MPI_CXX', spack_cxx)
        spack_env.set('I_MPI_F77', spack_fc)
        spack_env.set('I_MPI_F90', spack_f77)

    def setup_dependent_package(self, module, dep_spec):
        # Check for presence of bin64 or bin directory
        if os.path.isdir(self.prefix.bin):
            bindir = self.prefix.bin
        elif os.path.isdir(join_path(self.prefix, 'bin64')):
            bindir = join_path(self.prefix, 'bin64')
        else:
            raise "No suitable bindir found"

        self.spec.mpicc = join_path(bindir, 'mpicc')
        self.spec.mpicxx = join_path(bindir, 'mpic++')
        self.spec.mpifc = join_path(bindir, 'mpif90')
        self.spec.mpif77 = join_path(bindir, 'mpif77')
