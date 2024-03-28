# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.build_systems import cmake, makefile
from spack.package import *


class Abacus(MakefilePackage, CMakePackage, CudaPackage, ROCmPackage):
    """ABACUS (Atomic-orbital Based Ab-initio Computation at UStc)
    is an open-source computer code package aiming
    for large-scale electronic-structure simulations
    from first principles"""

    maintainers("yizeyi18", "QuantumMisaka", "caic99")

    build_system("cmake", conditional("makefile", when="@:2.3.4"), default="cmake")

    homepage = "http://abacus.ustc.edu.cn/"
    git = "https://github.com/deepmodeling/abacus-develop.git"
    url = "https://github.com/deepmodeling/abacus-develop/archive/refs/tags/v2.2.1.tar.gz"

    license("LGPL-3.0-or-later")

    version("develop", branch="develop")
    version("3.5.4", sha256="ab7cbdd07a951da116cc4fe4dfa23e7ac41dda9f35c35d16c267920f267f4722")
    version("3.5.3", sha256="f56066473dbd562f170f40809738076c0862321499ae7fcbd71508581f9ba7bf")
    version("3.5.2", sha256="b4823db244bc68cfa2cff0b4d33140051f56925b19c411f136ce27fb8e1ed3be")
    version("3.5.1", sha256="0867b74ef866033d0120f8b1040fdae8f1dc72a113ffdac6b472b2c8bf1eaf0e")
    version("3.5.0", sha256="0bc43af9bdb5b6a7bc30a72d680bb5054932ecedeb6fd3f4cdd3c4be0651c251")
    version("3.4.4", sha256="654590f97b2ff3ec49f800da667f24fc34c3ff42b392248b9c88104f8d3bf010")
    version("3.4.3", sha256="2c40d2d688ba599d2dcfa916c0e44a5d1a79d04213a9351830aaf231e6e321fe")
    version("3.4.2", sha256="251594ad864580181a26149819572631b757480ee9ce49a473d48855e55a084e")
    version("3.4.1", sha256="20f9a0e99320b1d4cf477ee55a17d1d88c2aa0b019c9a714d38a27a9cc700953")
    version("3.4.0", sha256="01ea63f921596f574d7eb93762724dbd45b01416bec8e3f719834ed7d2e7ed57")
    version("3.3.4", sha256="f9ef0baa624e39eb4f8a4fd7533d1bdd8f61ee3764a62ac980f51238aa102e38")
    version("3.3.3", sha256="8de5904656f7f83c5f5df32b0f05ec2d28c2fbb832576532f7714ea545620327")
    version("3.3.2", sha256="dc3049f68efa72d4e8c3e2c34e7553dbb057242cea3fbca062d5dd484e42bc53")
    version("3.3.1", sha256="29e1a78e1e370e45c5730df4a4b5ae52de74d0cf86771ca9f62dde34643f0f2d")
    version("3.3.0", sha256="9979572b0a60f74e1de432afeec072e16e0994b6a8f5fd5fb9985c3ff34d7816")
    version("3.2.5", sha256="8b96f9e509dedfb3cb43f802715a3ea8bde5d499a525171e314eebe6993c5897")
    version("3.2.4", sha256="65a84a4a02a085c42f86d54b487bf3f1501a45f940370a8a7527c881145f78d6")
    version("3.2.3", sha256="e01d2dd82ec1732499ea92a8ba48660593bc4ba4e165c1347b772561a005866d")
    version("3.2.2", sha256="80c11f6e7fa0b58cd3ef61ed101e519733eed32d7ddd125d9dbccc363f33ffa0")
    version("3.2.1", sha256="05389d66cb4e019764d2f1c8b51cfd445174c229629abe00dd4d31bfdc8ade08")
    version("3.2.0", sha256="cf7de312f6ddf1957621d6acc198ca4aa4e20924df7b4fda69454758e4614ea4")
    version("3.1.4", sha256="4aaf150d74e1c01726f012d23aa1e40e119cac9b8330ae425a29ec3b1040ef1c")
    version("3.1.3", sha256="ca056628472c8959f93f78e8e4fe10e1ea51a0b3333cef0c8c841dd22f9c0d1b")
    version("3.1.2", sha256="0fcebc659754deecfa912391a14ee9749c84ec45849e8b231ad9c765602826d4")
    version("3.1.1", sha256="a268a28e8dce2da98260265cb8edd0a16dd4a307a5016022c5cd2598e9df93c9")
    version("3.1.0", sha256="f038e20c712276c5a7c8f26ed6af6ff5d7c57110accd45882d11b1d64dee3f90")
    version("3.0.5", sha256="81ff1b8f10909eeda2d888f97f615e5b92aa26c101a32f36f346f78aa7638ba9")
    version("3.0.4", sha256="b01714e734b0aa5b0b52f3d7871e4bc9f6c81f25a444b1287e3f2e98a4f5d289")
    version("3.0.3", sha256="a4ae83cdb2c5029f152064f163d1b66b265980793d76b79908c073027401d2fc")
    version("3.0.2", sha256="b0c3aad9cac18d0ca73c78c69326031407af6a4bfcc953b3a27506c298bc59a3")
    version("3.0.1", sha256="812941146c31ab53c9a7695abbca6bfb36ae55878e38f8d0f13a17f3d9c36dc0")
    version("3.0.0", sha256="1c1299f53788beb2f6b6180d8484d584b6f293c81cea25f45b9632dd608ba4f9")
    version(
        "2.3.5",
        sha256="81c44be76c820b59a8b95f2b398c772160068a5e323f319e33704ff87dbefc5e",
        deprecated=True,
    )
    version(
        "2.3.4",
        sha256="16b817311c8055cf055021d895642fbb913585f08ec96f9aff3e0ef20148ec0e",
        deprecated=True,
    )
    version(
        "2.3.3",
        sha256="a1246c4a6de385826cae15d9a446e862331eb189a592622b1014c7b49504c908",
        deprecated=True,
    )
    version(
        "2.3.2",
        sha256="edcaae88e51360548bbdf1bcbd5048bec0d309b4fe11d8d11d5425afc001e9a1",
        deprecated=True,
    )
    version(
        "2.3.1",
        sha256="e9522469f499bcb1c57ec05e9866403e4142c97762d7662b4b638f7493bf5122",
        deprecated=True,
    )
    version(
        "2.3.0",
        sha256="c5a803a1a596983681d65aff46762f2f6b82b5f50449a53d0ec7dad368d35842",
        deprecated=True,
    )
    version(
        "2.2.4",
        sha256="1f3923d32c392fd2564d137b076134aebdc461dc3148c535a00f9b10a615157a",
        deprecated=True,
    )
    version(
        "2.2.3",
        sha256="88dbf6a3bdd907df3e097637ec8e51fde13e2f5e0b44f3667443195481320edf",
        deprecated=True,
    )
    version(
        "2.2.2",
        sha256="4a7cf2ec6e43dd5c53d5f877a941367074f4714d93c1977a719782957916169e",
        deprecated=True,
    )
    version(
        "2.2.1",
        sha256="14feca1d8d1ce025d3f263b85ebfbebc1a1efff704b6490e95b07603c55c1d63",
        deprecated=True,
    )
    version(
        "2.2.0",
        sha256="09d4a2508d903121d29813a85791eeb3a905acbe1c5664b8a88903f8eda64b8f",
        deprecated=True,
    )

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant(
        "lcao",
        default=True,
        description="Enable Linear Combinition of Atomic Orbital calculation",
        when="+mpi",
    )
    variant("libxc", default=True, description="Support additional functionals via libxc")
    variant(
        "elpa",
        default=True,
        description="Enable optimised diagonalisation routines from ELPA",
        when="+lcao",
    )
    variant("mathlib", default=False, description="Enable ABACUS's builtin libm")
    variant(
        "tests", default=False, description="Build ABACUS unit tests", when="build_system=cmake"
    )
    variant(
        "benchmarks",
        default=False,
        description="Enable ABACUS's builtin benchmark tests",
        when="+tests",
    )
    variant("rocm", default=False, description="(Experimental)Enable rocm support")
    # TODO: Add support for
    # LibRI(https://github.com/abacusmodeling/LibRI),
    # LibComm(https://github.com/abacusmodeling/LibComm),
    # Libnpy(https://github.com/llohse/libnpy/),
    # DeePKS(https://github.com/deepmodeling/deepks-kit),
    # DeePMD(https://github.com/deepmodeling/deepmd-kit),
    # LibPAW-interface(https://github.com/wenfei-li/libpaw_interface),
    # At 2024-1-30, none of above have a spack package.

    depends_on("fftw-api@3")
    depends_on("blas")
    depends_on("lapack")

    with when("+mpi"):
        depends_on("mpi", type=("build", "link", "run"))
    with when("+libxc"):
        depends_on("libxc")
    with when("+lcao"):
        depends_on("cereal")
        depends_on("scalapack")
    with when("+elpa"):
        depends_on("elpa")
    with when("+tests"):
        depends_on("googletest")
    with when("+benchmarks"):
        depends_on("benchmark")
    with when("+openmp"):
        depends_on("fftw+openmp", when="^[virtuals=fftw-api] fftw")
        depends_on("elpa+openmp", when="+elpa")
        depends_on(
            "openblas threads=openmp",
            when="^[virtuals=blas] openblas" or "^[virtuals=lapack] openblas",
        )
    with when("~openmp"):
        depends_on("elpa~openmp", when="+elpa")

    requires("%clang", when="+rocm", msg="build with rocm requires rocm compiler")

    conflicts(
        "^blis",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    conflicts(
        "^libflame",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    conflicts(
        "^amdblis",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    conflicts(
        "^amdlibflame",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    # netlab-lapack+external-blas do NOT contain libblas.so and not detectable
    # for abacus CMake script.
    conflicts(
        "^[virtuals=lapack] netlib-lapack~external-blas",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )
    conflicts(
        "^netlib-xblas",
        when="@:3.5.4",
        msg="abacus spack package supports openblas/mkl as blas/lapack provider",
    )


class MakefileBuilder(makefile.MakefileBuilder):
    build_directory = "source"

    def edit(self, pkg, spec, prefix):
        if "+openmp" in spec:
            inc_var = "_openmp-"
            system_var = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa_openmp -Wl, -rpath=${ELPA_LIB_DIR}"
        else:
            inc_var = "-"
            system_var = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa -Wl,-rpath=${ELPA_LIB_DIR}"

        tempInc = (
            "\
FORTRAN = ifort\n\
CPLUSPLUS = icpc\n\
CPLUSPLUS_MPI = mpiicpc\n\
LAPACK_DIR = $(MKLROOT)\n\
FFTW_DIR = %s\n\
ELPA_DIR = %s\n\
ELPA_INCLUDE = -I${ELPA_DIR}/include/elpa%s%s\n\
CEREAL_DIR = %s\n\
OBJ_DIR = obj\n\
OBJ_DIR_serial = obj\n\
NP      = 14\n"
            % (
                spec["fftw"].prefix,
                spec["elpa"].prefix,
                inc_var,
                f"{spec['elpa'].version}",
                spec["cereal"].prefix,
            )
        )

        with open(self.build_directory + "/Makefile.vars", "w") as f:
            f.write(tempInc)

        lineList = []
        Pattern1 = re.compile("^ELPA_INCLUDE_DIR")
        Pattern2 = re.compile("^ELPA_LIB\\s*= ")
        with open(self.build_directory + "/Makefile.system", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                elif Pattern1.search(line):
                    pass
                elif Pattern2.search(line):
                    pass
                else:
                    lineList.append(line)
        with open(self.build_directory + "/Makefile.system", "w") as f:
            for i in lineList:
                f.write(i)

        with open(self.build_directory + "/Makefile.system", "a") as f:
            f.write(system_var)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("USE_OPENMP", "openmp"),
            self.define_from_variant("USE_ELPA", "elpa"),
            self.define_from_variant("USE_ABACUS_LIBM", "mathlib"),
            self.define_from_variant("ENABLE_LCAO", "lcao"),
            self.define_from_variant("ENABLE_LIBXC", "libxc"),
            self.define_from_variant("ENABLE_GOOGLEBENCH", "benchmarks"),
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("USE_ROCM", "rocm"),
            self.define_from_variant("USE_CUDA", "cuda"),
        ]

        blas = spec["blas"]
        lapack = spec["lapack"]
        # fftw = spec["fftw-api"]
        # scalapack = spec["scalapack"] if spec.satisfies("+lcao") else ""
        if blas.name in ["intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"]:
            args += [self.define("MKLROOT", spec["mkl"].prefix)]
        elif spec.satisfies("@:3.5.4"):
            args.extend(
                [
                    self.define("LAPACK_FOUND", True),
                    self.define(
                        "LAPACK_LIBRARY", lapack.libs
                    ),  # must be single lib with both blas&lapack routines
                ]
            )

        # avoid misdirecting to global visible elpa from apt, dnf, etc.
        if spec.satisfies("+elpa"):
            elpa = spec["elpa"]
            elpa_include = elpa.headers.directories[0]
            args += [self.define("ELPA_INCLUDE_DIRS", elpa_include)]

        if spec.satisfies("+rocm"):
            args += [self.define("COMMIT_INFO", False)]
            args += [self.define("ROCM_PATH", spec["hip"].prefix)]
            # build all c++ part with rocm compiler.
            # cpu and gpu parts can be seperately build, but not done.
            # args += [
            #     self.define(
            #         "CMAKE_CXX_COMPILER",
            #         join_path(spec["llvm-amdgpu"].prefix.bin,"clang++")
            #         )
            #     ]
            # only work for dcu toolkit 23.10 environment, not sure if any other version needs
            args += [
                self.define(
                    "HIP_CXX_COMPILER", join_path(spec["llvm-amdgpu"].prefix.bin, "clang++")
                )
            ]
        return args
