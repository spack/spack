# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class ImpalajitLlvm(CMakePackage):
    """Impala is a calculator-like language. This is a fork of
    the original ImpalaJIT project and was enhanced with LLVM JIT.
    Impala acts as a backend for `easi` project.
    """

    homepage = "https://github.com/ravil-mobile/ImpalaJIT"
    git = "https://github.com/ravil-mobile/ImpalaJIT"

    maintainers = ['ravil-mobile']

    version('develop', branch='master')
    version('1.0.0', tag='v1.0.0')

    variant('shared', default=True, description='build as a shared library')

    depends_on('llvm@10.0.0:11.1.0')
    depends_on('z3')

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant('SHARED_LIB', 'shared'))
        return args
