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


class Blasr(Package):
    """The PacBio long read aligner."""

    homepage = "https://github.com/PacificBiosciences/blasr/wiki"
    url      = "https://github.com/PacificBiosciences/blasr/archive/5.3.1.tar.gz"

    version('5.3.1', '53c93f499aa4bc10781c87bafc33df2a') 

    depends_on('ncurses')
    depends_on('hdf5+cxx@1.8.12:1.8.99')
    depends_on('htslib')
    depends_on('zlib')
    depends_on('boost')
    depends_on('pbbam')
    depends_on('blasr-libcpp')
    depends_on('python', type='build')

    phases = ['configure', 'build', 'install']

    def setup_environment(self, spack_env, run_env):
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

    def configure(self, spec, prefix):
        configure_args[
            'LIBPBDATA_INC={0}'.format(
                self.spec['blasr-libcpp'].prefix.pbdata),
            'LIBPBDATA_LIB={0}'.format(
                self.spec['blasr-libcpp'].prefix.pbdata),
            'LIBBLASR_LIB={0}'.format(
                self.spec['blasr-libcpp'].prefix.alignment),
            'LIBBLASR_INC={0}'.format(
                self.spec['blasr-libcpp'].prefix.alignment),
            'LIBPBIHDF_INC={0}'.format(self.spec['blasr-libcpp'].prefix.hdf),
            'LIBPBIHDF_LIB={0}'.format(self.spec['blasr-libcpp'].prefix.hdf),
            'HDF5_INC={0}'.format(self.spec['hdf5'].prefix.include),
            'HDF5_LIB={0}'.format(self.spec['hdf5'].prefix.lib),
            '--shared'
        ]
        python('configure.py', *configure_args)

    def build(self):
        make()

    def install(self, spec, prefix):
        mkdir(prefix.utils)
        mkdir(prefix.bin)
        install('blasr', prefix.bin.blasr)
        install('utils/loadPulses', prefix.utils)
        install('utils/pls2fasta', prefix.utils)
        install('utils/samFilter', prefix.utils)
        install('utils/samtoh5', prefix.utils)
        install('utils/samtom4', prefix.utils)
        install('utils/sawriter', prefix.utils)
        install('utils/sdpMatcher', prefix.utils)
        install('utils/toAfg', prefix.utils)
