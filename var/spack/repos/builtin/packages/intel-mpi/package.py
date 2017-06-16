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

from spack.pkg.builtin.intel import IntelInstaller


class IntelMpi(IntelInstaller):
    """Intel MPI"""

    homepage = "https://software.intel.com/en-us/intel-mpi-library"

    version('2017.3', '721ecd5f6afa385e038777e5b5361dfb',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11595/l_mpi_2017.3.196.tgz')
    version('2017.2', 'b6c2e62c3fb9b1558ede72ccf72cf1d6',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11334/l_mpi_2017.2.174.tgz')
    version('2017.1', 'd5e941ac2bcf7c5576f85f6bcfee4c18',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11014/l_mpi_2017.1.132.tgz')
    version('5.1.3', '4316e78533a932081b1a86368e890800',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9278/l_mpi_p_5.1.3.223.tgz')

    provides('mpi')

    @property
    def mpi_libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpifort', 'libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpicxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix.lib64, shared=True, recurse=True
        )

    @property
    def mpi_headers(self):
        # recurse from self.prefix will find too many things for all the
        # supported sub-architectures like 'mic'
        return find_headers(
            'mpi', root=self.prefix.include64, recurse=False)

    def install(self, spec, prefix):
        self.intel_prefix = prefix
        IntelInstaller.install(self, spec, prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('I_MPI_CC', spack_cc)
        spack_env.set('I_MPI_CXX', spack_cxx)
        spack_env.set('I_MPI_F77', spack_fc)
        spack_env.set('I_MPI_F90', spack_f77)
        spack_env.set('I_MPI_FC', spack_fc)

    def setup_dependent_package(self, module, dep_spec):
        # Check for presence of bin64 or bin directory
        if os.path.isdir(self.prefix.bin):
            bindir = self.prefix.bin
        elif os.path.isdir(self.prefix.bin64):
            bindir = self.prefix.bin64
        else:
            raise RuntimeError('No suitable bindir found')

        self.spec.mpicc = join_path(bindir, 'mpicc')
        self.spec.mpicxx = join_path(bindir, 'mpicxx')
        self.spec.mpifc = join_path(bindir, 'mpif90')
        self.spec.mpif77 = join_path(bindir, 'mpif77')
