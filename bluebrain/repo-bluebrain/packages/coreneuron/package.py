##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack import *


class Coreneuron(CMakePackage):

    """CoreNEURON is a simplified engine for the NEURON simulator
    optimised for both memory usage and computational speed. Its goal
    is to simulate massive cell networks with minimal memory footprint
    and optimal performance."""

    homepage = "https://github.com/BlueBrain/CoreNeuron"
    url      = "https://github.com/BlueBrain/CoreNeuron"
    # This simplifies testing the gitlab-pipelines repository:
    git      = "git@bbpgitlab.epfl.ch:hpc/coreneuron.git"

    version('develop', branch='master')
    # 1.0.1 > 1.0.0.20210519 > 1.0 as far as Spack is concerned
    version('1.0.0.20220304', commit='2d08705')
    version('1.0.0.20220218', commit='102ebde')
    version('1.0.0.20220111', commit='64e56b7')
    version('1.0.0.20211020', commit='e265f9d')
    version('1.0.0.20211012', commit='846b3a6')
    version('1.0.0.20210708', commit='d54a3aa')
    version('1.0.0.20210610', commit='b4a25b4')
    version('1.0.0.20210525', commit='711d2b8')
    version('1.0.0.20210519', commit='c938e4f')
    version('1.0', tag='1.0')
    version('0.22', tag='0.22', submodules=True)

    variant('gpu', default=False, description="Enable GPU build")
    variant('unified', default=False, description="Enable Unified Memory with GPU build")
    variant('knl', default=False, description="Enable KNL specific flags")
    variant('mpi', default=True, description="Enable MPI support")
    variant('openmp', default=False, description="Enable OpenMP support")
    variant('profile', default=False, description="Enable profiling using Tau")
    variant('caliper', default=False, description="Enable Caliper instrumentation")
    variant('report', default=True, description="Enable SONATA and binary reports")
    variant('shared', default=True, description="Build shared library")
    variant('tests', default=False, description="Enable building tests")

    # nmodl specific options
    variant('nmodl', default=False, description="Use NMODL instead of MOD2C")
    variant('codegenopt', default=False, description="Use NMODL with codedgen ionvar copies optimizations")
    variant('sympy', default=False, description="Use NMODL with SymPy to solve ODEs")
    variant('sympyopt', default=False, description="Use NMODL with SymPy Optimizations")
    variant('ispc', default=False, description="Enable ISPC backend")
    variant("legacy-unit", default=True, description="Enable legacy units")

    # Build with `ninja` instead of `make`
    generator = 'Ninja'
    depends_on('ninja', type='build')

    depends_on('bison', type='build')
    depends_on('cmake@3:', type='build')
    depends_on('flex', type='build')
    # Some of the generated Makefile infrastucture uses Python!
    depends_on('python', type=('build', 'run'))

    depends_on('boost', when='+tests')
    depends_on('cuda', when='+gpu')
    depends_on('flex', type='build', when='~nmodl')
    depends_on('flex@2.6:', type='build', when='+nmodl')
    depends_on('mpi', when='+mpi')
    depends_on('reportinglib', when='+report')
    depends_on('libsonata-report@1.0.0.20210610:', when='@1.0.0.20210610:+report')
    depends_on('libsonata-report@1.0:1.0.0.20210531', when='@1.0.0.20210519:1.0.0.20210525+report')
    depends_on('libsonata-report@:0.1', when='@:1.0.0.20210518+report')
    depends_on('reportinglib+profile', when='+report+profile')
    depends_on('tau', when='+profile')
    depends_on('caliper+mpi', when='@1.0.0.20210519:+caliper+mpi')
    depends_on('caliper~mpi', when='@1.0.0.20210519:+caliper~mpi')

    # nmodl specific dependency
    depends_on('nmodl@0.3.0:', when='@1.0:+nmodl')
    depends_on('nmodl@0.3b', when='@:0.22+nmodl')
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

    # sympy, codegen and ispc options are only usable with nmodl
    conflicts('+sympyopt', when='~sympy')
    conflicts('+sympy', when='~nmodl')
    conflicts('+codegenopt', when='~nmodl')
    conflicts('+ispc', when='~nmodl')

    # Cannot enabled Unified Memory without GPU build
    conflicts('+unified', when='~gpu')

    # Caliper instrumentation is only supported after 1.0.0.20210519
    # Note: The 20210518 date is needed to specify a version before 20210519!
    conflicts('+caliper', when='@:1.0.0.20210518')

    # An old comment said "PGI compiler not able to compile nrnreport.cpp when
    # enabled OpenMP, OpenACC and Reporting. Disable ReportingLib for GPU", but
    # with the contemporary develop version it seems to work. Encode this
    # knowledge as a conflict between +report and +gpu for older versions.
    conflicts('+report', when='coreneuron@:0.22+gpu+openmp')

    # raise conflict when trying to install '+gpu' without PGI compiler
    gpu_compiler_message = "For gpu build use %pgi or %nvhpc"
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
        flags = []
        if '%intel' in spec:
            flags.append('-qopt-report=5')
            if '+knl' in spec:
                flags.append('-xMIC-AVX512')
            else:
                flags.append('-xHost')
        else:
            # For other complers, pass Spack's target architecture flags in
            # explicitly so that they are saved to nrnivmodl_core_makefile
            flags.append(spec.architecture.target.optimization_flags(spec.compiler))
        # NVHPC 21.11 and newer detect ABM support and define __ABM__, which
        # breaks Random123 compilation. CoreNEURON inserts a workaround for
        # this in https://github.com/BlueBrain/CoreNeuron/pull/754.
        if self.spec.satisfies('@:1.0.0.20220111%nvhpc@21.11:'):
            flags.append('-DR123_USE_INTRIN_H=0')
        # when pdt is used for instrumentation, the gcc's unint128 extension
        # is activated from random123 which results in compilation error
        if '+profile' in spec:
            flags += ['-DTAU', '-DR123_USE_GNU_UINT128=0']
        return ' '.join(flags)

    def get_cmake_args(self):
        spec   = self.spec
        flags = self.get_flags()

        if spec.satisfies('+profile'):
            env['CC']  = 'tau_cc'
            env['CXX'] = 'tau_cxx'

        options =\
            ['-DCORENRN_ENABLE_SPLAYTREE_QUEUING=ON',
             '-DCMAKE_CXX_FLAGS=%s' % flags,
             '-DCORENRN_ENABLE_REPORTING=%s'
             % ('ON' if '+report' in spec else 'OFF'),
             '-DCORENRN_ENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
             '-DCORENRN_ENABLE_OPENMP=%s'
             % ('ON' if '+openmp' in spec else 'OFF'),
             '-DCORENRN_ENABLE_UNIT_TESTS=%s'
             % ('ON' if '+tests' in spec else 'OFF'),
             '-DCORENRN_ENABLE_TIMEOUT=OFF',
             '-DPYTHON_EXECUTABLE=%s' % spec["python"].command.path
             ]

        # Versions after this only used C++, but we might still need C
        # flags if mod2c is being built as a submodule.
        if spec.satisfies('@:1.0.0.20210708') or spec.satisfies('~nmodl'):
            options.append('-DCMAKE_C_FLAGS=%s' % flags)

        if spec.satisfies('+caliper'):
            options.append('-DCORENRN_ENABLE_CALIPER_PROFILING=ON')

        if "+legacy-unit" in self.spec:
            options.append('-DCORENRN_ENABLE_LEGACY_UNITS=ON')

        if spec.satisfies('+nmodl'):
            options.append('-DCORENRN_ENABLE_NMODL=ON')
            options.append('-DCORENRN_NMODL_DIR=%s' % spec['nmodl'].prefix)

        nmodl_options = 'codegen --force'

        if spec.satisfies('+codegenopt'):
            nmodl_options += ' --opt-ionvar-copy=TRUE'

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
            if spec.satisfies('@1.0.0.20210709:'):
                # After https://github.com/BlueBrain/CoreNeuron/pull/609
                nvcc = which("nvcc")
                options.extend(['-DCMAKE_CUDA_COMPILER=%s' % nvcc,
                                '-DCMAKE_CUDA_HOST_COMPILER=%s' % gcc])
            else:
                options.extend(['-DCUDA_HOST_COMPILER=%s' % gcc,
                                '-DCUDA_PROPAGATE_HOST_FLAGS=OFF'])
            if spec.satisfies('+unified'):
                options.append('-DCORENRN_ENABLE_CUDA_UNIFIED_MEMORY=ON')
            options.append('-DCORENRN_ENABLE_GPU=ON')

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
