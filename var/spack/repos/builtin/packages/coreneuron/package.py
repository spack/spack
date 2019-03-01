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
import os


class Coreneuron(CMakePackage):

    """CoreNEURON is a simplified engine for the NEURON simulator
    optimised for both memory usage and computational speed. Its goal
    is to simulate massive cell networks with minimal memory footprint
    and optimal performance."""

    homepage = "https://github.com/BlueBrain/CoreNeuron"
    url      = "https://github.com/BlueBrain/CoreNeuron"

    version('develop', git=url, submodules=True)
    version('0.14', git=url, submodules=True, preferred=True)

    variant('debug', default=False, description='Build debug with O0')
    variant('gpu', default=False, description="Enable GPU build")
    variant('knl', default=False, description="Enable KNL specific flags")
    variant('mpi', default=True, description="Enable MPI support")
    variant('openmp', default=False, description="Enable OpenMP support")
    variant('profile', default=False, description="Enable profiling using Tau")
    variant('report', default=True, description="Enable reports using ReportingLib")
    variant('shared', default=True, description="Build shared library")
    variant('tests', default=False, description="Enable building tests")

    depends_on('boost', when='+tests')
    depends_on('cmake@3:', type='build')
    depends_on('cuda', when='+gpu')
    depends_on('mpi', when='+mpi')
    depends_on('reportinglib', when='+report')
    depends_on('reportinglib+profile', when='+report+profile')
    depends_on('tau', when='+profile')

    # Old versions. Required by previous neurodamus package.
    version('master',      git=url, submodules=True)
    version('hippocampus', git=url, submodules=True)
    version('plasticity',  git=url, submodules=True)
    depends_on('neurodamus-base@master', when='@master')
    depends_on('neurodamus-base@plasticity', when='@plasticity')
    depends_on('neurodamus-base@hippocampus', when='@hippocampus')

    @run_before('build')
    def profiling_wrapper_on(self):
        os.environ["USE_PROFILER_WRAPPER"] = "1"
        tau_file = self.stage.source_path + "/extra/instrumentation.tau"
        tau_opts = "-optPDTInst -optNoCompInst -optRevert -optVerbose"
        tau_opts += " -optTauSelectFile=%s" % tau_file
        os.environ["TAU_OPTIONS"] = tau_opts

    @run_after ('install')
    def profiling_wrapper_off(self):
        del os.environ["USE_PROFILER_WRAPPER"]
        del os.environ["TAU_OPTIONS"]

    def get_flags(self):
        spec = self.spec
        flags = "-g -O2"
        if 'bgq' in spec.architecture and '%xl' in spec:
            flags = '-O3 -qtune=qp -qarch=qp -q64 -qhot=simd -qsmp -qthreaded -g'
        if '%intel' in spec:
            flags = '-g -xHost -O2 -qopt-report=5'
            if '+knl' in spec:
                flags = '-g -xMIC-AVX512 -O2 -qopt-report=5'
        if '+gpu' in spec:
            flags = '-O2 -Minline=size:1000,levels:100,totalsize:40000,maxsize:4000'
            flags += ' -ta=tesla:cuda%s' % (spec['cuda'].version.up_to(2))
        if '+debug' in spec:
            flags = '-g -O0'
        # when pdt is used for instrumentation, the gcc's unint128 extension
        # is activated from random123 which results in compilation error
        if '+profile' in spec:
            flags += ' -DTAU -DR123_USE_GNU_UINT128=0'
        return flags

    def cmake_args(self):
        spec   = self.spec
        flags = self.get_flags()

        if spec.satisfies('+profile'):
            env['CC']  = 'tau_cc'
            env['CXX'] = 'tau_cxx'
        elif 'bgq' in spec.architecture and spec.satisfies('+mpi'):
            env['CC']  = spec['mpi'].mpicc
            env['CXX'] = spec['mpi'].mpicxx

        options = ['-DENABLE_SPLAYTREE_QUEUING=ON',
                   '-DCMAKE_C_FLAGS=%s' % flags,
                   '-DCMAKE_CXX_FLAGS=%s' % flags,
                   '-DCMAKE_BUILD_TYPE=CUSTOM',
                   '-DENABLE_REPORTINGLIB=%s' % ('ON' if '+report' in spec else 'OFF'),
                   '-DENABLE_MPI=%s' % ('ON' if '+mpi' in spec else 'OFF'),
                   '-DCORENEURON_OPENMP=%s' % ('ON' if '+openmp' in spec else 'OFF'),
                   '-DUNIT_TESTS=%s' % ('ON' if '+tests' in spec else 'OFF'),
                   '-DFUNCTIONAL_TESTS=%s' % ('ON' if '+tests' in spec else 'OFF'),
                   '-DENABLE_HEADER_INSTALL=ON'  # for compiling mods to corenrn-special
                   ]

        if spec.satisfies('~shared') or spec.satisfies('+gpu'):
            options.append('-DCOMPILE_LIBRARY_TYPE=STATIC')

        if 'bgq' in spec.architecture and '%xl' in spec:
            options.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')

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

    @property
    def libs(self):
        """Export the coreneuron library.
        Sample usage: spec['coreneuron'].libs.ld_flags
        """
        search_paths = [[self.prefix.lib, False], [self.prefix.lib64, False]]
        spec = self.spec
        is_shared = spec.satisfies('+shared') and spec.satisfies('~gpu')
        for path, recursive in search_paths:
            libs = find_libraries(['libcoreneuron', 'libcorenrnmech'], root=path,
                                  shared=is_shared, recursive=False)
            if libs:
                return libs
        return None
