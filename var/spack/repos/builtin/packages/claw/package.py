# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Claw(CMakePackage):
    """CLAW Compiler targets performance portability problem in climate and
       weather application written in Fortran. From a single source code, it
       generates architecture specific code decorated with OpenMP or OpenACC"""

    homepage = 'https://claw-project.github.io/'
    git      = 'https://github.com/claw-project/claw-compiler.git'
    maintainers = ['clementval', 'skosukhin']

    version('2.0.3', tag='v2.0.3', submodules=True)
    version('2.0.2', tag='v2.0.2', submodules=True)
    version('2.0.1', tag='v2.0.1', submodules=True)
    version('2.0',   tag='v2.0', submodules=True)
    version('1.2.3', tag='v1.2.3', submodules=True)
    version('1.2.2', tag='v1.2.2', submodules=True)
    version('1.2.1', tag='v1.2.1', submodules=True)
    version('1.2.0', tag='v1.2.0', submodules=True)
    version('1.1.0', tag='v1.1.0', submodules=True)

    depends_on('cmake@3.0:', type='build')
    depends_on('ant@1.9:', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')

    depends_on('java@8:', when="@2.0:")
    depends_on('java@7:', when="@1.1.0:1.2.3")
    depends_on('libxml2')

    # Enable parsing of source files with calls to TRACEBACKQQ from the Intel
    # Fortran run-time library:
    patch('https://github.com/claw-project/claw-compiler/commit/e9fe6dbd291454ce34dd58f21d102f7f1bdff874.patch?full_index=1',
          sha256='262799fde57cb32f1514db22a7757e994bd8b97090ce0a5f55249fd56d0e5c29',
          when='@:2.0.2%intel')

    # Fix the dependency preprocessing for compilers that cannot use
    # redirection > to save file (cce is currently the only known case):
    patch('https://github.com/claw-project/claw-compiler/commit/4d8bc7a794af3651b8b61501388fc00096b23a85.patch?full_index=1',
          sha256='a20427456560070e284ff44edb658383b635042be91d2ffbe7aeb7afbd8f02bc',
          when='@2.0.2%cce')

    # Cache ANT dependencies in the stage directory.
    # Otherwise, they are cached to the user's home directory.
    patch('ivy_local_cache.patch')

    # https://github.com/claw-project/claw-compiler/pull/586
    conflicts('%nag', when='@:2.0.1')

    filter_compiler_wrappers('claw_f.conf', relative_root='etc')

    def flag_handler(self, name, flags):
        if name == 'cflags':
            if any([self.spec.compiler.satisfies(s) for s in
                    ['gcc@10:', 'clang@11:', 'cce@11:', 'aocc@3:']]):
                # https://gcc.gnu.org/gcc-10/porting_to.html
                # https://releases.llvm.org/11.0.0/tools/clang/docs/ReleaseNotes.html#modified-compiler-flags
                flags.append('-fcommon')

        return flags, None, None

    def cmake_args(self):
        args = [
            '-DOMNI_CONF_OPTION=--with-libxml2=%s' %
            self.spec['libxml2'].prefix
        ]

        return args
