from spack import *
import os

class Julia(Package):
    """The Julia Language: A fresh approach to technical computing"""
    homepage = "http://julialang.org"
    url      = "http://github.com/JuliaLang/julia/releases/download/v0.4.2/julia-0.4.2.tar.gz"

    version('0.4.2', 'ccfeb4f4090c8b31083f5e1ccb03eb06')

    # Build-time dependencies
    depends_on("cmake")
    # depends_on("awk")
    # depends_on("m4")
    # depends_on("pkg-config")

    # I think that Julia requires the dependencies above, but it builds find (on
    # my system) without these. We should enable them as necessary.

    # Run-time dependencies
    # depends_on("arpack")
    # depends_on("fftw +float")
    # depends_on("gmp")
    # depends_on("mpfr")
    # depends_on("pcre2")

    # ARPACK: Requires BLAS and LAPACK; needs to use the same version as Julia.

    # BLAS and LAPACK: Julia prefers 64-bit versions on 64-bit systems. OpenBLAS
    # has an option for this; make it available as variant.

    # FFTW: Something doesn't work when using a pre-installed FFTW library; need
    # to investigate.

    # GMP, MPFR: Something doesn't work when using a pre-installed FFTW library;
    # need to investigate.

    # LLVM: Julia works only with specific versions, and might require patches.
    # Thus we let Julia install its own LLVM.

    # Other possible dependencies:
    # USE_SYSTEM_OPENLIBM=0
    # USE_SYSTEM_OPENSPECFUN=0
    # USE_SYSTEM_DSFMT=0
    # USE_SYSTEM_SUITESPARSE=0
    # USE_SYSTEM_UTF8PROC=0
    # USE_SYSTEM_LIBGIT2=0

    def install(self, spec, prefix):
        # Explicitly setting CC, CXX, or FC breaks building libuv, one of
        # Julia's dependencies. This might be a Darwin-specific problem. Given
        # how Spack sets up compilers, Julia should still use Spack's compilers,
        # even if we don't specify them explicitly.
        options = [#"CC=cc",
                   #"CXX=c++",
                   #"FC=fc",
                   #"USE_SYSTEM_ARPACK=1",
                   #"USE_SYSTEM_FFTW=1",
                   #"USE_SYSTEM_GMP=1",
                   #"USE_SYSTEM_MPFR=1",
                   #TODO "USE_SYSTEM_PCRE=1",
                   "prefix=%s" % prefix]
        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')
        make()
        make("install")
