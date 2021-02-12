# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fasttransforms(MakefilePackage):
    """FastTransforms provides computational kernels and driver routines for
    orthogonal polynomial transforms. The univariate algorithms have a runtime
    complexity of O(n log n), while the multivariate algorithms are 2-normwise
    backward stable with a runtime complexity of O(nd+1), where n is the
    polynomial degree and d is the spatial dimension of the problem."""

    homepage = "https://github.com/MikaelSlevinsky/FastTransforms"
    url      = "https://github.com/MikaelSlevinsky/FastTransforms/archive/v0.3.4.tar.gz"

    version('0.5.0', sha256='9556d0037bd5348a33f15ad6100e32053b6e22cab16a97c504f30d6c52fd0efd')
    version('0.4.1', sha256='5d30b3b9cb8e1260072b81831e4beeb73e5a956fa8952df8281e9dab399bbbb4')
    version('0.4.0', sha256='0a7c85a0f10acc0d57f9498925f941b79eff68b942eb89067f973ba08fb7a1bc')
    version('0.3.4', sha256='a5c8b5aedbdb40218521d061a7df65ef32ce153d4e19d232957db7e3e63c7e9b')

    variant('quadmath', default=False, description="Support 128-bit floats")

    depends_on('blas')
    depends_on('fftw')
    depends_on('mpfr')

    def build(self, spec, prefix):
        makeargs = ["CC=cc"]
        if 'openblas' in spec:
            makeargs += ["FT_BLAS=openblas"]
        if 'quadmath' in spec:
            makeargs += ["FT_QUADMATH=1"]
        make('assembly', *makeargs)
        make('lib', *makeargs)

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install(join_path('src', '*.h'), prefix.include)
        mkdirp(prefix.lib)
        install('libfasttransforms.' + dso_suffix, prefix.lib)
