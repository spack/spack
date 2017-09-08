##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import glob
import os

from spack import *
from spack.environment import EnvironmentModifications


class IntelParallelStudio(IntelPackage):
    """Intel Parallel Studio."""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    version('professional.2017.4', '27398416078e1e4005afced3e9a6df7e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11537/parallel_studio_xe_2017_update4.tgz')
    version('cluster.2017.4',      '27398416078e1e4005afced3e9a6df7e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11537/parallel_studio_xe_2017_update4.tgz')
    version('composer.2017.4',     'd03d351809e182c481dc65e07376d9a2',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11541/parallel_studio_xe_2017_update4_composer_edition.tgz')
    version('professional.2017.3', '691874735458d3e88fe0bcca4438b2a9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11460/parallel_studio_xe_2017_update3.tgz')
    version('cluster.2017.3',      '691874735458d3e88fe0bcca4438b2a9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11460/parallel_studio_xe_2017_update3.tgz')
    version('composer.2017.3',     '52344df122c17ddff3687f84ceb21623',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11464/parallel_studio_xe_2017_update3_composer_edition.tgz')
    version('professional.2017.2', '70e54b33d940a1609ff1d35d3c56e3b3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11298/parallel_studio_xe_2017_update2.tgz')
    version('cluster.2017.2',      '70e54b33d940a1609ff1d35d3c56e3b3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11298/parallel_studio_xe_2017_update2.tgz')
    version('composer.2017.2',     '2891ab1ece43eb61b6ab892f07c47f01',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz')
    version('professional.2017.1', '7f75a4a7e2c563be778c377f9d35a542',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10973/parallel_studio_xe_2017_update1.tgz')
    version('cluster.2017.1',      '7f75a4a7e2c563be778c377f9d35a542',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10973/parallel_studio_xe_2017_update1.tgz')
    version('composer.2017.1',     '1f31976931ed8ec424ac7c3ef56f5e85',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz')
    version('professional.2017.0', '34c98e3329d6ac57408b738ae1daaa01',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9651/parallel_studio_xe_2017.tgz')
    version('cluster.2017.0',      '34c98e3329d6ac57408b738ae1daaa01',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9651/parallel_studio_xe_2017.tgz')
    version('composer.2017.0',     'b67da0065a17a05f110ed1d15c3c6312',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9656/parallel_studio_xe_2017_composer_edition.tgz')
    version('professional.2016.4', '16a641a06b156bb647c8a56e71f3bb33',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9781/parallel_studio_xe_2016_update4.tgz')
    version('cluster.2016.4',      '16a641a06b156bb647c8a56e71f3bb33',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9781/parallel_studio_xe_2016_update4.tgz')
    version('composer.2016.4',      '2bc9bfc9be9c1968a6e42efb4378f40e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz')
    version('professional.2016.3', 'eda19bb0d0d19709197ede58f13443f3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9061/parallel_studio_xe_2016_update3.tgz')
    version('cluster.2016.3',      'eda19bb0d0d19709197ede58f13443f3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9061/parallel_studio_xe_2016_update3.tgz')
    version('composer.2016.3',     '3208eeabee951fc27579177b593cefe9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz')
    version('professional.2016.2', '70be832f2d34c9bf596a5e99d5f2d832',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8676/parallel_studio_xe_2016_update2.tgz')
    version('cluster.2016.2',      '70be832f2d34c9bf596a5e99d5f2d832',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8676/parallel_studio_xe_2016_update2.tgz')
    version('composer.2016.2',     '1133fb831312eb519f7da897fec223fa',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz')
    version('professional.2015.6', 'd460f362c30017b60f85da2e51ad25bf',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8469/parallel_studio_xe_2015_update6.tgz')
    version('cluster.2015.6',      'd460f362c30017b60f85da2e51ad25bf',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8469/parallel_studio_xe_2015_update6.tgz')
    version('composer.2015.6',      'da9f8600c18d43d58fba0488844f79c9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8432/l_compxe_2015.6.233.tgz')

    # Generic Variants
    variant('rpath',    default=True,
            description='Add rpath to .cfg files')
    variant('newdtags', default=False,
            description='Allow use of --enable-new-dtags in MPI wrappers')
    variant('shared',   default=True,
            description='Builds shared library')
    variant('ilp64',    default=False,
            description='64 bit integers')
    variant('openmp',   default=False,
            description='OpenMP multithreading layer')

    # Components available in all editions
    variant('daal', default=True,
            description='Install the Intel DAAL libraries')
    variant('gdb',  default=False,
            description='Install the Intel Debugger for Heterogeneous Compute')
    variant('ipp',  default=True,
            description='Install the Intel IPP libraries')
    variant('mkl',  default=True,
            description='Install the Intel MKL library')
    variant('mpi',  default=True,
            description='Install the Intel MPI library')
    variant('tbb',  default=True,
            description='Install the Intel TBB libraries')

    # Components only available in the Professional and Cluster Editions
    variant('advisor',   default=False,
            description='Install the Intel Advisor')
    variant('clck',      default=False,
            description='Install the Intel Cluster Checker')
    variant('inspector', default=False,
            description='Install the Intel Inspector')
    variant('itac',      default=False,
            description='Install the Intel Trace Analyzer and Collector')
    variant('vtune',     default=False,
            description='Install the Intel VTune Amplifier XE')

    provides('daal', when='+daal')

    provides('ipp', when='+ipp')

    provides('mkl',       when='+mkl')
    provides('blas',      when='+mkl')
    provides('lapack',    when='+mkl')
    provides('scalapack', when='+mkl')

    provides('mpi', when='+mpi')

    provides('tbb', when='+tbb')

    # The following components are not available in the Composer Edition
    conflicts('+advisor',   when='@composer.0:composer.9999')
    conflicts('+clck',      when='@composer.0:composer.9999')
    conflicts('+inspector', when='@composer.0:composer.9999')
    conflicts('+itac',      when='@composer.0:composer.9999')
    conflicts('+vtune',     when='@composer.0:composer.9999')

    @property
    def blas_libs(self):
        spec = self.spec
        prefix = self.prefix
        shared = '+shared' in spec

        if '+ilp64' in spec:
            mkl_integer = ['libmkl_intel_ilp64']
        else:
            mkl_integer = ['libmkl_intel_lp64']

        mkl_threading = ['libmkl_sequential']

        omp_libs = LibraryList([])

        if '+openmp' in spec:
            if '%intel' in spec:
                mkl_threading = ['libmkl_intel_thread']
                omp_threading = ['libiomp5']

                omp_root = prefix.compilers_and_libraries.linux.lib.intel64
                omp_libs = find_libraries(
                    omp_threading, root=omp_root, shared=shared)
            elif '%gcc' in spec:
                mkl_threading = ['libmkl_gnu_thread']

                gcc = Executable(self.compiler.cc)
                omp_libs = gcc('--print-file-name', 'libgomp.{0}'.format(
                    dso_suffix), output=str)
                omp_libs = LibraryList(omp_libs)

        # TODO: TBB threading: ['libmkl_tbb_thread', 'libtbb', 'libstdc++']

        mkl_root = prefix.compilers_and_libraries.linux.mkl.lib.intel64

        mkl_libs = find_libraries(
            mkl_integer + ['libmkl_core'] + mkl_threading,
            root=mkl_root,
            shared=shared
        )

        # Intel MKL link line advisor recommends these system libraries
        system_libs = find_system_libraries(
            ['libpthread', 'libm', 'libdl'],
            shared=shared
        )

        return mkl_libs + omp_libs + system_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        libnames = ['libmkl_scalapack']
        if self.spec.satisfies('^openmpi'):
            libnames.append('libmkl_blacs_openmpi')
        elif self.spec.satisfies('^mpich@1'):
            libnames.append('libmkl_blacs')
        elif self.spec.satisfies('^mpich@2:'):
            libnames.append('libmkl_blacs_intelmpi')
        elif self.spec.satisfies('^mvapich2'):
            libnames.append('libmkl_blacs_intelmpi')
        elif self.spec.satisfies('^mpt'):
            libnames.append('libmkl_blacs_sgimpt')
        # TODO: ^intel-parallel-studio can mean intel mpi, a compiler or a lib
        # elif self.spec.satisfies('^intel-parallel-studio'):
        #     libnames.append('libmkl_blacs_intelmpi')
        else:
            raise InstallError('No MPI found for scalapack')

        integer = 'ilp64' if '+ilp64' in self.spec else 'lp64'
        mkl_root = self.prefix.compilers_and_libraries.linux.mkl.lib.intel64
        shared = True if '+shared' in self.spec else False

        libs = find_libraries(
            ['{0}_{1}'.format(l, integer) for l in libnames],
            root=mkl_root,
            shared=shared
        )
        return libs

    @property
    def mpi_libs(self):
        mpi_root = self.prefix.compilers_and_libraries.linux.mpi.lib64
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpifort', 'libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpicxx'] + libraries

        return find_libraries(
            libraries, root=mpi_root, shared=True, recurse=True
        )

    @property
    def mpi_headers(self):
        # recurse from self.prefix will find too many things for all the
        # supported sub-architectures like 'mic'
        mpi_root = self.prefix.compilers_and_libraries.linux.mpi.include64
        return find_headers('mpi', root=mpi_root, recurse=False)

    @property
    def components(self):
        spec = self.spec
        edition = self.version[0]

        # Intel(R) Compilers
        components = [
            # Common files
            'intel-comp-',
            'intel-openmp',

            # C/C++
            'intel-icc',

            # Fortran
            'intel-ifort',

            # Parallel Studio Documentation and Licensing Files
            'intel-psxe',
        ]

        # Intel(R) Parallel Studio XE Suite Files and Documentation
        if edition == 'cluster':
            components.append('intel-icsxe')
        elif edition == 'professional':
            components.extend(['intel-ips', 'intel-ipsc', 'intel-ipsf'])
        elif edition == 'composer':
            components.extend([
                'intel-compxe', 'intel-ccompxe', 'intel-fcompxe'
            ])

        # Intel(R) Data Analytics Acceleration Library
        if '+daal' in spec:
            components.append('intel-daal')

        # Intel(R) Debugger for Heterogeneous Compute
        if '+gdb' in spec:
            components.append('intel-gdb')

        # Intel(R) Integrated Performance Primitives
        if '+ipp' in spec:
            components.extend(['intel-ipp', 'intel-crypto-ipp'])

        # Intel(R) Math Kernel Library
        if '+mkl' in spec:
            components.append('intel-mkl')

        # Intel(R) MPI Library
        if '+mpi' in spec:
            components.extend(['intel-mpi', 'intel-mpirt', 'intel-imb'])

        # Intel(R) Threading Building Blocks
        if '+tbb' in spec:
            components.append('intel-tbb')

        # Intel(R) Advisor
        if '+advisor' in spec:
            components.append('intel-advisor')

        # Intel(R) Cluster Checker
        if '+clck' in spec:
            components.append('intel_clck')

        # Intel(R) Inspector
        if '+inspector' in spec:
            components.append('intel-inspector')

        # Intel(R) Trace Analyzer and Collector
        if '+itac' in spec:
            components.extend(['intel-itac', 'intel-ta', 'intel-tc'])

        # Intel(R) VTune(TM) Amplifier XE
        if '+vtune' in spec:
            components.append('intel-vtune-amplifier-xe')

        return components

    @property
    def bin_dir(self):
        """The relative path to the bin directory with symlinks resolved."""

        bin_path = os.path.join(self.prefix.bin, 'icc')
        absolute_path = os.path.realpath(bin_path)  # resolve symlinks
        relative_path = os.path.relpath(absolute_path, self.prefix)
        return os.path.dirname(relative_path)

    @property
    def lib_dir(self):
        """The relative path to the lib directory with symlinks resolved."""

        lib_path = os.path.join(self.prefix.lib, 'intel64', 'libimf.a')
        absolute_path = os.path.realpath(lib_path)  # resolve symlinks
        relative_path = os.path.relpath(absolute_path, self.prefix)
        return os.path.dirname(relative_path)

    @property
    def license_files(self):
        spec = self.spec
        year = self.version[1]

        directories = [
            'Licenses',
            self.bin_dir
        ]

        if '+advisor' in spec:
            advisor_dir = 'advisor_xe/licenses'

            if year >= 2017:
                advisor_dir = 'advisor/licenses'

            directories.append(advisor_dir)

        if '+inspector' in spec:
            inspector_dir = 'inspector_xe/licenses'

            if year >= 2017:
                inspector_dir = 'inspector/licenses'

            directories.append(inspector_dir)

        if '+itac' in spec:
            itac_dir = 'itac_{0}'.format(year)

            directories.append(itac_dir)

        if '+vtune' in spec:
            vtune_dir = 'vtune_amplifier_xe/licenses'

            directories.append(vtune_dir)

        return [os.path.join(dir, 'license.lic') for dir in directories]

    @run_after('install')
    def filter_compiler_wrappers(self):
        spec = self.spec

        if '+mpi' in spec:
            if '~newdtags' in spec:
                wrappers = [
                    'mpif77', 'mpif90', 'mpigcc', 'mpigxx',
                    'mpiicc', 'mpiicpc', 'mpiifort'
                ]
                wrapper_paths = []
                for root, dirs, files in os.walk(spec.prefix):
                    for name in files:
                        if name in wrappers:
                            wrapper_paths.append(os.path.join(spec.prefix,
                                                              root, name))
                for wrapper in wrapper_paths:
                    filter_file('-Xlinker --enable-new-dtags', ' ',
                                wrapper, string=True)

    @run_after('install')
    def rpath_configuration(self):
        spec = self.spec

        if '+rpath' in spec:
            lib_dir = os.path.join(self.prefix, self.lib_dir)
            for compiler in ['icc', 'icpc', 'ifort']:
                cfgfilename = os.path.join(
                    self.prefix, self.bin_dir, '{0}.cfg'.format(compiler))
                with open(cfgfilename, 'w') as f:
                    f.write('-Xlinker -rpath -Xlinker {0}\n'.format(lib_dir))

    @run_after('install')
    def fix_psxevars(self):
        """Newer versions of Intel Parallel Studio have a bug in the
        ``psxevars.sh`` script."""

        bindir = glob.glob(join_path(
            self.prefix, 'parallel_studio*', 'bin'))[0]

        filter_file('^SCRIPTPATH=.*', 'SCRIPTPATH={0}'.format(self.prefix),
                    os.path.join(bindir, 'psxevars.sh'),
                    os.path.join(bindir, 'psxevars.csh'))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if '+mpi' in self.spec:
            spack_env.set('I_MPI_CC',  spack_cc)
            spack_env.set('I_MPI_CXX', spack_cxx)
            spack_env.set('I_MPI_F77', spack_fc)
            spack_env.set('I_MPI_F90', spack_f77)
            spack_env.set('I_MPI_FC',  spack_fc)

        # set up MKLROOT for everyone using MKL package
        if '+mkl' in self.spec:
            mkl_root = self.prefix.compilers_and_libraries.linux.mkl.lib.intel64  # noqa

            spack_env.set('MKLROOT', self.prefix)
            spack_env.append_path('SPACK_COMPILER_EXTRA_RPATHS', mkl_root)

    def setup_dependent_package(self, module, dep_spec):
        if '+mpi' in self.spec:
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
            bindir = self.prefix.compilers_and_libraries.linux.mpi.intel64.bin

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

           $ source parallel_studio_xe_2017/bin/psxevars.sh intel64
        """
        # NOTE: Spack runs setup_environment twice, once pre-build to set up
        # the build environment, and once post-installation to determine
        # the environment variables needed at run-time to add to the module
        # file. The script we need to source is only present post-installation,
        # so check for its existence before sourcing.
        # TODO: At some point we should split setup_environment into
        # setup_build_environment and setup_run_environment to get around
        # this problem.
        psxevars = glob.glob(join_path(
            self.prefix, 'parallel_studio*', 'bin', 'psxevars.sh'))

        if psxevars:
            run_env.extend(EnvironmentModifications.from_sourcing_file(
                psxevars[0], 'intel64'))
