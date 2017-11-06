##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
    url      = "https://github.com/QMCPACK/qmcpack.git"

    # This download method is untrusted, and is not recommended
    # by the Spack manual. However, it is easier to maintain
    # because github hashes can occasionally change
    version('3.2.0', git=url, tag='v3.2.0')
    version('3.1.1', git=url, tag='v3.1.1')
    version('3.1.0', git=url, tag='v3.1.0')
    version('3.0.0', git=url, tag='v3.0.0')
    version('develop', git=url)

    # These defaults match those in the QMCPACK manual
    variant('debug', default=False, description='Build debug version')
    variant('mpi', default=True, description='Build with MPI support')
    variant('cuda', default=False,
            description='Enable CUDA and GPU acceleration')
    variant('complex', default=False,
            description='Build the complex (general twist/k-point) version')
    variant('mixed', default=False,
            description='Build the mixed precision (mixture of single and '
                        'double precision) version for gpu and cpu')
    variant('soa', default=False,
            description='Build with Structure-of-Array instead of '
                        'Array-of-Structure code. Only for CPU code'
                        'and only in mixed precision')
    variant('timers', default=False,
             description='Build with support for timers')
    variant('da', default=False,
            description='Install with support for basic data analysis tools')
    variant('gui', default=False,
            description='Install with Matplotlib (long installation time)')

    # cuda variant implies mixed precision variant by default, but there is
    # no way to express this in variant syntax, need something like
    # variant('+mixed', default=True, when='+cuda', description="...")

    # conflicts
    conflicts('+soa', when='+cuda')
    conflicts('^openblas+ilp64')
    conflicts('^intel-mkl+ilp64')

    # Dependencies match those in the QMCPACK manual
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

    # qmcpack data analysis tools
    # basic command line tool based on Python and NumPy
    # blas and lapack patching fails often and so are disabled at this time
    depends_on('py-numpy~blas~lapack', type='run', when='+da')

    # GUI is optional fpr data anlysis
    # py-matplotlib leads to a long complex DAG for dependencies
    depends_on('py-matplotlib', type='run', when='+gui')

    # B-spline basis calculation require a patched version of
    # Quantum Espresso 5.3.0 (see QMCPACK manual)
    patch_url = 'https://raw.githubusercontent.com/QMCPACK/qmcpack/develop/external_codes/quantum_espresso/add_pw2qmcpack_to_espresso-5.3.0.diff'
    patch_checksum = '0d8d7ba805313ddd4c02ee32c96d2f12e7091e9e82e22671d3ad5a24247860c4'
    depends_on('espresso@5.3.0~elpa',
               patches=patch(patch_url, sha256=patch_checksum),
               when='+mpi')

    depends_on('espresso@5.3.0~elpa~scalapack~mpi',
               patches=patch(patch_url, sha256=patch_checksum),
               when='~mpi')

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
        if '+mpi' in self.spec:
            args.append('-DQMC_MPI=1')
        elif '~mpi' in self.spec:
            args.append('-DQMC_MPI=0')

        # Default is real-valued single particle orbitals
        if '+complex' in self.spec:
            args.append('-DQMC_COMPLEX=1')
        elif '~complex' in self.spec:
            args.append('-DQMC_COMPLEX=0')

        # When '-DQMC_CUDA=1', CMake automatically sets:
        # '-DQMC_MIXED_PRECISION=1'
        #
        # There is a double-precision CUDA path, but it is not as well
        # tested.

        if '+cuda' in self.spec:
            args.append('-DQMC_CUDA=1')
        elif '~cuda' in self.spec:
            args.append('-DQMC_CUDA=0')

        # Mixed-precision versues double-precision CPU and GPU code
        if '+mixed' in self.spec:
            args.append('-DQMC_MIXED_PRECISION=1')
        elif '~mixed' in self.spec:
            args.append('-DQMC_MIXED_PRECISION=0')

        # New Structure-of-Array (SOA) code, much faster than default
        # Array-of-Structure (AOS) code.
        # No support for local atomic orbital basis.
        if '+soa' in self.spec:
            args.append('-DENABLE_SOA=1')
        elif '~soa' in self.spec:
            args.append('-DENABLE_SOA=0')

        # Manual Timers
        if '+timers' in self.spec:
            args.append('-DENABLE_TIMERS=1')
        elif '~timers' in self.spec:
            args.append('-DENABLE_TIMERS=0')

    #     # Proper MKL detection not working.
    #     # Include MKL flags
    #     if 'intel-mkl' in self.spec:
    #         args.append('-DBLA_VENDOR=Intel10_64lp_seq')
    #         args.append('-DQMC_INCLUDE={0}'.format(join_path(env['MKLROOT'],'include')))
        return args

    # def setup_environment(self, spack_env, run_env):
    #     # Add MKLROOT/lib to the CMAKE_PREFIX_PATH to enable CMake to find
    #     # MKL libraries. MKLROOT environment variable must be defined for
    #     # this to work properly.
    #     if 'intel-mkl' in self.spec:
    #         spack_env.append_path('CMAKE_PREFIX_PATH',format(join_path(env['MKLROOT'],'lib')))

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
    def check(self):
        """Run ctest after building binary.
        It can take over 24 hours to run all the regression tests, here we
        only run the unit tests and short tests."""
        with working_dir(self.build_directory):
            ctest('-L', 'unit')
            ctest('-R', 'short')
