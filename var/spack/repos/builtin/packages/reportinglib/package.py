##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
import os


class Reportinglib(CMakePackage):

    """Soma and full compartment report library developed
       by Blue Brain Project, EPFL"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/reportinglib"
    url      = "git@bbpgitlab.epfl.ch:hpc/reportinglib.git"
    git      = "git@bbpgitlab.epfl.ch:hpc/reportinglib.git"

    version('develop', branch='master')
    version('2.5.6', tag='2.5.6')
    version('2.5.5', tag='2.5.5')
    version('2.5.4', tag='2.5.4')
    version('2.5.3', tag='2.5.3')
    version('2.5.2', tag='2.5.2')
    version('2.5.1', tag='2.5.1')
    version('2.5.0', tag='2.5.0')

    variant('profile', default=False, description="Enable profiling using Tau")
    variant('shared', default=True, description="Build shared library")
    variant('tests', default=False, description="Build unit tests")

    depends_on('cmake@2.8.12:', type='build')
    depends_on('boost', when='+tests')
    depends_on('mpi')
    depends_on('tau', when='+profile')

    @run_before('build')
    def profiling_wrapper_on(self):
        os.environ["USE_PROFILER_WRAPPER"] = "1"

    @run_after('install')
    def profiling_wrapper_off(self):
        del os.environ["USE_PROFILER_WRAPPER"]

    def cmake_args(self):
        spec   = self.spec
        options = []

        if spec.satisfies('+profile'):
            env['CC']  = 'tau_cc'
            env['CXX'] = 'tau_cxx'
        elif 'bgq' in self.spec.architecture:
            env['CC']  = spec['mpi'].mpicc
            env['CXX'] = spec['mpi'].mpicxx

        if spec.satisfies('~shared'):
            options.append('-DCOMPILE_LIBRARY_TYPE=STATIC')

        if spec.satisfies('~tests'):
            options.append('-DUNIT_TESTS=OFF')

        return options

    @property
    def libs(self):
        """Export the reportinglib library.
        Sample usage: spec['reportinglib'].libs.ld_flags
        """
        search_paths = [[self.prefix.lib64, False], [self.prefix.lib, False]]
        is_shared = '+shared' in self.spec
        for path, recursive in search_paths:
            libs = find_libraries('libreportinglib', root=path,
                                  shared=is_shared, recursive=False)
            if libs:
                return libs
        return None
