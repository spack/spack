# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import subprocess


class Nekrs(Package):
    """nekRS is an open-source Navier Stokes solver based on the spectral
       element method targeting classical processors and hardware accelerators
       like GPUs"""

    homepage = "https://github.com/Nek5000/nekRS.git"
    git      = "https://github.com/Nek5000/nekRS.git"

    tags = ['cfd', 'flow', 'hpc', 'solver', 'navier-stokes',
            'spectral-elements', 'fluid', 'ecp', 'ecp-apps']

    maintainers = ['thilinarmtb', 'stgeke']

    # TODO: Make sure that we only use gcc

    version('develop', branch='master')

    variant('cuda',
            default=False,
            description='Activates support for CUDA')
    variant('opencl',
            default=False,
            description='Activates support for OpenCL')
    variant('hip',
            default=False,
            description='Activates support for HIP')

    # Dependencies
    depends_on('mpi')
    depends_on('git')
    depends_on('cmake')

    depends_on('cuda', when='+cuda')
    depends_on('hip', when='+hip')

    patch('add_fjfortran.patch', when='%fj')

    @run_before('install')
    def fortran_check(self):
        if not self.compiler.f77:
            msg = 'Cannot build NekRS without a Fortran 77 compiler.'
            raise RuntimeError(msg)

    @run_after('install')
    def test_install(self):
        with working_dir(os.path.join('examples', 'ethier')):
            # Update ethier.par to use Serial backend
            f = open('ethier.par', 'r')
            par = f.read()
            f.close()

            par = par.replace('CUDA', 'Serial')

            f = open('ethier.par', 'w')
            f.write(par)
            f.close()

            ethier_cmd = ' '.join(['TRAVIS=true', os.path.join(prefix.bin, 'nrsmpi'),
                                   'ethier 4 1'])

            process = subprocess.Popen(ethier_cmd, stdout=subprocess.PIPE,
                                       cwd=os.getcwd(), shell=True)
            output, error = process.communicate()
            rc = process.returncode

            assert rc == 0, "ethier example failed.\n{}".format(output.decode('ascii'))

    # Following 4 methods are stolen from OCCA since we are using OCCA
    # shipped with nekRS not as a dependency.
    def _setup_runtime_flags(self, s_env):
        spec = self.spec
        s_env.set('OCCA_CXX', self.compiler.cxx)

        cxxflags = spec.compiler_flags['cxxflags']
        if cxxflags:
            # Run-time compiler flags:
            s_env.set('OCCA_CXXFLAGS', ' '.join(cxxflags))

        if '+cuda' in spec:
            cuda_dir = spec['cuda'].prefix
            # Run-time CUDA compiler:
            s_env.set('OCCA_CUDA_COMPILER',
                      join_path(cuda_dir, 'bin', 'nvcc'))

    def setup_build_environment(self, env):
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
            env.set('CXXFLAGS', ' '.join(cxxflags))

        # For the cuda, openmp, and opencl variants, set the environment
        # variable OCCA_{CUDA,OPENMP,OPENCL}_ENABLED only if the variant is
        # disabled. Otherwise, let OCCA autodetect what is available.

        if '+cuda' in spec:
            cuda_dir = spec['cuda'].prefix
            cuda_libs_list = ['libcuda', 'libcudart', 'libOpenCL']
            cuda_libs = find_libraries(cuda_libs_list,
                                       cuda_dir,
                                       shared=True,
                                       recursive=True)
            env.set('OCCA_INCLUDE_PATH', cuda_dir.include)
            env.set('OCCA_LIBRARY_PATH', ':'.join(cuda_libs.directories))
            env.set('OCCA_CUDA_ENABLED', '1')
        else:
            env.set('OCCA_CUDA_ENABLED', '0')

        # Disable hip autodetection for now since it fails on some machines.
        if '+hip' in spec:
            env.set('OCCA_HIP_ENABLED', '1')
        else:
            env.set('OCCA_HIP_ENABLED', '0')

        if '+opencl' in spec:
            env.set('OCCA_OPENCL_ENABLED', '1')
        else:
            env.set('OCCA_OPENCL_ENABLED', '0')

        # Setup run-time environment for testing.
        env.set('OCCA_VERBOSE', '1')
        self._setup_runtime_flags(env)

    def setup_run_environment(self, env):
        # The 'env' is included in the Spack generated module files.
        self._setup_runtime_flags(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Export OCCA_* variables for everyone using this package from within
        # Spack.
        self._setup_runtime_flags(env)

    def install(self, spec, prefix):
        script_dir = 'scripts'
        makenrs_cmd = 'NEKRS_INSTALL_DIR={} NEKRS_CC={} NEKRS_CXX={} ' + \
            'NEKRS_FC={} ./makenrs'

        cc  = spec['mpi'].mpicc
        fc  = spec['mpi'].mpifc
        cxx = spec['mpi'].mpicxx

        fflags = spec.compiler_flags['fflags']
        cflags = spec.compiler_flags['cflags']
        cxxflags = spec.compiler_flags['cxxflags']

        if self.compiler.name in ['xl', 'xl_r']:
            # Use '-qextname' to add underscores.
            # Use '-WF,-qnotrigraph' to fix an error about a string: '... ??'
            fflags += ['-qextname', '-WF,-qnotrigraph']

        error = Executable(fc)('empty.f', output=str, error=str,
                               fail_on_error=False)

        if 'gfortran' in error or 'GNU' in error or 'gfortran' in fc:
            # Use '-std=legacy' to suppress an error that used to be a
            # warning in previous versions of gfortran.
            fflags += ['-std=legacy']

        fflags = ' '.join(fflags)
        cflags = ' '.join(cflags)
        cxxflags = ' '.join(cxxflags)

        with working_dir(script_dir):
            # Make sure nekmpi wrapper uses srun when we know OpenMPI
            # is not built with mpiexec
            if '^openmpi~legacylaunchers' in spec:
                filter_file(r'mpirun -np', 'srun -n', 'nrsmpi')
                filter_file(r'mpirun -np', 'srun -n', 'nrspre')
                filter_file(r'mpirun -np', 'srun -n', 'nrsbmpi')

        makenrs_cmd = makenrs_cmd.format(prefix, cc, cxx, fc)

        process = subprocess.Popen(makenrs_cmd, stdout=subprocess.PIPE,
                                   cwd=os.getcwd(), shell=True)
        output, error = process.communicate()
        rc = process.returncode

        assert rc == 0, "nekRS installation failed.\n{}".format(output.decode('ascii'))
