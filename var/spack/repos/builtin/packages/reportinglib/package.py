##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Reportinglib(CMakePackage):

    """Soma and full compartment report library developed by Blue Brain Project, EPFL"""

    homepage = "https://bbpcode.epfl.ch/code/a/sim/reportinglib/bbp"
    url      = "ssh://bbpcode.epfl.ch/sim/reportinglib/bbp"

    version('develop', git=url, tag='2.5.0', preferred=True)

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

    @run_after ('install')
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
        search_paths = [[self.prefix.lib, False], [self.prefix.lib64, False]]
        is_shared = '+shared' in self.spec
        for path, recursive in search_paths:
            libs = find_libraries('libreportinglib', root=path,
                                  shared=is_shared, recursive=False)
            if libs:
                return libs
        return None

    def setup_environment(self, spack_env, run_env):
        spack_env.unset('LC_ALL')
