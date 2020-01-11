# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LlvmFlang(CMakePackage):
    """LLVM-Flang is the Flang fork of LLVM needed by the Flang package."""

    homepage = "https://github.com/flang-compiler"

    git      = "https://github.com/flang-compiler/llvm.git"

    maintainer = ['naromero77']

    version('master', branch='master')
    version('release_70', branch='release_70')
    version('release_60', branch='release_60')
    version('20190329', tag='flang_20190329')
    version('20181226_70', tag='20181226_70')
    version('20181226_60', tag='20181226_60')
    version('20180921', tag='20180921')
    version('20180319', tag='20180319')
    version('20180328', tag='20180308')

    # Variants
    variant('target', default='X86',
            description='Target archiecture',
            values=('X86', 'PowerPC', 'AArch64'))

    # Build dependency
    depends_on('cmake@3.8:', type='build')
    depends_on('python@2.7:', type='build')

    # LLVM-Flang Componentes: Driver, OpenMP
    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             branch='master',
             destination='tools',
             placement='clang',
             when='@master')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             branch='release_70',
             destination='tools',
             placement='clang',
             when='@release_70')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             branch='release_60',
             destination='tools',
             placement='clang',
             when='@release_60')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20190329',
             destination='tools',
             placement='clang',
             when='@20190329')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20181226_70',
             destination='tools',
             placement='clang',
             when='@20181226_70')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20181226_60',
             destination='tools',
             placement='clang',
             when='@20181226_60')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20180921',
             destination='tools',
             placement='clang',
             when='@20180921')

    resource(name='flang-driver',
             git='https://github.com/flang-compiler/flang-driver.git',
             tag='flang_20180921',
             destination='tools',
             placement='clang',
             when='@20180308')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             branch='master',
             destination='projects',
             placement='openmp',
             when='@master')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             branch='release_70',
             destination='projects',
             placement='openmp',
             when='@release_70')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             branch='release_60',
             destination='projects',
             placement='openmp',
             when='@release_60')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             tag='flang_20190329',
             destination='projects',
             placement='openmp',
             when='@20190329')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             tag='flang_20181226_70',
             destination='projects',
             placement='openmp',
             when='@20181226_70')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             tag='flang_20181226_60',
             destination='projects',
             placement='openmp',
             when='@20181226_60')

    resource(name='openmp',
             git='https://github.com/flang-compiler/openmp.git',
             tag='flang_20180921',
             destination='projects',
             placement='openmp',
             when='@20180921')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append('-DPYTHON_EXECUTABLE={0}'.format(
            spec['python'].command.path))
        args.append('-DLLVM_TARGETS_TO_BUILD={0}'.format(
            spec.variants['target'].value))

        return args
