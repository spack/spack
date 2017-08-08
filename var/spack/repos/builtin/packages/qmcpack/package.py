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


class Qmcpack(CMakePackage):
    """QMCPACK, is a modern high-performance open-source Quantum Monte
       Carlo (QMC) simulation code."""

    # Package information
    homepage = "http://www.qmcpack.org/"
    url      = "https://github.com/QMCPACK/qmcpack/archive/v3.1.0.tar.gz"

    version('3.1.0', 'bdf3acd090557acdb6cab5ddbf7c7960')
    version('3.0.0', '75f9cf70e6cc6d8b7ff11a86340da43d')

    # This download method is untrusted, and is not recommended
    # by the Spack manual.
    version('develop', git='https://github.com/QMCPACK/qmcpack.git')

    # These defaults match those in the QMCPACK manual
    variant('debug', default=False, description='Build debug version')
    variant('mpi', default=True, description='Build with MPI support')
    variant('cuda', default=False,
            description='Enable CUDA and GPU acceleration.')
    variant('complex', default=True,
            description='Build the complex (general twist/k-point) version')
    variant('mixed', default=False,
            description='Build the mixed precision (mixture of single and '
                        'double precision) version for gpu and cpu '
                        '(experimental)')
    variant('gui', default=False,
            description='Install with Matplotlib (long installation time)')

    depends_on('cmake@3.4.3:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('libxml2')
    depends_on('hdf5')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('boost')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw')
    depends_on('fftw+mpi', when='+mpi')
    depends_on('fftw~mpi', when='~mpi')
    depends_on('cuda', when='+cuda')

    # qmcpack needs these for data analysis
    depends_on('python', type='run')
    depends_on('py-numpy', type='run')

    # GUI is optional and leads to a long complex DAG for dependencies
    depends_on('py-matplotlib', type='run', when='+gui')

    # B-spline basis calculation require a patched version of
    # Quantum Espresso 5.3.0 (see QMCPACK manual)
    depends_on('espresso@5.3.0+qmcpackconv~elpa', when='+mpi')
    depends_on('espresso@5.3.0+qmcpackconv~elpa~scalapack~mpi', when='~mpi')

    def patch(self):
        # FindLibxml2QMC.cmake doesn't check the environment by default
        # for libxml2, so we fix that.
        filter_file(r'$ENV{LIBXML2_HOME}/lib',
                    '${LIBXML2_HOME}/lib $ENV{LIBXML2_HOME}/lib',
                    'CMake/FindLibxml2QMC.cmake')

    def cmake_args(self):
        args = []

        if '+mpi' in self.spec:
            mpi = self.spec['mpi']
            args.append('-DCMAKE_C_COMPILER={0}'.format(mpi.mpicc))
            args.append('-DCMAKE_CXX_COMPILER={0}'.format(mpi.mpicxx))
            args.append('-DMPI_BASE_DIR:PATH={0}'.format(mpi.prefix))

        # Currently FFTW_HOME and LIBXML2_HOME are used by CMake.
        # Any CMake warnings about other variables are benign.
        xml2_prefix = self.spec['libxml2'].prefix
        args.append('-DLIBXML2_HOME={0}'.format(xml2_prefix))
        args.append('-DLibxml2_INCLUDE_DIRS={0}'.format(xml2_prefix.include))
        args.append('-DLibxml2_LIBRARY_DIRS={0}'.format(xml2_prefix.lib))

        fftw_prefix = self.spec['fftw'].prefix
        args.append('-DFFTW_HOME={0}'.format(fftw_prefix))
        args.append('-DFFTW_INCLUDE_DIRS={0}'.format(fftw_prefix.include))
        args.append('-DFFTW_LIBRARY_DIRS={0}'.format(fftw_prefix.lib))

        args.append('-DBOOST_ROOT={0}'.format(self.spec['boost'].prefix))
        args.append('-DHDF5_ROOT={0}'.format(self.spec['hdf5'].prefix))

        # Default is MPI, serial version is convenient for cases, e.g. laptops
        if '~mpi' in self.spec:
            args.append('-DQMC_MPI=0')

        # When '-DQMC_CUDA=1', CMake automatically sets:
        # '-DQMC_MIXED_PRECISION=1'
        #
        # Note: there is a double-precision CUDA path, but it is deprecated
        if '+cuda' in self.spec:
            args.append('-DQMC_CUDA=1')

        # this is for the experimental mixed-prescision CPU code
        if '+mixed' in self.spec:
            args.append('-DQMC_MIXED_PRECISION=1')

        return args

    def install(self, spec, prefix):
        """Make the install targets"""

        # QMCPACK 'make install' does nothing, which causes
        # Spack to throw an error.
        #
        # This install method creates the top level directory
        # and copies the bin subdirectory into the appropriate
        # location. We do not copy include or lib at this time due
        # to technical difficulties in qmcpack itself.

        mkdirp(prefix)

        # We assume cwd is self.stage.source_path

        # install manual
        install_tree('manual', prefix.manual)

        # install nexus
        install_tree('nexus', prefix.nexus)

        with working_dir(self.build_directory):
            mkdirp(prefix)

            # install binaries
            install_tree('bin', prefix.bin)

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        """Run ctest after building binary.
        Use 'spack install --run-tests qmcpack'.
        It can take 24 hours to run all the regression tests.
        We only run the unit tests and short tests."""
        ctest('-L unit')
        ctest('-R short')
