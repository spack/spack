# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package_defs import *
from spack.pkg.builtin.blis import BlisBase


class Amdblis(BlisBase):
    """AMD Optimized BLIS.

    BLIS is a portable software framework for instantiating high-performance
    BLAS-like dense linear algebra libraries. The framework was designed to
    isolate essential kernels of computation that, when optimized, immediately
    enable optimized implementations of most of its commonly used and
    computationally intensive operations.
    """

    _name = 'amdblis'
    homepage = "https://developer.amd.com/amd-aocl/blas-library/"
    url = "https://github.com/amd/blis/archive/3.0.tar.gz"
    git = "https://github.com/amd/blis.git"

    maintainers = ['amd-toolchain-support']

    version('3.1', sha256='2891948925b9db99eec02a1917d9887a7bee9ad2afc5421c9ba58602a620f2bf')
    version('3.0.1', sha256='dff643e6ef946846e91e8f81b75ff8fe21f1f2d227599aecd654d184d9beff3e')
    version('3.0', sha256='ac848c040cd6c3550fe49148dbdf109216cad72d3235763ee7ee8134e1528517')
    version('2.2', sha256='e1feb60ac919cf6d233c43c424f6a8a11eab2c62c2c6e3f2652c15ee9063c0c9')

    variant('ilp64', default=False, when='@3.0.1:', description='ILP64 support')

    def configure_args(self):
        spec = self.spec
        args = super(Amdblis, self).configure_args()

        if spec.satisfies('+ilp64'):
            args.append('--blas-int-size=64')

        # To enable Fortran to C calling convention for
        # complex types when compiling with aocc flang
        if self.spec.satisfies("@3.0 %aocc"):
            args.append('CFLAGS={0}'.format("-DAOCL_F2C"))
            args.append('CXXFLAGS={0}'.format("-DAOCL_F2C"))
        elif self.spec.satisfies("@3.0.1: %aocc"):
            args.append('--complex-return=intel')

        if self.spec.satisfies("@3.1:"):
            args.append('--disable-aocl-dynamic')

        return args

    def config_args(self):
        config_args = super(Amdblis, self).config_args()

        # "amdzen" - A fat binary or multiarchitecture binary
        # support for 3.1 release onwards
        if self.spec.satisfies("@3.1:"):
            config_args.append("amdzen")
        else:
            config_args.append("auto")

        return config_args
