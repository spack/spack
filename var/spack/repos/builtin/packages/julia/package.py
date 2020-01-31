# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import sys


class Julia(MakefilePackage):
    """The Julia Language: A fresh approach to technical computing"""

    homepage = "http://julialang.org"
    url      = "https://github.com/JuliaLang/julia/releases/download/v0.4.3/julia-0.4.3-full.tar.gz"
    git      = "https://github.com/JuliaLang/julia.git"

    extendable = True

    version('master', branch='master')
    version('1.2.0', sha256='2419b268fc5c3666dd9aeb554815fe7cf9e0e7265bc9b94a43957c31a68d9184')
    version('1.1.1', sha256='3c5395dd3419ebb82d57bcc49dc729df3b225b9094e74376f8c649ee35ed79c2')

    # TODO: Split these out into jl-hdf5, jl-mpi packages etc.

    variant('binutils', default=sys.platform != 'darwin',
            description="Build via binutils")

    variant("external_llvm", default=False, description="Use an external LLVM")

    # Build-time dependencies:
    depends_on("m4", type="build")
    depends_on("pkgconfig")

    # Combined build-time and run-time dependencies:
    # (Yes, these are run-time dependencies used by Julia's package manager.)
    depends_on("binutils", when='+binutils')
    depends_on("cmake @2.8:")
    depends_on("git")
    depends_on("openssl")

    # 1.2 and higher can be built with an external LLVM installation
    depends_on("llvm@7:7.999 +link_dylib", when="+external_llvm")
    # Python needed to build heavily patched included LLVM
    depends_on("python@2.7:2.8", when="@:1.2~external_llvm")

    # Run-time dependencies:

    # depends_on("blas")
    # depends_on("lapack")

    depends_on("pcre2")
    depends_on("gmp")
    depends_on("mpfr")
    depends_on("suite-sparse")

    # depends_on("libuv")
    depends_on("curl")
    depends_on("libgit2")
    # depends_on("libm")
    # depends_on("libxml2")
    # # depends_on("lzma")
    # depends_on("ncurses")
    # depends_on("zlib")


    # ARPACK: Requires BLAS and LAPACK; needs to use the same version
    # as Julia.

    # BLAS and LAPACK: Julia prefers 64-bit versions on 64-bit
    # systems. OpenBLAS has an option for this; make it available as
    # variant.

    # FFTW: Something doesn't work when using a pre-installed FFTW
    # library; need to investigate.

    # GMP, MPFR: Something doesn't work when using a pre-installed
    # FFTW library; need to investigate.

    # LLVM: Julia works only with specific versions, and might require
    # patches. Thus we let Julia install its own LLVM.

    # Other possible dependencies:
    # USE_SYSTEM_OPENLIBM=0
    # USE_SYSTEM_OPENSPECFUN=0
    # USE_SYSTEM_DSFMT=0
    # USE_SYSTEM_SUITESPARSE=0
    # USE_SYSTEM_UTF8PROC=0
    # USE_SYSTEM_LIBGIT2=0

    def edit(self, spec, prefix):
        # Julia needs git tags
        if os.path.isfile(".git/shallow"):
            git = which("git")
            git("fetch", "--unshallow")
        # Explicitly setting CC, CXX, or FC breaks building libuv, one
        # of Julia's dependencies. This might be a Darwin-specific
        # problem. Given how Spack sets up compilers, Julia should
        # still use Spack's compilers, even if we don't specify them
        # explicitly.
        options = [
            "USE_BINARYBUILDER=0",
            "USE_SYSTEM_LLVM={0}".format(1 if spec.satisfies('+external_llvm') else 0),
            "USE_SYSTEM_PCRE=1",
            "USE_SYSTEM_LIBM=1",
            # "USE_SYSTEM_BLAS=1",
            # "USE_SYSTEM_LAPACK=1",
            "USE_SYSTEM_GMP=1",
            "USE_SYSTEM_MPFR=1",
            "USE_SYSTEM_SUITESPARSE=1",
            # "USE_SYSTEM_LIBUV=1",
            "USE_SYSTEM_CURL=1",
            "USE_SYSTEM_LIBGIT2=1",

            # START Can be removed in future versions!
            "override USE_BINARYBUILDER_LLVM=0",
            "override USE_BINARYBUILDER_PCRE=0",
            "override USE_BINARYBUILDER_OPENBLAS=0",
            "override USE_BINARYBUILDER_OPENLIBM=0",
            "override USE_BINARYBUILDER_SUITESPARSE=0",
            "override USE_BINARYBUILDER_MBEDTLS=0",
            "override USE_BINARYBUILDER_LIBSSH2=0",
            "override USE_BINARYBUILDER_CURL=0",
            "override USE_BINARYBUILDER_LIBGIT2=0",
            "override USE_BINARYBUILDER_PCRE=0",
            "override USE_BINARYBUILDER_LIBUV=0",
            "override USE_BINARYBUILDER_UNWIND=0",
            # END remove

            # "# LIBBLAS={0}".format(spec["blas"].libs),
            # "LIBBLASNAME={0}".format(spec["blas"].name),
            # "# LIBLAPACK={0}".format(spec["lapack"].libs),
            # "LIBLAPACKNAME={0}".format(spec["lapack"].name),
            "prefix={0}".format(prefix)
        ]
        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')
