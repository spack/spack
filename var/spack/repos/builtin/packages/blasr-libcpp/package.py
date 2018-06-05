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


class BlasrLibcpp(Package):
    """Blasr_libcpp is a library used by blasr
    and other executables such as samtoh5,
    loadPulses for analyzing PacBio sequences."""

    homepage = "https://github.com/PacificBiosciences/blasr_libcpp"
    url      = "https://github.com/PacificBiosciences/blasr_libcpp/archive/5.3.1.tar.gz"

    version('5.3.1', 'ca770042cbca508d5ff12dff0d645045')

    depends_on('pbbam')
    depends_on('hdf5+cxx@1.8.12:1.8.99')
    # maximum version is 1.8.20 currently. There doesn't appear to be a
    # major version 1.9 and the 1.10.1 version doesn't build correctly.
    # https://github.com/PacificBiosciences/blasr/issues/355

    depends_on('python', type='build')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        configure_args[
            'PBBAM_INC={0}'.format(self.spec['pbbam'].prefix.include),
            'PBBAM_LIB={0}'.format(self.spec['pbbam'].prefix.lib),
            'HDF5_INC={0}'.format(self.spec['hdf5'].prefix.include),
            'HDF5_LIB={0}'.format(self.spec['hdf5'].prefix.lib)
        ]
        python('configure.py', *configure_args)

    def setup_dependent_environment(self, spack_env, run_env):
        run_env.prepend_path('LD_LIBRARY_PATH',
                             self.spec['blasr-libcpp'].prefix.hdf)
        run_env.prepend_path('LD_LIBRARY_PATH',
                             self.spec['blasr-libcpp'].prefix.alignment)
        run_env.prepend_path('LD_LIBRARY_PATH',
                             self.spec['blasr-libcpp'].prefix.pbdata)
        run_env.prepend_path('PATH', self.spec.prefix.utils)

        # hdf has +mpi by default, so handle that possibility
        if ('+mpi' in self.spec['hdf5']):
            spack_env.set('CC', self.spec['mpi'].mpicc)
            spack_env.set('CXX', self.spec['mpi'].mpicxx)

    def build(self):
        make()

    def install(self, spec, prefix):
        install_tree('alignment', prefix.alignment)
        install_tree('hdf', prefix.hdf)
        install_tree('pbdata', prefix.pbdata)
