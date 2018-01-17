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
import sys

from spack import *
from spack.environment import EnvironmentModifications


class IntelMkl(IntelPackage):
    """Intel Math Kernel Library."""

    homepage = "https://software.intel.com/en-us/intel-mkl"

    version('2018.1.163', 'f1f7b6ddd7eb57dfe39bd4643446dc1c',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mkl_2018.1.163.tgz")
    version('2018.0.128', '0fa23779816a0f2ee23a396fc1af9978',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12070/l_mkl_2018.0.128.tgz")
    version('2017.4.239', '3066272dd0ad3da7961b3d782e1fab3b',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12147/l_mkl_2017.4.239.tgz")
    version('2017.3.196', '4a2eb4bee789391d9c07d7c348a80702',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11544/l_mkl_2017.3.196.tgz")
    version('2017.2.174', 'ef39a12dcbffe5f4a0ef141b8759208c',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11306/l_mkl_2017.2.174.tgz")
    version('2017.1.132', '7911c0f777c4cb04225bf4518088939e',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11024/l_mkl_2017.1.132.tgz")
    version('2017.0.098', '3cdcb739ab5ab1e047eb130b9ffdd8d0',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9662/l_mkl_2017.0.098.tgz")
    version('11.3.3.210', 'f72546df27f5ebb0941b5d21fd804e34',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9068/l_mkl_11.3.3.210.tgz")
    version('11.3.2.181', '536dbd82896d6facc16de8f961d17d65',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8711/l_mkl_11.3.2.181.tgz")

    variant('shared', default=True, description='Builds shared library')
    variant('ilp64', default=False, description='64 bit integers')
    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('openmp', 'none'),
        multi=False
    )

    provides('blas')
    provides('lapack')
    provides('scalapack')
    provides('mkl')

    if sys.platform == 'darwin':
        # there is no libmkl_gnu_thread on macOS
        conflicts('threads=openmp', when='%gcc')

    @property
    def license_required(self):
        # The Intel libraries are provided without requiring a license as of
        # version 2017.2. Trying to specify the license will fail. See:
        # https://software.intel.com/en-us/articles/free-ipsxe-tools-and-libraries
        if self.version >= Version('2017.2'):
            return False
        else:
            return True

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

        if spec.satisfies('threads=openmp'):
            if '%intel' in spec:
                mkl_threading = ['libmkl_intel_thread']
                omp_threading = ['libiomp5']

                if sys.platform != 'darwin':
                    omp_root = prefix.compilers_and_libraries.linux.lib.intel64
                else:
                    omp_root = prefix.lib
                omp_libs = find_libraries(
                    omp_threading, root=omp_root, shared=shared)
            elif '%gcc' in spec:
                mkl_threading = ['libmkl_gnu_thread']

                gcc = Executable(self.compiler.cc)
                libgomp = gcc('--print-file-name', 'libgomp.{0}'.format(
                    dso_suffix), output=str)
                omp_libs = LibraryList(libgomp)

        # TODO: TBB threading: ['libmkl_tbb_thread', 'libtbb', 'libstdc++']

        if sys.platform != 'darwin':
            mkl_root = prefix.compilers_and_libraries.linux.mkl.lib.intel64
        else:
            mkl_root = prefix.mkl.lib

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

        # Intel MKL does not directly depend on mpi but the scalapack
        # interface does and the corresponding  BLACS library changes
        # depending on the MPI implementation we are using. We need then to
        # inspect the root package which asked for Scalapack and check which
        # MPI it depends on.
        root = self.spec.root
        if sys.platform == 'darwin' and '^mpich' in root:
            # MKL 2018 supports only MPICH on darwin
            libnames.append('libmkl_blacs_mpich')
        elif '^openmpi' in root:
            libnames.append('libmkl_blacs_openmpi')
        elif '^mpich@1' in root:
            libnames.append('libmkl_blacs')
        elif '^mpich@2:' in root:
            libnames.append('libmkl_blacs_intelmpi')
        elif '^mvapich2' in root:
            libnames.append('libmkl_blacs_intelmpi')
        elif '^mpt' in root:
            libnames.append('libmkl_blacs_sgimpt')
        elif '^intel-mpi' in root:
            libnames.append('libmkl_blacs_intelmpi')
        else:
            raise InstallError('No MPI found for scalapack')

        integer = 'ilp64' if '+ilp64' in self.spec else 'lp64'
        mkl_root = self.prefix.mkl.lib if sys.platform == 'darwin' else \
            self.prefix.compilers_and_libraries.linux.mkl.lib.intel64

        shared = True if '+shared' in self.spec else False

        libs = find_libraries(
            ['{0}_{1}'.format(l, integer) for l in libnames],
            root=mkl_root,
            shared=shared
        )

        return libs

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # set up MKLROOT for everyone using MKL package
        if sys.platform == 'darwin':
            mkl_lib = self.prefix.mkl.lib
            mkl_root = self.prefix.mkl
        else:
            mkl_lib = self.prefix.compilers_and_libraries.linux.mkl.lib.intel64
            mkl_root = self.prefix.compilers_and_libraries.linux.mkl

        spack_env.set('MKLROOT', mkl_root)
        spack_env.append_path('SPACK_COMPILER_EXTRA_RPATHS', mkl_lib)

    def setup_environment(self, spack_env, run_env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source mkl/bin/mklvars.sh intel64
        """
        # NOTE: Spack runs setup_environment twice, once pre-build to set up
        # the build environment, and once post-installation to determine
        # the environment variables needed at run-time to add to the module
        # file. The script we need to source is only present post-installation,
        # so check for its existence before sourcing.
        # TODO: At some point we should split setup_environment into
        # setup_build_environment and setup_run_environment to get around
        # this problem.
        mklvars = os.path.join(self.prefix.mkl.bin, 'mklvars.sh')

        if sys.platform == 'darwin':
            if os.path.isfile(mklvars):
                run_env.extend(EnvironmentModifications.from_sourcing_file(
                    mklvars))
        else:
            if os.path.isfile(mklvars):
                run_env.extend(EnvironmentModifications.from_sourcing_file(
                    mklvars, 'intel64'))
