# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pmlib(CMakePackage):
    """This library records the statistics information of run-time performance
       and the trace information of a user code and reports its summary.
       The PMlib is able to use for both serial and parallel environments
       including hybrid(OpenMP & MPI) code. In addition, PAPI interface allows
       us to access the information of build-in hardware counter."""

    homepage = "https://github.com/avr-aics-riken/PMlib"
    git      = "https://github.com/avr-aics-riken/PMlib.git"

    version('master', branch='master')
    version('6.4.1', commit='0a35f5bec8c12e532e5a1bdac8c32c659fd3ee11')

    variant('mpi', default=False, description='Activate MPI support')

    phases = ['edit', 'cmake', 'build', 'install']

    depends_on('mpi', when='+mpi')

    def edit(self, spec, prefix):
        if '%fj' in self.spec:
            toolchain = FileFilter('./cmake/Toolchain_fx100.cmake')
            toolchain.filter('mpifccpx', spec['mpi'].mpicc)
            toolchain.filter('mpiFCCpx', spec['mpi'].mpicxx)
            toolchain.filter('mpifrtpx', spec['mpi'].mpifc)
            toolchain.filter('/opt/FJSVmxlang/GM-2.0.0-05',
                             spec['mpi'].prefix, string=True)
            toolchain.filter('lib64', 'lib')

            selector = FileFilter('./cmake/CompileOptionSelector.cmake')
            selector.filter('-Nrt_notune', '')
            selector.filter('-Xg', '-Nclang')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append('-DINSTALL_DIR={0}'.format(self.prefix))

        if '%gcc' in spec:
            gcc_args = [
                '-DCMAKE_CXX_FLAGS=-fopenmp',
                '-DCMAKE_Fortran_FLAGS=-fopenmp -cpp',
            ]
            args = args + gcc_args

        if '%fj' in spec:
            fj_args = [
                '-DCMAKE_TOOLCHAIN_FILE=./cmake/Toolchain_fx100.cmake',
                '-Denable_OPENMP=no',
                '-Dwith_MPI=yes',
                '-Denable_Fortran=no',
                '-Dwith_example=no',
                '-Dwith_PAPI=no',
                '-Dwith_OTF=no',
                '-Denable_PreciseTimer=yes ..',
            ]
            args = args + fj_args

        return args
