##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os

from spack import *
from spack.environment import EnvironmentModifications


class IntelMpi(IntelPackage):
    """Intel MPI"""

# https://software.intel.com/en-us/articles/intel-mpi-library-release-notes-linux
# Intel® MPI Library 2018 Update 2
#   ...
#   Intel® MPI Library is now available to install in YUM and APT repositories.
#   ...
# See also:
# https://software.intel.com/en-us/articles/installing-intel-free-libs-and-python-yum-repo
# https://software.intel.com/en-us/articles/installing-intel-parallel-studio-xe-on-aws-linux-instances

    homepage = "https://software.intel.com/en-us/intel-mpi-library"

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
    version('5.1.3.223',  '4316e78533a932081b1a86368e890800',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9278/l_mpi_p_5.1.3.223.tgz')

    provides('mpi')

    @property
    def license_required(self):
        # The Intel libraries are provided without requiring a license as of
        # version 2017.2. Trying to specify the license will fail. See:
        # https://software.intel.com/en-us/articles/free-ipsxe-tools-and-libraries
        return self.version < Version('2017.2')

    @property
    def mpi_libs(self):
        # If prefix is too general, recursive searches may get file variants
        # from supported but inappropriate sub-architectures like 'mic'.
        libnames = ['libmpifort', 'libmpi']
        if 'cxx' in self.spec.last_query.extra_parameters:
            libnames = ['libmpicxx'] + libnames
        return find_libraries(libnames,
                              root=self.component_libdir,
                              shared=True, recursive=True)

    @property
    def mpi_headers(self):
        return find_headers('mpi',
                            root=self.component_includedir,
                            recursive=False)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('I_MPI_CC', spack_cc)
        spack_env.set('I_MPI_CXX', spack_cxx)
        spack_env.set('I_MPI_F77', spack_fc)
        spack_env.set('I_MPI_F90', spack_f77)
        spack_env.set('I_MPI_FC', spack_fc)

        # Convenience variable.
        spack_env.set('I_MPI_ROOT', self.product_component_dir)

    def setup_dependent_package(self, module, dep_spec):
        # Intel comes with 2 different flavors of MPI wrappers:
        #
        # * mpiicc, mpiicpc, and mpifort are hardcoded to wrap around
        #   the Intel compilers.
        # * mpicc, mpicxx, mpif90, and mpif77 allow you to set which
        #   compilers to wrap using I_MPI_CC and friends. By default,
        #   wraps around the GCC compilers.
        #
        # In theory, these should be equivalent as long as I_MPI_CC
        # and friends are set to point to the Intel compilers, but in
        # practice, mpicc fails to compile some applications while
        # mpiicc works.
        bindir = self.component_bindir
        if self.compiler.name == 'intel':
            self.spec.mpicc  = bindir.mpiicc
            self.spec.mpicxx = bindir.mpiicpc
            self.spec.mpifc  = bindir.mpiifort
            self.spec.mpif77 = bindir.mpiifort
        else:
            self.spec.mpicc  = bindir.mpicc
            self.spec.mpicxx = bindir.mpicxx
            self.spec.mpifc  = bindir.mpif90
            self.spec.mpif77 = bindir.mpif77

    def setup_environment(self, spack_env, run_env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh
        """
        # NOTE: Spack runs setup_environment twice, once pre-build to set up
        # the build environment, and once post-installation to determine
        # the environment variables needed at run-time to add to the module
        # file. The script we need to source is only present post-installation,
        # so check for its existence before sourcing.
        # TODO: At some point we should split setup_environment into
        # setup_build_environment and setup_run_environment to get around
        # this problem.
        f = join_path(self.component_bindir, 'mpivars.sh')
        if os.path.isfile(f):
            run_env.extend(EnvironmentModifications.from_sourcing_file(f))
