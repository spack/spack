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


class IntelMpi(IntelPackage):
    """Intel MPI"""

    homepage = "https://software.intel.com/en-us/intel-mpi-library"

    version('2018.2.199', '6ffeab59c83a8842537484d53e180520',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12748/l_mpi_2018.2.199.tgz')
    version('2018.1.163', '437ce50224c5bbf98fd578a810c3e401',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mpi_2018.1.163.tgz')
    version('2018.0.128', '15b46fc6a3014595de897aa48d3a658b',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12120/l_mpi_2018.0.128.tgz')
    version('2017.4.239', '460a9ef1b3599d60b4d696e3f0f2a14d',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12209/l_mpi_2017.4.239.tgz')
    version('2017.3.196', '721ecd5f6afa385e038777e5b5361dfb',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11595/l_mpi_2017.3.196.tgz')
    version('2017.2.174', 'b6c2e62c3fb9b1558ede72ccf72cf1d6',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11334/l_mpi_2017.2.174.tgz')
    version('2017.1.132', 'd5e941ac2bcf7c5576f85f6bcfee4c18',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11014/l_mpi_2017.1.132.tgz')
    # built from parallel_studio_xe_2016.3.068
    version('5.1.3.223',  '4316e78533a932081b1a86368e890800',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9278/l_mpi_p_5.1.3.223.tgz')

    provides('mpi')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # CAUTION - DUP code in:
        #   ../intel-mpi/package.py
        #   ../intel-parallel-studio/package.py
        #
        # Related: setup_dependent_package() in parent class:
        #   ../../../../../../lib/spack/spack/build_systems/intel.py
        #
        if '+mpi' in self.spec or self.provides('mpi'):
            # See note at compiler_wrappers_mpi() in parent class.
            spack_env.set('I_MPI_CC', spack_cc)
            spack_env.set('I_MPI_CXX', spack_cxx)
            spack_env.set('I_MPI_F77', spack_f77)
            spack_env.set('I_MPI_F90', spack_fc)
            spack_env.set('I_MPI_FC', spack_fc)
            # NB: Normally set by the modulefile, but that is not active here:
            spack_env.set('I_MPI_ROOT', self.normalize_path('mpi'))

            # CAUTION - SIMILAR code in:
            #   ../mpich/package.py
            #   ../openmpi/package.py
            #   ../mvapich2/package.py
            #
            # On Cray, the regular compiler wrappers *are* the MPI wrappers.
            if 'platform=cray' in self.spec:
                # TODO: Confirm
                spack_env.set('MPICC',  spack_cc)
                spack_env.set('MPICXX', spack_cxx)
                spack_env.set('MPIF77', spack_fc)
                spack_env.set('MPIF90', spack_fc)
            else:
                w = self.compiler_wrappers_mpi    # names vary by compiler.name
                spack_env.set('MPICC',  w['MPICC'])
                spack_env.set('MPICXX', w['MPICXX'])
                spack_env.set('MPIF77', w['MPIF77'])
                spack_env.set('MPIF90', w['MPIF90'])
