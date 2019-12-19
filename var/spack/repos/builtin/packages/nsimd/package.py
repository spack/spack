# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nsimd(CMakePackage):

    """NSIMD is a vectorization library that abstracts SIMD programming.
    It was designed to exploit the maximum power of processors
    at a low development cost."""

    homepage = "https://agenium-scale.github.io/nsimd/"
    url      = "https://github.com/agenium-scale/nsimd/archive/v1.0.tar.gz"

    maintainers = ['eschnett']

    version('1.0', 'a692d25ed0335f1a6bb901c4b2c9fc47e26f8bf3')



    variant('simd',
            default='none',
            description='SIMD instruction set',
            values=(
                'none',
                'CPU',
                'SSE2', 'SSE42', 'AVX', 'AVX2', 'AVX512_KNL', 'AVX512_SKYLAKE',
                'NEON128', 'AARCH64', 'SVE',
            ),
            multi=False)
    variant('optionals',
            default=(),
            description='Optional SIMD features',
            values=('FMA', 'FP16'),
            multi=True)

    # Requires a C++14 compiler for building.
    # The C++ interface requires a C++11 compiler to use.
    depends_on('cmake@2.8.7:', type='build')
    depends_on('python@3:', type='build')

    # Add 'check_options' and 'generate_code' phases in the beginning
    phases = ['check_options', 'generate_code'] + CMakePackage.phases

    def check_options(self, spec, prefix):
        simd = self.spec.variants['simd'].value
        if simd == 'none':
            raise InstallError("'simd' variant is not set")

    def generate_code(self, spec, prefix):
        """Auto-generates code in the build directory"""
        options = [
            'egg/hatch.py',
            '--all',
            '--force',
            '--disable-clang-format',
        ]
        python = which('python')
        python(*options)

    def cmake_args(self):
        simd = self.spec.variants['simd'].value
        optionals = ';'.join(self.spec.variants['optionals'].value)
        cmake_args = [
            "-DSIMD={0}".format(simd),
            "-DSIMD_OPTIONALS={0}".format(optionals),
        ]
        return cmake_args
