# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SuiteSparse(Package):
    """
    SuiteSparse is a suite of sparse matrix algorithms
    """

    homepage = "https://people.engr.tamu.edu/davis/suitesparse.html"
    url = "https://github.com/DrTimothyAldenDavis/SuiteSparse/archive/v4.5.3.tar.gz"
    git = "https://github.com/DrTimothyAldenDavis/SuiteSparse.git"

    version("5.13.0", sha256="59c6ca2959623f0c69226cf9afb9a018d12a37fab3a8869db5f6d7f83b6b147d")
    version("5.12.0", sha256="5fb0064a3398111976f30c5908a8c0b40df44c6dd8f0cc4bfa7b9e45d8c647de")
    version("5.11.0", sha256="fdd957ed06019465f7de73ce931afaf5d40e96e14ae57d91f60868b8c123c4c8")
    version("5.10.1", sha256="acb4d1045f48a237e70294b950153e48dce5b5f9ca8190e86c2b8c54ce00a7ee")
    version("5.10.0", sha256="4bcc974901c0173acf80c41ee0fd779eb7dce2871d4afa24a5d15b1a468f93e5")
    version("5.9.0", sha256="7bdd4811f1cf0767c5fdb5e435817fdadee50b0acdb598f4882ae7b8291a7f24")
    version("5.8.1", sha256="06726e471fbaa55f792578f9b4ab282ea9d008cf39ddcc3b42b73400acddef40")
    version("5.8.0", sha256="94a9b7134eb4dd82b97f1a22a6b464feb81e73af2dcdf683c6f252285191df1d")
    version("5.7.2", sha256="fe3bc7c3bd1efdfa5cffffb5cebf021ff024c83b5daf0ab445429d3d741bd3ad")
    version("5.7.1", sha256="5ba5add1663d51a1b6fb128b50fe869b497f3096765ff7f8212f0ede044b9557")
    version("5.6.0", sha256="76d34d9f6dafc592b69af14f58c1dc59e24853dcd7c2e8f4c98ffa223f6a1adb")
    version("5.5.0", sha256="63c73451734e2bab19d1915796c6776565ea6aea5da4063a9797ecec60da2e3d")
    version("5.4.0", sha256="d9d62d539410d66550d0b795503a556830831f50087723cb191a030525eda770")
    version("5.3.0", sha256="d8ef4bee4394d2f07299d4688b83bbd98e9d3a2ebbe1c1632144b6f7095ce165")
    version("5.2.0", sha256="68c431aef3d9a0b02e97803eb61671c5ecb9d36fd292a807db87067dadb36e53")
    version("5.1.2", sha256="97dc5fdc7f78ff5018e6a1fcc841e17a9af4e5a35cebd62df6922349bf12959e")
    version("5.1.0", sha256="0b0e03c63e67b04529bb6248808d2a8c82259d40b30fc5a7599f4b6f7bdd4dc6")
    version("5.0.0", sha256="2f8694d9978033659f10ceb8bdb19147d3c519a0251b8de84be6ba8824d30517")
    version("4.5.6", sha256="1c7b7a265a1d6c606095eb8aa3cb8e27821f1b7f5bc04f28df6d62906e02f4e4")
    version("4.5.5", sha256="80d1d9960a6ec70031fecfe9adfe5b1ccd8001a7420efb50d6fa7326ef14af91")
    version("4.5.3", sha256="b6965f9198446a502cde48fb0e02236e75fa5700b94c7306fc36599d57b563f4")

    variant(
        "pic",
        default=True,
        description="Build position independent code (required to link with shared libraries)",
    )
    variant("cuda", default=False, description="Build with CUDA")
    variant("openmp", default=False, description="Build with OpenMP")
    variant(
        "graphblas",
        default=False,
        description="Build with GraphBLAS (takes a long time to compile)",
    )

    # In @4.5.1. TBB support in SPQR seems to be broken as TBB-related linking
    # flags does not seem to be used, which leads to linking errors on Linux.
    # Support for TBB has been removed in version 5.11
    variant("tbb", default=False, description="Build with Intel TBB", when="@4.5.3:5.10")

    depends_on("blas")
    depends_on("lapack")
    depends_on("cuda", when="+cuda")

    depends_on("mpfr@4.0.0:", when="@5.8.0:")
    depends_on("gmp", when="@5.8.0:")
    depends_on("m4", type="build", when="@5.0.0:")
    depends_on("cmake", when="+graphblas @5.2.0:", type="build")
    depends_on("metis@5.1.0", when="@4.5.1:")

    with when("+tbb"):
        depends_on("tbb")
        patch("tbb_453.patch", when="@4.5.3:4.5.5")
        # The @2021.x versions of tbb dropped the task_scheduler_init.h header and
        # related stuff (which have long been deprecated).  This appears to be
        # rather problematic for suite-sparse (see e.g.
        # https://github.com/DrTimothyAldenDavis/SuiteSparse/blob/master/SPQR/Source/spqr_parallel.cpp)
        depends_on("intel-tbb@:2020 build_system=makefile", when="^intel-tbb")
        conflicts(
            "^intel-oneapi-tbb@2021:",
            msg="suite-sparse needs task_scheduler_init.h dropped in recent tbb libs",
        )

    # This patch removes unsupported flags for pgi compiler
    patch("pgi.patch", when="%pgi")
    patch("pgi.patch", when="%nvhpc")

    # This patch adds '-lm' when linking libgraphblas and when using clang.
    # Fixes 'libgraphblas.so.2.0.1: undefined reference to `__fpclassify''
    patch("graphblas_libm_dep.patch", when="+graphblas @5.2.0:5.2%clang")

    # CUDA-11 dropped sm_30 code generation, remove hardcoded sm_30 from makefile
    # open issue: https://github.com/DrTimothyAldenDavis/SuiteSparse/issues/56
    # Tested only with 5.9.0, previous versions probably work too
    patch("fix_cuda11.patch", when="@5.9.0:5.10.0+cuda ^cuda@11:")

    conflicts(
        "%gcc@:4.8", when="@5.2.0:", msg="gcc version must be at least 4.9 for suite-sparse@5.2.0:"
    )

    def flag_handler(self, name, flags):
        if name in ("cflags", "cxxflags"):
            if self.spec.satisfies("^openblas ~shared threads=openmp"):
                flags.append(self.compiler.openmp_flag)
        return (flags, None, None)

    def symbol_suffix_blas(self, spec, args):
        """When using BLAS with a special symbol suffix we use defines to
        replace blas symbols, e.g. dgemm_ becomes dgemm_64_ when
        symbol_suffix=64_."""

        # Currently only OpenBLAS does this.
        if not spec.satisfies("^openblas"):
            return

        suffix = spec["openblas"].variants["symbol_suffix"].value
        if suffix == "none":
            return

        symbols = (
            "dtrsv_",
            "dgemv_",
            "dtrsm_",
            "dgemm_",
            "dsyrk_",
            "dger_",
            "dscal_",
            "dpotrf_",
            "ztrsv_",
            "zgemv_",
            "ztrsm_",
            "zgemm_",
            "zherk_",
            "zgeru_",
            "zscal_",
            "zpotrf_",
            "dnrm2_",
            "dlarf_",
            "dlarfg_",
            "dlarft_",
            "dlarfb_",
            "dznrm2_",
            "zlarf_",
            "zlarfg_",
            "zlarft_",
            "zlarfb_",
        )

        for symbol in symbols:
            args.append("CFLAGS+=-D{0}={1}{2}".format(symbol, symbol, suffix))

    def install(self, spec, prefix):
        # The build system of SuiteSparse is quite old-fashioned.
        # It's basically a plain Makefile which include an header
        # (SuiteSparse_config/SuiteSparse_config.mk)with a lot of convoluted
        # logic in it. Any kind of customization will need to go through
        # filtering of that file

        cc_pic_flag = self.compiler.cc_pic_flag if "+pic" in spec else ""
        f77_pic_flag = self.compiler.f77_pic_flag if "+pic" in spec else ""

        make_args = [
            # By default, the Makefile uses the Intel compilers if
            # they are found. The AUTOCC flag disables this behavior,
            # forcing it to use Spack's compiler wrappers.
            "AUTOCC=no",
            # CUDA=no does NOT disable cuda, it only disables internal search
            # for CUDA_PATH. If in addition the latter is empty, then CUDA is
            # completely disabled. See
            # [SuiteSparse/SuiteSparse_config/SuiteSparse_config.mk] for more.
            "CUDA=no",
            "CUDA_PATH=%s" % (spec["cuda"].prefix if "+cuda" in spec else ""),
            "CFOPENMP=%s" % (self.compiler.openmp_flag if "+openmp" in spec else ""),
            "CFLAGS=-O3 %s" % cc_pic_flag,
            # Both FFLAGS and F77FLAGS are used in SuiteSparse makefiles;
            # FFLAGS is used in CHOLMOD, F77FLAGS is used in AMD and UMFPACK.
            "FFLAGS=%s" % f77_pic_flag,
            "F77FLAGS=%s" % f77_pic_flag,
            # use Spack's metis in CHOLMOD/Partition module,
            # otherwise internal Metis will be compiled
            "MY_METIS_LIB=%s" % spec["metis"].libs.ld_flags,
            "MY_METIS_INC=%s" % spec["metis"].prefix.include,
            # Make sure Spack's Blas/Lapack is used. Otherwise System's
            # Blas/Lapack might be picked up. Need to add -lstdc++, following
            # with the TCOV path of SparseSuite 4.5.1's Suitesparse_config.mk,
            # even though this fix is ugly
            "BLAS=%s" % (spec["blas"].libs.ld_flags + (" -lstdc++" if "@4.5.1" in spec else "")),
            "LAPACK=%s" % spec["lapack"].libs.ld_flags,
        ]

        # Recent versions require c11 but some demos do not get the c11 from
        # GraphBLAS/CMakeLists.txt, for example the file
        # GraphBLAS/Demo/Program/wildtype_demo.c. For many compilers this is
        # not an issue because c11 or newer is their default. However, for some
        # compilers (e.g. xlc) the c11 flag is necessary.
        if spec.satisfies("@5.4:5.7.1") and ("%xl" in spec or "%xl_r" in spec):
            make_args += ["CFLAGS+=%s" % self.compiler.c11_flag]

        # 64bit blas in UMFPACK:
        if (
            spec.satisfies("^openblas+ilp64")
            or spec.satisfies("^intel-mkl+ilp64")
            or spec.satisfies("^intel-parallel-studio+mkl+ilp64")
        ):
            make_args.append('UMFPACK_CONFIG=-DLONGBLAS="long long"')

        # Handle symbol suffix of some BLAS'es (e.g. 64_ or _64 for ilp64)
        self.symbol_suffix_blas(spec, make_args)

        # SuiteSparse defaults to using '-fno-common -fexceptions' in
        # CFLAGS, but not all compilers use the same flags for these
        # optimizations
        if any([x in spec for x in ("%apple-clang", "%clang", "%gcc", "%intel", "%fj")]):
            make_args += ["CFLAGS+=-fno-common -fexceptions"]
        elif "%pgi" in spec:
            make_args += ["CFLAGS+=--exceptions"]

        if spack_f77.endswith("xlf") or spack_f77.endswith("xlf_r"):
            make_args += ["CFLAGS+=-DBLAS_NO_UNDERSCORE"]

        # Intel TBB in SuiteSparseQR
        if "+tbb" in spec:
            make_args += ["SPQR_CONFIG=-DHAVE_TBB", "TBB=%s" % spec["tbb"].libs.ld_flags]

        if "@5.3:" in spec:
            # Without CMAKE_LIBRARY_PATH defined, the CMake file in the
            # Mongoose directory finds libsuitesparseconfig.so in system
            # directories like /usr/lib.
            make_args += [
                "CMAKE_OPTIONS=-DCMAKE_INSTALL_PREFIX=%s" % prefix
                + " -DCMAKE_LIBRARY_PATH=%s" % prefix.lib
            ]

        if spec.satisfies("%gcc platform=darwin"):
            make_args += ["LDLIBS=-lm"]

        make_args.append("INSTALL=%s" % prefix)

        # Filter the targets we're interested in
        targets = [
            "SuiteSparse_config",
            "AMD",
            "BTF",
            "CAMD",
            "CCOLAMD",
            "COLAMD",
            "CHOLMOD",
            "CXSparse",
            "LDL",
            "KLU",
            "UMFPACK",
            "RBio",
        ]
        if spec.satisfies("+cuda"):
            targets.extend(["SuiteSparse_GPURuntime", "GPUQREngine"])
        targets.extend(["SPQR"])
        if spec.satisfies("+graphblas"):
            targets.append("GraphBLAS")
        if spec.satisfies("@5.8.0:"):
            targets.append("SLIP_LU")

        # Finally make and install
        make("-C", "SuiteSparse_config", "config", *make_args)
        for target in targets:
            make("-C", target, "library", *make_args)
            make("-C", target, "install", *make_args)

    @run_after("install")
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        # See https://github.com/DrTimothyAldenDavis/SuiteSparse/issues/42
        if "+pic platform=darwin" in self.spec:
            fix_darwin_install_name(self.spec.prefix.lib)

    @property
    def libs(self):
        """Export the libraries of SuiteSparse.
        Sample usage: spec['suite-sparse'].libs.ld_flags
                      spec['suite-sparse:klu,btf'].libs.ld_flags
        """
        # Component libraries, ordered by dependency. Any missing components?
        all_comps = [
            "klu",
            "btf",
            "umfpack",
            "cholmod",
            "colamd",
            "amd",
            "camd",
            "ccolamd",
            "cxsparse",
            "ldl",
            "rbio",
            "spqr",
            "suitesparseconfig",
        ]
        query_parameters = self.spec.last_query.extra_parameters
        comps = all_comps if not query_parameters else query_parameters
        return find_libraries(
            ["lib" + c for c in comps], root=self.prefix.lib, shared=True, recursive=False
        )
