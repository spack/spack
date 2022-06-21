# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import shutil

from spack.package import *
from spack.repo import GitExe


class Easi(CMakePackage):
    """easi is a library for the Easy Initialization of models
    in three (or less or more) dimensional domains.
    """

    homepage = "https://easyinit.readthedocs.io"
    git = "https://github.com/SeisSol/easi.git"

    maintainers = ['ThrudPrimrose', 'ravil-mobile', 'krenzland']

    version('develop', branch='master')
    version('1.1.2', tag='v1.1.2')

    variant('asagi', default=True, description='build with ASAGI support')
    variant('jit', default='impalajit', description='build with JIT support',
            values=('impalajit', 'impalajit-llvm', 'lua'),
            multi=False)

    depends_on('asagi +mpi +mpi3', when='+asagi')
    depends_on('yaml-cpp@0.6.2')
    depends_on('impalajit-llvm@1.0.0', when='jit=impalajit-llvm')
    depends_on('lua@5.3.2', when='jit=lua')
    depends_on('git', type='build', when='jit=impalajit')

    conflicts('jit=impalajit', when='target=aarch64:')
    conflicts('jit=impalajit', when='target=ppc64:')
    conflicts('jit=impalajit', when='target=ppc64le:')
    conflicts('jit=impalajit', when='target=riscv64:')

    def pre_build(self):
        spec = self.spec
        if "jit=impalajit" in spec:
            impalajir_src = join_path(self.stage.source_path, 'impalajit')
            if os.path.isdir(impalajir_src):
                shutil.rmtree(impalajir_src)

            git_exe = GitExe()
            git_exe('clone', 'https://github.com/uphoffc/ImpalaJIT.git', impalajir_src)
            with working_dir(join_path(impalajir_src, 'build'), create=True):
                cmake('..', '-DCMAKE_INSTALL_PREFIX={0}'.format(self.spec.prefix))
                make()
                make('install')

    def cmake_args(self):
        self.pre_build()

        args = []
        args.append(self.define_from_variant('ASAGI', 'asagi'))

        with_impala = 'jit=impalajit' in self.spec
        with_impala |= 'jit=impalajit-llvm' in self.spec
        if with_impala:
            args.append(self.define('IMPALAJIT', True))
            backend_type = 'llvm' if 'jit=impalajit-llvm' in self.spec else 'original'
            args.append(self.define('IMPALAJIT_BACKEND', backend_type))

        if 'jit=lua' in self.spec:
            args.append(self.define('IMPALAJIT', False))
            args.append(self.define('LUA', True))

        return args
