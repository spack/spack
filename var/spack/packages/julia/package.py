from spack import *

class Julia(Package):
    """The Julia Language: A fresh approach to technical computing"""
    homepage = "http://julialang.org"
    url      = "http://github.com/JuliaLang/julia/releases/download/v0.4.2/julia-0.4.2.tar.gz"

    version('0.4.2', 'ccfeb4f4090c8b31083f5e1ccb03eb06')

    # Build-time dependencies
    # depends_on("cmake")
    # depends_on("awk")
    # depends_on("m4")
    # depends_on("pkg-config")

    # Run-time dependencies
    #TODO depends_on("arpack")
    #TODO depends_on("fftw")
    #TODO depends_on("git")
    #TODO depends_on("gmp")
    # depends_on("libedit")
    #TODO depends_on("mpfr")
    #TODO depends_on("pcre2")
    # depends_on("zlib")

    # BLAS and LAPACK: Julia prefers 64-bit versions on 64-bit systems. OpenBLAS
    # has an option for this; make it available as variant.

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
        options = ["CC=cc",
                   "CXX=c++",
                   "FC=fc",
                   #TODO "USE_SYSTEM_ARPACK=1",
                   #TODO "USE_SYSTEM_FFTW=1",
                   #TODO "USE_SYSTEM_GMP=1",
                   #TODO "USE_SYSTEM_MPFR=1",
                   #TODO "USE_SYSTEM_PCRE=1",
                   "prefix=%s" % prefix]
        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')
        which('env')()
        which('env')('which', 'cc')
        make()
        make("install")
