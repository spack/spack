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
from spack.build_systems.intel import debug_print, raise_lib_error


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
        return self.version < Version('2017.2')

    @property
    def _want_shared(self):
        return ('+shared' in self.spec)

    @property
    def blas_libs(self):
        # Main magic here.
        # For reference, see The Intel Math Kernel Library Link Line Advisor:
        # https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor/

        mkl_libnames = ['libmkl_intel_' + self.intel64_int_suffix]
        if not self.spec.satisfies('threads=openmp'):
            mkl_libnames.append('libmkl_sequential')
        elif '%intel' in self.spec:
            mkl_libnames.append('libmkl_intel_thread')
        elif '%gcc' in self.spec:
            mkl_libnames.append('libmkl_gnu_thread')
        else:
            raise_lib_error('Cannot determine MKL threading libraries.')
        mkl_libnames.append('libmkl_core')

        mkl_libs = find_libraries(
            mkl_libnames,
            root=self.component_lib_dir,
            shared=self._want_shared)
        debug_print(mkl_libs)

        if len(mkl_libs) < 3:
            raise_lib_error('Cannot locate core MKL libraries:', mkl_libnames)

        # TODO? TBB threading: ['libmkl_tbb_thread', 'libtbb', 'libstdc++']
        #
        # NB: TBB is C++, and I don't think here is the right place to try
        # messing with compiler specifics to spit out the right libtbb and
        # libstdc++. Can't a user now use the Spack 'tbb' provider concept?

        if self.spec.satisfies('threads=openmp'):
            omp_libs = self.omp_libs()
        else:
            omp_libs = LibraryList([])

        # The Intel MKL link line advisor recommends these system libraries
        system_libs = find_system_libraries(
            'libpthread libm libdl'.split(),
            shared=self._want_shared)
        debug_print(system_libs)

        return mkl_libs + omp_libs + system_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        # Intel MKL does not directly depend on MPI but the BLACS library
        # which underlies ScaLapack does. It comes in several personalities;
        # we must supply a personality matching the MPI implementation that
        # is active for the root package that asked for ScaLapack.
        spec_root = self.spec.root
        if sys.platform == 'darwin' and '^mpich' in spec_root:
            # The only supported choice for MKL 2018 on Mac.
            blacs_lib = 'libmkl_blacs_mpich'
        elif '^openmpi' in spec_root:
            blacs_lib = 'libmkl_blacs_openmpi'
        elif '^mpich@1' in spec_root:
            # Was supported only up to 2015.
            blacs_lib = 'libmkl_blacs'
        elif ('^mpich@2:' in spec_root
              or '^mvapich2' in spec_root
              or '^intel-mpi' in spec_root):
            blacs_lib = 'libmkl_blacs_intelmpi'
        elif '^mpt' in spec_root:
            blacs_lib = 'libmkl_blacs_sgimpt'
        else:
            raise_lib_error('Cannot find a BLACS library for the given MPI.')

        int_suff = '_' + self.intel64_int_suffix
        scalapack_libnames = [
            'libmkl_scalapack' + int_suff,
            blacs_lib + int_suff,
        ]
        sca_libs = find_libraries(
            scalapack_libnames,
            root=self.component_lib_dir,
            shared=self._want_shared)
        debug_print(sca_libs)

        if len(sca_libs) < 2:
            raise_lib_error(
                'Cannot locate ScaLapack/BLACS libraries:', scalapack_libnames)

        return sca_libs

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # BTW: The name and meaning of the 'root=' keyword arg of
        # find_libraries() entices us to feed it an "mkl_root" variable, but
        # that is a siren song that pulls us down and under from the true
        # MKLROOT. Hence, such a variable name is not used here [anymore].
        spack_env.set('MKLROOT', self.component_dir)
        spack_env.append_path('SPACK_COMPILER_EXTRA_RPATHS',
                              self.component_lib_dir)

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
        f = join_path(self.component_bin_dir, 'mklvars.sh')
        if not os.path.isfile(f):
            return

        if sys.platform == 'darwin':
            run_env.extend(
                EnvironmentModifications.from_sourcing_file(f))
        else:
            run_env.extend(
                EnvironmentModifications.from_sourcing_file(f, 'intel64'))
