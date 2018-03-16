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
import shutil


class Occa(Package):
    """OCCA is an open-source (MIT license) library used to program current
       multi-core/many-core architectures. Devices (such as CPUs, GPUs,
       Intel's Xeon Phi, FPGAs, etc) are abstracted using an offload-model
       for application development and programming for the devices is done
       through a C-based (OKL) or Fortran-based kernel language (OFL).
       OCCA gives developers the ability to target devices at run-time by
       using run-time compilation for device kernels.
    """

    homepage = "http://libocca.org"

    version('develop', git='https://github.com/libocca/occa.git')
    # FIXME: Replace this version with tagged version?
    version('48cf18a', git='https://github.com/libocca/occa.git',
            commit='48cf18af79da6463074b8757b923f7ad1e6a5174')
    version('0.2', git='https://github.com/libocca/occa.git', tag='0.2')
    version('0.1', git='https://github.com/libocca/occa.git', tag='0.1')
    version('0.0.0', git='https://github.com/libocca/occa.git',
            commmit='381e886886dc87823769c5f20d0ecb29dd117afa')

    variant('cuda',   default=True,
            description='Activates support for CUDA')
    variant('openmp',   default=True,
            description='Activates support for OpenMP')
    variant('opencl',   default=True,
            description='Activates support for OpenCL')
    variant('coi',   default=False,
            description='Activates support for COI')
    variant('debug', default=False, description='Enable debug build')

    depends_on('cuda', when='+cuda')

    def install(self, spec, prefix):
        # The build environment is set by the 'setup_environment' method.

        # Copy the source to the installation directory and build OCCA there.
        for file in os.listdir('.'):
            dest = join_path(prefix, os.path.basename(file))
            if os.path.isdir(file):
                shutil.copytree(file, dest)
            else:
                shutil.copy2(file, dest)
        make('-C', prefix, 'CC=%s' % env['CC'])

        if self.run_tests:
            make('-C', prefix, 'test', 'CC=%s' % env['CC'], parallel=False)

    def _setup_rt_env(self, s_env):
        spec = self.spec
        s_env.set('OCCA_DIR', self.prefix)
        # Run-time compiler:
        s_env.set('OCCA_CXX', self.compiler.cxx)
        cxxflags = spec.compiler_flags['cxxflags']
        if cxxflags:
            # Run-time compiler flags:
            s_env.set('OCCA_CXXFLAGS', ' '.join(cxxflags))
        if '+cuda' in spec:
            # Run-time CUDA compiler:
            s_env.set('OCCA_CUDA_COMPILER',
                      join_path(cuda_path, 'bin', 'nvcc'))
            # Set OCCA_CUDA_COMPILER_FLAGS?
        # TODO: export other OCCA_* variables.

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        # The environment variable CXX is automatically set to the Spack
        # compiler wrapper.

        # The cxxflags, if specified, will be set by the Spack compiler wrapper
        # while the environment variable CXXFLAGS will remain undefined.
        # We define CXXFLAGS in the environment to tell OCCA to use the user
        # specified flags instead of its defaults. This way the compiler will
        # get the cxxflags twice - once from the Spack compiler wrapper and
        # second time from OCCA - however, only the second one will be seen in
        # the verbose output, so we keep both.
        cxxflags = spec.compiler_flags['cxxflags']
        if cxxflags:
            spack_env.set('CXXFLAGS', ' '.join(cxxflags))

        # For the cuda, openmp, and opencl variants, set the environment
        # variable OCCA_{CUDA,OPENMP,OPENCL}_ENABLED only if the variant is
        # disabled. Otherwise, let OCCA autodetect what is available.

        if '+cuda' in spec:
            cuda_dir = spec['cuda'].prefix
            spack_env.set('OCCA_INCLUDE_PATH', cuda_dir.include)
            spack_env.set('OCCA_LIBRARY_PATH',
                          join_path(cuda_dir, 'lib*') + ':' +
                          join_path(cuda_dir, 'lib*/stubs'))
        else:
            spack_env.set('OCCA_CUDA_ENABLED', '0')

        if '~openmp' in spec:
            spack_env.set('OCCA_OPENMP_ENABLED', '0')
        # If +openmp, how can we tell OCCA what the OpenMP flag is?
        # We can get the flag from Spack as: self.compiler.openmp_flag.

        if '~opencl' in spec:
            spack_env.set('OCCA_OPENCL_ENABLED', '0')
        # If +opencl, set OCCA_OPENCL_COMPILER_FLAGS?

        # TODO: coi variant?

        if '+debug' in spec:
            spack_env.set('OCCA_DEVELOPER', '1')
            spack_env.set('DEBUG', '1')

        # Setup run-time environment for testing.
        spack_env.set('OCCA_VERBOSE', '1')
        self._setup_rt_env(spack_env)
        # The 'run_env' is included in the Spack generated module files.
        self._setup_rt_env(run_env)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Export OCCA_* variables for everyone using this package from within
        # Spack.
        self._setup_rt_env(spack_env)
