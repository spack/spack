##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
import os


class Coreneuron(CMakePackage):

    """CoreNEURON is a simplified engine for the NEURON simulator
    optimised for both memory usage and computational speed. Its goal
    is to simulate massive cell networks with minimal memory footprint
    and optimal performance."""

    homepage = "https://github.com/BlueBrain/CoreNeuron"
    url      = "https://github.com/BlueBrain/CoreNeuron"
    git      = "https://github.com/BlueBrain/CoreNeuron"

    version('develop', branch='master', submodules=True)
    version('0.21a', commit="bf3c823", preferred=True)
    version('0.20', tag='0.20', submodules=True)
    version('0.19', tag='0.19', submodules=True)
    version('0.18', tag='0.18', submodules=True)
    version('0.17', tag='0.17', submodules=True)
    version('0.16', tag='0.16', submodules=True)
    version('0.15', tag='0.15', submodules=True)
    version('0.14', tag='0.14', submodules=True)
    patch('0001-Fixes-for-NMODL-MOD2C-binary.patch', when='@0.17+nmodl')

    variant('debug', default=False, description='Build debug with O0')
    variant('gpu', default=False, description="Enable GPU build")
    variant('knl', default=False, description="Enable KNL specific flags")
    variant('mpi', default=True, description="Enable MPI support")
    variant('openmp', default=False, description="Enable OpenMP support")
    variant('profile', default=False, description="Enable profiling using Tau")
    variant('report', default=True, description="Enable SONATA and binary reports")
    variant('shared', default=True, description="Build shared library")
    variant('tests', default=False, description="Enable building tests")

    # nmodl specific options
    variant('nmodl', default=False, description="Use NMODL instead of MOD2C")
    variant('sympy', default=False, description="Use NMODL with SymPy to solve ODEs")
    variant('sympyopt', default=False, description="Use NMODL with SymPy Optimizations")
    variant('ispc', default=False, description="Enable ISPC backend")

    depends_on('bison', type='build')
    depends_on('cmake@3:', type='build')
    depends_on('flex', type='build')

    depends_on('boost', when='+tests')
    depends_on('cuda', when='+gpu')
    depends_on('flex', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('reportinglib', when='+report')
    depends_on('libsonata-report', when='+report')
    depends_on('reportinglib+profile', when='+report+profile')
    depends_on('tau', when='+profile')

    # nmodl specific dependency
    depends_on('nmodl@0.3b:', when='@0.17:+nmodl')
    depends_on('nmodl@0.3a', when='@0:0.16+nmodl')
    depends_on('eigen@3.3.4:~metis~scotch~fftw~suitesparse~mpfr', when='+nmodl')
    depends_on('ispc', when='+ispc')

    # Old versions. Required by previous neurodamus package.
    version('master',      git=url, submodules=True)
    version('mousify',     git=url, submodules=True)
    version('hippocampus', git=url, submodules=True)
    version('plasticity',  git=url, submodules=True)
    depends_on('neurodamus-base@master', when='@master')
    depends_on('neurodamus-base@mousify', when='@mousify')
    depends_on('neurodamus-base@plasticity', when='@plasticity')
    depends_on('neurodamus-base@hippocampus', when='@hippocampus')

    # sympy and ispc options are only usable with nmodl
    conflicts('+sympyopt', when='~sympy')
    conflicts('+sympy', when='~nmodl')
    conflicts('+sympy', when='coreneuron@0.17')  # issue with include directories
    conflicts('+ispc', when='~nmodl')

    # raise conflict when trying to install '+gpu' without PGI compiler
    gpu_compiler_message = "For gpu build use %pgi"
    conflicts('%gcc', when='+gpu', msg=gpu_compiler_message)
    conflicts('%intel', when='+gpu', msg=gpu_compiler_message)

    @run_before('build')
    def profiling_wrapper_on(self):
        os.environ["USE_PROFILER_WRAPPER"] = "1"
        tau_file = self.stage.source_path + "/extra/instrumentation.tau"
        tau_opts = "-optPDTInst -optNoCompInst -optRevert -optVerbose"
        tau_opts += " -optTauSelectFile=%s" % tau_file
        os.environ["TAU_OPTIONS"] = tau_opts

    @run_after('install')
    def profiling_wrapper_off(self):
        del os.environ["USE_PROFILER_WRAPPER"]
        del os.environ["TAU_OPTIONS"]

    def get_flags(self):
        spec = self.spec
        flags = "-g -O2"
        if '%intel' in spec:
            flags = '-g -xHost -O2 -qopt-report=5'
            if '+knl' in spec:
                flags = '-g -xMIC-AVX512 -O2 -qopt-report=5'
        if '+gpu' in spec:
            flags = '-O2'
            flags += ' -Minline=size:1000,levels:100,'
            flags += 'totalsize:40000,maxsize:4000'
            flags += ' -ta=tesla:cuda%s' % (spec['cuda'].version.up_to(2))
        if '+debug' in spec:
            flags = '-g -O0'
        # when pdt is used for instrumentation, the gcc's unint128 extension
        # is activated from random123 which results in compilation error
        if '+profile' in spec:
            flags += ' -DTAU -DR123_USE_GNU_UINT128=0'
        return flags

    def get_cmake_args(self):
        spec   = self.spec
        flags = self.get_flags()

        if spec.satisfies('+profile'):
            env['CC']  = 'tau_cc'
            env['CXX'] = 'tau_cxx'

        if '@0.17:0.18' in spec:
            enable_reporting = '-DCORENRN_ENABLE_REPORTINGLIB=%s'
        else:
            enable_reporting = '-DCORENRN_ENABLE_REPORTING=%s'

        options =\
            ['-DCORENRN_ENABLE_SPLAYTREE_QUEUING=ON',
             '-DCMAKE_C_FLAGS=%s' % flags,
             '-DCMAKE_CXX_FLAGS=%s' % flags,
             '-DCMAKE_BUILD_TYPE=CUSTOM',
             enable_reporting % ('ON' if '+report' in spec else 'OFF'),
             '-DCORENRN_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
             '-DCORENRN_ENABLE_OPENMP=%s'
             % ('ON' if '+openmp' in spec else 'OFF'),
             '-DCORENRN_ENABLE_UNIT_TESTS=%s'
             % ('ON' if '+tests' in spec else 'OFF'),
             '-DCORENRN_ENABLE_TIMEOUT=OFF'
             ]

        if spec.satisfies('+nmodl'):
            options.append('-DCORENRN_ENABLE_NMODL=ON')
            options.append('-DCORENRN_NMODL_DIR=%s' % spec['nmodl'].prefix)
            flags += ' -I%s -I%s' % (spec['nmodl'].prefix.include,
                                     spec['eigen'].prefix.include.eigen3)

        nmodl_options = 'codegen --force'

        if spec.satisfies('+ispc'):
            options.append('-DCORENRN_ENABLE_ISPC=ON')
            if '+knl' in spec:
                options.append('-DCMAKE_ISPC_FLAGS=-O2 -g --pic '
                               '--target=avx512knl-i32x16')
            else:
                options.append('-DCMAKE_ISPC_FLAGS=-O2 -g --pic '
                               '--target=host')

        if spec.satisfies('+sympy'):
            nmodl_options += ' sympy --analytic'

        if spec.satisfies('+sympyopt'):
            nmodl_options += ' --conductance --pade --cse'

        options.append('-DCORENRN_NMODL_FLAGS=%s' % nmodl_options)

        if spec.satisfies('~shared') or spec.satisfies('+gpu'):
            options.append('-DCOMPILE_LIBRARY_TYPE=STATIC')

        if spec.satisfies('+gpu'):
            gcc = which("gcc")
            options.extend(['-DCUDA_HOST_COMPILER=%s' % gcc,
                            '-DCUDA_PROPAGATE_HOST_FLAGS=OFF',
                            '-DCORENRN_ENABLE_GPU=ON'])
            # PGI compiler not able to compile nrnreport.cpp when enabled
            # OpenMP, OpenACC and Reporting. Disable ReportingLib for GPU
            options.append('-DCORENRN_ENABLE_REPORTING=OFF')

        return options

    @when('@0:0.16')
    def get_cmake_args(self):
        spec   = self.spec
        flags = self.get_flags()

        options =\
            ['-DENABLE_SPLAYTREE_QUEUING=ON',
             '-DCMAKE_BUILD_TYPE=CUSTOM',
             '-DENABLE_REPORTINGLIB=%s'
                % ('ON' if '+report' in spec else 'OFF'),
             '-DENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
             '-DCORENEURON_OPENMP=%s' % ('ON' if '+openmp' in spec else 'OFF'),
             '-DUNIT_TESTS=%s' % ('ON' if '+tests' in spec else 'OFF'),
             '-DFUNCTIONAL_TESTS=%s' % ('ON' if '+tests' in spec else 'OFF'),
             '-DENABLE_HEADER_INSTALL=ON',  # for corenrn-special
             '-DDISABLE_NRN_TIMEOUT=ON'
             ]

        if spec.satisfies('+profile'):
            env['CC']  = 'tau_cc'
            env['CXX'] = 'tau_cxx'

        if spec.satisfies('+nmodl'):
            options.append('-DENABLE_NMODL=ON')
            options.append('-DNMODL_ROOT=%s' % spec['nmodl'].prefix)
            flags += ' -I%s -I%s' % (spec['nmodl'].prefix.include,
                                     spec['eigen'].prefix.include.eigen3)

        nmodl_options = 'codegen --force passes --verbatim-rename --inline'

        if spec.satisfies('+ispc'):
            options.append('-DENABLE_ISPC_TARGET=ON')
            if '+knl' in spec:
                options.append('-DCMAKE_ISPC_FLAGS=-O2 -g --pic '
                               '--target=avx512knl-i32x16')
            else:
                options.append('-DCMAKE_ISPC_FLAGS=-O2 -g --pic '
                               '--target=host')

        if spec.satisfies('+sympy'):
            nmodl_options += ' sympy --analytic'

        if spec.satisfies('+sympyopt'):
            nmodl_options += ' --conductance --pade --cse'

        options.append('-DNMODL_EXTRA_FLAGS=%s' % nmodl_options)

        options.extend(['-DCMAKE_C_FLAGS=%s' % flags,
                        '-DCMAKE_CXX_FLAGS=%s' % flags])

        if spec.satisfies('~shared') or spec.satisfies('+gpu')\
           or 'cray' in spec.architecture:
            options.append('-DCOMPILE_LIBRARY_TYPE=STATIC')

        if spec.satisfies('+gpu'):
            gcc = which("gcc")
            options.extend(['-DCUDA_HOST_COMPILER=%s' % gcc,
                            '-DCUDA_PROPAGATE_HOST_FLAGS=OFF',
                            '-DENABLE_SELECTIVE_GPU_PROFILING=ON',
                            '-DENABLE_OPENACC=ON',
                            '-DENABLE_OPENACC_INFO=ON'])
            # PGI compiler not able to compile nrnreport.cpp when enabled
            # OpenMP, OpenACC and Reporting. Disable ReportingLib for GPU
            options.append('-DENABLE_REPORTINGLIB=OFF')

        # Suppport for previous neurodamus package
        if '^neurodamus-base' in spec:
            modlib_dir = self.spec['neurodamus-base'].prefix.lib.modlib
            modfile_list = '%s/coreneuron_modlist.txt' % modlib_dir
            options.append('-DADDITIONAL_MECHS=%s' % modfile_list)
            options.append('-DADDITIONAL_MECHPATH=%s' % modlib_dir)

        return options

    def cmake_args(self):
        return self.get_cmake_args()

    @run_after('install')
    def filter_compilers(self):
        """run after install to avoid spack compiler wrappers
        getting embded into nrnivmodl script"""

        nrnmakefile = join_path(self.prefix,
                                'share/coreneuron/nrnivmodl_core_makefile')

        kwargs = {
            'backup': False,
            'string': True
        }

        filter_file(env['CC'],  self.compiler.cc, nrnmakefile, **kwargs)
        filter_file(env['CXX'], self.compiler.cxx, nrnmakefile, **kwargs)

    @property
    def libs(self):
        """Export the coreneuron library.
        Sample usage: spec['coreneuron'].libs.ld_flags
        """
        search_paths = [[self.prefix.lib, False], [self.prefix.lib64, False]]
        spec = self.spec
        # opposite of how static linkage is used
        is_shared = not (spec.satisfies('~shared') or spec.satisfies('+gpu')
                         or 'cray' in spec.architecture)
        for path, recursive in search_paths:
            libs = find_libraries(['libcoreneuron', 'libcorenrnmech'],
                                  root=path, shared=is_shared, recursive=False)
            if libs:
                return libs
        return None
