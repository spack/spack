# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.version import ver


def get_best_target(microarch, compiler_name, compiler_version):
    for compiler_entry in microarch.compilers[compiler_name]:
        if compiler_version.satisfies(ver(compiler_entry["versions"])):
            return compiler_entry.get("name", microarch.name)
    raise InstallError("Could not find a target architecture")


class Julia(MakefilePackage):
    """The Julia Language: A fresh approach to technical computing"""

    homepage = "https://julialang.org"
    url = "https://github.com/JuliaLang/julia/releases/download/v1.7.0/julia-1.7.0.tar.gz"
    git = "https://github.com/JuliaLang/julia.git"

    maintainers("vchuravy", "haampie", "giordano")

    version("master", branch="master")
    version("1.9.0", sha256="48f4c8a7d5f33d0bc6ce24226df20ab49e385c2d0c3767ec8dfdb449602095b2")
    version("1.8.5", sha256="d31026cc6b275d14abce26fd9fd5b4552ac9d2ce8bde4291e494468af5743031")
    version("1.8.4", sha256="b7b8ee64fb947db8d61104f231e1b25342fe330d29e0d2273f93c264f32c5333")
    version("1.8.3", sha256="4d8d460fcae5c6f8306a3e3c14371635c1a26f47c3ce62b2950cf9234b6ec849")
    version("1.8.2", sha256="3e2cea35bf5df963ed7b75a83e8febfc000acf1e664ecd657a0772508eb1fb5d")
    version("1.8.1", sha256="066f4ca7a2ad39b003e2af77dbecfbfb9b0a1cb1664033f657ffdbe2f374d956")
    version("1.8.0", sha256="0fa980286d6d912f24ed9f90a02930560d985e0ada8233a4ae5610884feb2438")

    version("1.7.3", sha256="06df2a81e6a18d0333ffa58d36f6eb84934c38984898f9e0c3072c8facaa7306")
    version("1.7.2", sha256="0847943dd65001f3322b00c7dc4e12f56e70e98c6b798ccbd4f02d27ce161fef")
    version("1.7.1", sha256="17d298e50e4e3dd897246ccebd9f40ce5b89077fa36217860efaec4576aa718e")
    version("1.7.0", sha256="8e870dbef71bc72469933317a1a18214fd1b4b12f1080784af7b2c56177efcb4")

    version("1.6.7", sha256="74af1dc7b5841757a06a899923a62cac04665c09829324e8bf53cfb66f7b3d61")
    version("1.6.6", sha256="a8023708cadb2649395769810e6cec8afc8e352aa6d407189b6c88b86d7f5090")
    version("1.6.5", sha256="b70ae299ff6b63a9e9cbf697147a48a31b4639476d1947cb52e4201e444f23cb")
    version("1.6.4", sha256="a4aa921030250f58015201e28204bff604a007defc5a379a608723e6bb1808d4")

    variant("precompile", default=True, description="Improve julia startup time")
    variant("openlibm", default=True, description="Use openlibm instead of libm")

    # Note, we just use link_llvm_dylib so that we not only get a libLLVM,
    # but also so that llvm-config --libfiles gives only the dylib. Without
    # it it also gives static libraries, and breaks Julia's build.
    depends_on(
        "llvm"
        " targets=amdgpu,bpf,nvptx,webassembly"
        " version_suffix=jl +link_llvm_dylib libunwind=none"
    )
    depends_on("libuv", when="@:1.7")
    depends_on("libuv-julia@1.42.0", when="@1.8.0:1.8.1")
    depends_on("libuv-julia@1.44.2", when="@1.8.2:")

    with when("@1.9.0:1.9"):
        # libssh2.so.1, libpcre2-8.so.0, mbedtls.so.14, mbedcrypto.so.7, mbedx509.so.1
        # openlibm.so.4, libblastrampoline.so.5, libgit2.so.1.5, libnghttp2.so.14,
        # libcurl.so.4
        depends_on("libblastrampoline@5.4.0:5")
        depends_on("libgit2@1.5.0:1.5")
        depends_on("libssh2@1.10.0:1.10")
        depends_on("llvm@14.0.6 +lld shlib_symbol_version=JL_LLVM_14.0")
        depends_on("mbedtls@2.28.0:2.28")
        depends_on("openlibm@0.8.1:0.8", when="+openlibm")
        depends_on("nghttp2@1.48.0:1.48")
        depends_on("curl@7.84.0:")

    with when("@1.8.0:1.8"):
        # libssh2.so.1, libpcre2-8.so.0, mbedtls.so.14, mbedcrypto.so.7, mbedx509.so.1
        # openlibm.so.4, libblastrampoline.so.5, libgit2.so.1.3, libnghttp2.so.14,
        # libcurl.so.4
        depends_on("libblastrampoline@5.1.0:5")
        depends_on("libgit2@1.3.0:1.3")
        depends_on("libssh2@1.10.0:1.10")
        depends_on("llvm@13.0.1 shlib_symbol_version=JL_LLVM_13.0")
        depends_on("mbedtls@2.28.0:2.28")
        depends_on("openlibm@0.8.1:0.8", when="+openlibm")
        depends_on("nghttp2@1.47.0:1.47")
        depends_on("curl@7.84.0:")

    with when("@1.7.0:1.7"):
        # libssh2.so.1, libpcre2-8.so.0, mbedtls.so.13, mbedcrypto.so.5, mbedx509.so.1
        # openlibm.so.3
        depends_on("libblastrampoline@3.0.0:3")
        depends_on("libgit2@1.1.0:1.1")
        depends_on("libssh2@1.9.0:1.9")
        depends_on("libuv@1.42.0")
        depends_on("llvm@12.0.1")
        depends_on("mbedtls@2.24.0:2.24")
        depends_on("openlibm@0.7.0:0.7", when="+openlibm")
        depends_on("curl@7.73.0:")

    with when("@1.6.0:1.6"):
        # libssh2.so.1, libpcre2-8.so.0, mbedtls.so.13, mbedcrypto.so.5, mbedx509.so.1
        # openlibm.so.3, (todo: complete this list for upperbounds...)
        depends_on("libgit2@1.1.0:1.1")
        depends_on("libssh2@1.9.0:1.9")
        depends_on("libuv@1.39.0")
        depends_on("llvm@11.0.1")
        depends_on("mbedtls@2.24.0:2.24")
        depends_on("openlibm@0.7.0:0.7", when="+openlibm")
        depends_on("curl@7.73.0:")

    # Patches for llvm
    depends_on("llvm", patches="llvm7-symver-jlprefix.patch", when="@:1.7")
    depends_on(
        "llvm",
        when="^llvm@11.0.1",
        patches=patch(
            "https://raw.githubusercontent.com/spack/patches/0b543955683a903d711a3e95ff29a4ce3951ca13/julia/llvm-11.0.1-julia-1.6.patch",
            sha256="8866ee0595272b826b72d173301a2e625855e80680a84af837f1ed6db4657f42",
        ),
    )
    depends_on(
        "llvm",
        when="^llvm@12.0.1",
        patches=patch(
            "https://github.com/JuliaLang/llvm-project/compare/fed41342a82f5a3a9201819a82bf7a48313e296b...980d2f60a8524c5546397db9e8bbb7d6ea56c1b7.patch",
            sha256="10cb42f80c2eaad3e9c87cb818b6676f1be26737bdf972c77392d71707386aa4",
        ),
    )
    depends_on(
        "llvm",
        when="^llvm@13.0.1",
        patches=patch(
            "https://github.com/JuliaLang/llvm-project/compare/75e33f71c2dae584b13a7d1186ae0a038ba98838...2f4460bd46aa80d4fe0d80c3dabcb10379e8d61b.patch",
            sha256="45f72c59ae5cf45461e9cd8b224ca49b739d885c79b3786026433c6c22f83b5f",
        ),
    )
    depends_on(
        "llvm",
        when="^llvm@14.0.6",
        patches=patch(
            "https://github.com/JuliaLang/llvm-project/compare/f28c006a5895fc0e329fe15fead81e37457cb1d1...381043941d2c7a5157a011510b6d0386c171aae7.diff",
            sha256="f3def26930832532bbcd861d41b31ae03db993bc2b3510f89ef831a30bd3e099",
        ),
    )

    # Patches for libuv
    depends_on(
        "libuv",
        when="^libuv@1.39.0",
        patches=patch(
            "https://raw.githubusercontent.com/spack/patches/b59ca193423c4c388254f528afabb906b5373162/julia/libuv-1.39.0.patch",
            sha256="f7c1e7341e89dc35dfd85435ba35833beaef575b997c3f978c27d0dbf805149b",
        ),
    )
    depends_on(
        "libuv",
        when="^libuv@1.42.0",
        patches=patch(
            "https://raw.githubusercontent.com/spack/patches/89b6d14eb1f3c3d458a06f1e06f7dda3ab67bd38/julia/libuv-1.42.0.patch",
            sha256="d9252fbe67ac8f15e15653f0f6b00dffa07ae1a42f013d4329d17d8b492b7cdb",
        ),
    )

    # patchelf 0.13 is required because the rpath patch uses --add-rpath
    depends_on("patchelf@0.13:", type="build")
    depends_on("perl", type="build")
    depends_on("libwhich", type="build")

    depends_on("blas")  # note: for now openblas is fixed...
    depends_on("curl tls=mbedtls +nghttp2 +libssh2")
    depends_on("dsfmt@2.2.4:")  # apparently 2.2.3->2.2.4 breaks API
    depends_on("gmp")
    depends_on("lapack")  # note: for now openblas is fixed...
    depends_on("libblastrampoline", when="@1.7.0:")
    depends_on("libgit2")
    depends_on("libssh2 crypto=mbedtls")
    depends_on("mbedtls libs=shared")
    depends_on("mpfr")
    depends_on("nghttp2")
    depends_on("openblas +ilp64 symbol_suffix=64_")
    depends_on("openlibm", when="+openlibm")
    depends_on("p7zip")
    depends_on("pcre2")
    depends_on("suite-sparse +pic")
    depends_on("unwind")
    depends_on("utf8proc")
    depends_on("zlib +shared +pic +optimize")

    # Patches for julia
    patch("julia-1.6-system-libwhich-and-p7zip-symlink.patch", when="@1.6.0:1.6")
    patch("use-add-rpath.patch", when="@:1.8.0")
    patch("use-add-rpath-2.patch", when="@1.8.1:1.8")

    # Fix libstdc++ not being found (https://github.com/JuliaLang/julia/issues/47987)
    patch(
        "https://github.com/JuliaLang/julia/pull/48342.patch?full_index=1",
        sha256="10f7cab89c8353b2648a968d2c8e8ed8bd90961df3227084f1d69d3d482933d7",
        when="@1.8.4:1.8.5",
    )

    # Fix printing of `BigFloat`s when using MPFR 4.2.0, but the patch is
    # applicable to previous versions of the library too
    # (https://github.com/JuliaLang/julia/issues/49895).
    patch(
        "https://github.com/JuliaLang/julia/pull/49909.patch?full_index=1",
        sha256="7fa53516b97d83ccf06f6d387c04d337849808f7e8ee2bdc2e79894d84578afc",
        when="@1.6.4:1.9.0",
    )

    # Fix gfortran abi detection https://github.com/JuliaLang/julia/pull/44026
    patch("fix-gfortran.patch", when="@1.7.0:1.7.2")

    # Don't make julia run patchelf --set-rpath on llvm (presumably this should've
    # only applied to libllvm when it's vendored by julia).
    patch("revert-fix-rpath-of-libllvm.patch", when="@1.7.0:1.7.2")

    # Allow build with clang.
    patch("gcc-ifdef.patch", when="@1.7.0:1.7")

    # Make sure Julia sets -DNDEBUG when including LLVM header files.
    patch("llvm-NDEBUG.patch", when="@1.7.0:1.7")

    def patch(self):
        # The system-libwhich-libblastrampoline.patch causes a rebuild of docs as it
        # touches the main Makefile, so we reset the a/m-time to doc/_build's.
        f = os.path.join("doc", "_build", "html", "en", "index.html")
        if os.path.exists(f):
            time = (os.path.getatime(f), os.path.getmtime(f))
            os.utime(os.path.join("base", "Makefile"), time)

    def setup_build_environment(self, env):
        # this is a bit ridiculous, but we are setting runtime linker paths to
        # dependencies so that libwhich can locate them.
        if self.spec.satisfies("platform=linux") or self.spec.satisfies("platform=cray"):
            linker_var = "LD_LIBRARY_PATH"
        elif self.spec.satisfies("platform=darwin"):
            linker_var = "DYLD_FALLBACK_LIBRARY_PATH"
        else:
            return
        pkgs = [
            "curl",
            "dsfmt",
            "gmp",
            "libgit2",
            "libssh2",
            "libunwind",
            "mbedtls",
            "mpfr",
            "nghttp2",
            "openblas",
            "pcre2",
            "suite-sparse",
            "utf8proc",
            "zlib",
        ]
        if "+openlibm" in self.spec:
            pkgs.append("openlibm")
        if self.spec.satisfies("@1.7.0:"):
            pkgs.append("libblastrampoline")
        for pkg in pkgs:
            for dir in self.spec[pkg].libs.directories:
                env.prepend_path(linker_var, dir)

    def edit(self, spec, prefix):
        # TODO: use a search query for blas / lapack?
        libblas = os.path.splitext(spec["blas"].libs.basenames[0])[0]
        liblapack = os.path.splitext(spec["lapack"].libs.basenames[0])[0]

        # Host compiler target name
        march = get_best_target(spec.target, spec.compiler.name, spec.compiler.version)

        # LLVM compatible name for the JIT
        julia_cpu_target = get_best_target(spec.target, "clang", spec["llvm"].version)

        libuv = "libuv-julia" if "^libuv-julia" in spec else "libuv"

        options = [
            "prefix:={0}".format(prefix),
            "MARCH:={0}".format(march),
            "JULIA_CPU_TARGET:={0}".format(julia_cpu_target),
            "USE_BINARYBUILDER:=0",
            "VERBOSE:=1",
            # Spack managed dependencies
            "USE_SYSTEM_BLAS:=1",
            "USE_SYSTEM_CSL:=1",
            "USE_SYSTEM_CURL:=1",
            "USE_SYSTEM_DSFMT:=1",
            "USE_SYSTEM_GMP:=1",
            "USE_SYSTEM_LAPACK:=1",
            "USE_SYSTEM_LIBBLASTRAMPOLINE:=1",
            "USE_SYSTEM_LIBGIT2:=1",
            "USE_SYSTEM_LIBSSH2:=1",
            "USE_SYSTEM_LIBSUITESPARSE:=1",  # @1.7:
            "USE_SYSTEM_SUITESPARSE:=1",  # @:1.6
            "USE_SYSTEM_LIBUNWIND:=1",
            "USE_SYSTEM_LIBUV:=1",
            "USE_SYSTEM_LIBWHICH:=1",
            "USE_SYSTEM_LLD:=1",  # @1.9:
            "USE_SYSTEM_LLVM:=1",
            "USE_SYSTEM_MBEDTLS:=1",
            "USE_SYSTEM_MPFR:=1",
            "USE_SYSTEM_P7ZIP:=1",
            "USE_SYSTEM_PATCHELF:=1",
            "USE_SYSTEM_PCRE:=1",
            "USE_SYSTEM_UTF8PROC:=1",
            "USE_SYSTEM_ZLIB:=1",
            # todo: ilp depends on arch
            "USE_BLAS64:=1",
            "LIBBLASNAME:={0}".format(libblas),
            "LIBLAPACKNAME:={0}".format(liblapack),
            "override LIBUV:={0}".format(spec[libuv].libs.libraries[0]),
            "override LIBUV_INC:={0}".format(spec[libuv].headers.directories[0]),
            "override USE_LLVM_SHLIB:=1",
            # make rebuilds a bit faster for now, not sure if this should be kept
            "JULIA_PRECOMPILE:={0}".format("1" if spec.variants["precompile"].value else "0"),
            # we want to use `patchelf --add-rpath` instead of `patchelf --set-rpath`
            "override PATCHELF_SET_RPATH_ARG:=--add-rpath",  # @1.9:
        ]

        options.append("USEGCC:={}".format("1" if "%gcc" in spec else "0"))
        options.append("USECLANG:={}".format("1" if "%clang" in spec else "0"))

        options.extend(
            [
                "override CC:={0}".format(spack_cc),
                "override CXX:={0}".format(spack_cxx),
                "override FC:={0}".format(spack_fc),
            ]
        )

        # libm or openlibm?
        if spec.variants["openlibm"].value:
            options.append("USE_SYSTEM_LIBM=0")
            options.append("USE_SYSTEM_OPENLIBM=1")
        else:
            options.append("USE_SYSTEM_LIBM=1")
            options.append("USE_SYSTEM_OPENLIBM=0")

        with open("Make.user", "w") as f:
            f.write("\n".join(options) + "\n")
