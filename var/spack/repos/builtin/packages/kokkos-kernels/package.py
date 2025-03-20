# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class KokkosKernels(CMakePackage, CudaPackage):
    """Kokkos Kernels provides math kernels, often BLAS or LAPACK
    for small matrices, that can be used in larger Kokkos parallel routines"""

    homepage = "https://github.com/kokkos/kokkos-kernels"
    git = "https://github.com/kokkos/kokkos-kernels.git"
    url = "https://github.com/kokkos/kokkos-kernels/releases/download/4.4.01/kokkos-kernels-4.4.01.tar.gz"

    tags = ["e4s"]

    test_requires_compiler = True

    maintainers("lucbv", "srajama1", "brian-kelley")

    license("Apache-2.0 WITH LLVM-exception")

    version("develop", branch="develop")
    version("master", branch="master")
    version("4.5.01", sha256="c111a6561f23a85af9850d1df1e9015f37a586f1da0be4b6fb1e98001d75e074")
    version("4.5.00", sha256="94726a64e349adf6cd276e9fdc1b2bf7ff81efec833e479a5d3024b83f165a59")
    version("4.4.01", sha256="4a32bc8330e0113856bdf181df94cc4f9902e3cebb5dc7cea5948f30df03bfa1")
    version("4.4.00", sha256="66d5c3f728a8c7689159c97006996164ea00fd39702476220e3dbf2a05c49e8f")
    version(
        "4.3.01",
        sha256="749553a6ea715ba1e56fa0b13b42866bb9880dba7a94e343eadf40d08c68fab8",
        url="https://github.com/kokkos/kokkos-kernels/archive/4.3.01.tar.gz",
    )
    version(
        "4.3.00",
        sha256="03c3226ee97dbca4fa56fe69bc4eefa0673e23c37f2741943d9362424a63950e",
        url="https://github.com/kokkos/kokkos-kernels/archive/4.3.00.tar.gz",
    )
    version(
        "4.2.01",
        sha256="058052b3a40f5d4e447b7ded5c480f1b0d4aa78373b0bc7e43804d0447c34ca8",
        url="https://github.com/kokkos/kokkos-kernels/archive/4.2.01.tar.gz",
    )
    version(
        "4.2.00",
        sha256="c65df9a101dbbef2d8fd43c60c9ea85f2046bb3535fa1ad16e7c661ddd60401e",
        url="https://github.com/kokkos/kokkos-kernels/archive/4.2.00.tar.gz",
    )
    version(
        "4.1.00",
        sha256="d6a4108444ea226e43bf6a9c0dfc557f223a72b1142bf81aa78dd60e16ac2d56",
        url="https://github.com/kokkos/kokkos-kernels/archive/4.1.00.tar.gz",
    )
    version(
        "4.0.01",
        sha256="3f493fcb0244b26858ceb911be64092fbf7785616ad62c81abde0ea1ce86688a",
        url="https://github.com/kokkos/kokkos-kernels/archive/4.0.01.tar.gz",
    )
    version(
        "4.0.00",
        sha256="750079d0be1282d18ecd280e130ca303044ac399f1e5864488284b92f5ce0a86",
        url="https://github.com/kokkos/kokkos-kernels/archive/4.0.00.tar.gz",
    )
    version(
        "3.7.01",
        sha256="b2060f5894bdaf7f7d4793b90444fac260460cfa80595afcbcb955518864b446",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.7.01.tar.gz",
    )
    version(
        "3.7.00",
        sha256="51bc6db3995392065656848e2b152cfd1c3a95a951ab18a3934278113d59f32b",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.7.00.tar.gz",
    )
    version(
        "3.6.01",
        sha256="f000b156c8c0b80e85d38587907c11d9479aaf362408b812effeda5e22b24d0d",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.6.01.tar.gz",
    )
    version(
        "3.6.00",
        sha256="2753643fd643b9eed9f7d370e0ff5fa957211d08a91aa75398e31cbc9e5eb0a5",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.6.00.tar.gz",
    )
    version(
        "3.5.00",
        sha256="a03a41a047d95f9f07cd1e1d30692afdb75b5c705ef524e19c1d02fe60ccf8d1",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.5.00.tar.gz",
    )
    version(
        "3.4.01",
        sha256="f504aa4afbffb58fa7c4430d0fdb8fd5690a268823fa15eb0b7d58dab9d351e6",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.4.01.tar.gz",
    )
    version(
        "3.4.00",
        sha256="07ba11869e686cb0d47272d1ef494ccfbcdef3f93ff1c8b64ab9e136a53a227a",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.4.00.tar.gz",
    )
    version(
        "3.3.01",
        sha256="0f21fe6b5a8b6ae7738290e293aa990719aefe88b32f84617436bfd6074a8f77",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.3.01.tar.gz",
    )
    version(
        "3.3.00",
        sha256="8d7f78815301afb90ddba7914dce5b718cea792ac0c7350d2f8d00bd2ef1cece",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.3.00.tar.gz",
    )
    version(
        "3.2.01",
        sha256="c486e5cac19e354a517498c362838619435734d64b44f44ce909b0531c21d95c",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.2.01.tar.gz",
    )
    version(
        "3.2.00",
        sha256="8ac20ee28ae7813ce1bda461918800ad57fdbac2af86ef5d1ba74e83e10956de",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.2.00.tar.gz",
    )
    version(
        "3.1.00",
        sha256="27fea241ae92f41bd5b070b1a590ba3a56a06aca750207a98bea2f64a4a40c89",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.1.00.tar.gz",
    )
    version(
        "3.0.00",
        sha256="e4b832aed3f8e785de24298f312af71217a26067aea2de51531e8c1e597ef0e6",
        url="https://github.com/kokkos/kokkos-kernels/archive/3.0.00.tar.gz",
    )

    variant("shared", default=True, description="Build shared libraries")
    variant(
        "execspace_cuda",
        default=False,
        description="Whether to pre instantiate kernels for the execution space Kokkos::Cuda",
    )
    variant(
        "execspace_openmp",
        default=False,
        description="Whether to pre instantiate kernels for the execution space "
        "Kokkos::Experimental::OpenMPTarget",
    )
    variant(
        "execspace_threads",
        default=False,
        description="Whether to pre instantiate kernels for the execution space Kokkos::Threads",
    )
    variant(
        "execspace_serial",
        default=False,
        description="Whether to pre instantiate kernels for the execution space Kokkos::Serial",
    )
    variant(
        "memspace_cudauvmspace",
        default=False,
        description="Whether to pre instantiate kernels for the memory space Kokkos::CudaUVMSpace",
    )
    variant(
        "memspace_cudaspace",
        default=False,
        description="Whether to pre instantiate kernels for the memory space Kokkos::CudaSpace",
    )
    variant("serial", default=False, description="Enable serial backend")
    variant("openmp", default=False, description="Enable OpenMP backend")
    variant("threads", default=False, description="Enable C++ threads backend")
    variant(
        "ordinals", default="int", values=["int", "int64_t"], multi=True, description="Ordinals"
    )
    variant(
        "offsets",
        default="int,size_t",
        values=["int", "size_t"],
        multi=True,
        description="Offsets",
    )
    variant("layouts", default="left", values=["left", "right"], description="Layouts")
    variant(
        "scalars",
        default="double",
        values=["float", "double", "complex_float", "complex_double"],
        multi=True,
        description="Scalars",
    )

    depends_on("cxx", type="build")
    depends_on("kokkos")
    depends_on("kokkos@master", when="@master")
    depends_on("kokkos@develop", when="@develop")
    depends_on("kokkos@4.5.01", when="@4.5.01")
    depends_on("kokkos@4.5.00", when="@4.5.00")
    depends_on("kokkos@4.4.01", when="@4.4.01")
    depends_on("kokkos@4.4.00", when="@4.4.00")
    depends_on("kokkos@4.3.01", when="@4.3.01")
    depends_on("kokkos@4.3.00", when="@4.3.00")
    depends_on("kokkos@4.2.01", when="@4.2.01")
    depends_on("kokkos@4.2.00", when="@4.2.00")
    depends_on("kokkos@4.1.00", when="@4.1.00")
    depends_on("kokkos@4.0.01", when="@4.0.01")
    depends_on("kokkos@4.0.00", when="@4.0.00")
    depends_on("kokkos@3.7.01", when="@3.7.01")
    depends_on("kokkos@3.7.00", when="@3.7.00")
    depends_on("kokkos@3.6.01", when="@3.6.01")
    depends_on("kokkos@3.6.00", when="@3.6.00")
    depends_on("kokkos@3.5.00", when="@3.5.00")
    depends_on("kokkos@3.4.01", when="@3.4.01")
    depends_on("kokkos@3.4.00", when="@3.4.00")
    depends_on("kokkos@3.3.01", when="@3.3.01")
    depends_on("kokkos@3.3.00", when="@3.3.00")
    depends_on("kokkos@3.2.01", when="@3.2.01")
    depends_on("kokkos@3.2.00", when="@3.2.00")
    depends_on("kokkos@3.1.00", when="@3.1.00")
    depends_on("kokkos@3.0.00", when="@3.0.00")
    depends_on("kokkos+cuda", when="+execspace_cuda")
    depends_on("kokkos+openmp", when="+execspace_openmp")
    depends_on("kokkos+threads", when="+execspace_threads")
    depends_on("kokkos+serial", when="+execspace_serial")
    depends_on("kokkos+cuda", when="+memspace_cudauvmspace")
    depends_on("kokkos+cuda", when="+memspace_cudaspace")
    depends_on("kokkos+serial", when="+serial")
    depends_on("kokkos+cuda", when="+cuda")
    depends_on("kokkos+openmp", when="+openmp")
    depends_on("kokkos+threads", when="+threads")
    depends_on("kokkos+cuda_lambda", when="@4.0.00:+cuda")
    depends_on("cmake@3.16:", type="build")

    tpls = {
        # variant name   #deflt   #spack name  #root var name  #supporting versions  #docstring
        "blas": (False, "blas", "BLAS", "@3.0.00:", "Link to system BLAS"),
        "lapack": (False, "lapack", "LAPACK", "@3.0.00:", "Link to system LAPACK"),
        "mkl": (False, "mkl", "MKL", "@3.0.00:", "Link to system MKL"),
        "cublas": (False, "cuda", None, "@3.0.00:", "Link to CUDA BLAS library"),
        "cusparse": (False, "cuda", None, "@3.0.00:", "Link to CUDA sparse library"),
        "superlu": (False, "superlu", "SUPERLU", "@3.1.00:", "Link to SuperLU library"),
        "cblas": (False, "cblas", "CBLAS", "@3.1.00:", "Link to CBLAS library"),
        "lapacke": (False, "clapack", "LAPACKE", "@3.1.00:", "Link to LAPACKE library"),
        "rocblas": (False, "rocblas", "ROCBLAS", "@3.6.00:", "Link to AMD BLAS library"),
        "rocsparse": (False, "rocsparse", "ROCSPARSE", "@3.6.00:", "Link to AMD sparse library"),
        "cusolver": (False, "cuda", None, "@4.3.00:", "Link to CUDA solver library"),
        "rocsolver": (False, "rocsolver", "ROCSOLVER", "@4.3.00:", "Link to AMD solver library"),
    }

    for tpl in tpls:
        deflt_bool, spackname, rootname, condition, descr = tpls[tpl]
        variant(tpl, default=deflt_bool, when=f"{condition}", description=descr)
        depends_on(spackname, when=f"+{tpl}")

    # sanity check
    sanity_check_is_file = [join_path("include", "KokkosKernels_config.h")]
    sanity_check_is_dir = ["include"]

    def cmake_args(self):
        spec = self.spec
        options = [
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_CUDA", "execspace_cuda"),
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_OPENMP", "execspace_openmp"),
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_THREADS", "execspace_threads"),
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_SERIAL", "execspace_serial"),
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_SERIAL", "execspace_serial"),
            self.define_from_variant(
                "KokkosKernels_INST_MEMSPACE_CUDAUVMSPACE", "memspace_cudauvmspace"
            ),
            self.define_from_variant(
                "KokkosKernels_INST_MEMSPACE_CUDASPACE", "memspace_cudaspace"
            ),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        if spec.satisfies("+diy"):
            options.append(self.define("Spack_WORKAROUND", True))

        options.append(self.define("Kokkos_ROOT", spec["kokkos"].prefix))
        if spec.satisfies("^kokkos+rocm"):
            options.append(self.define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
        else:
            options.append(self.define("CMAKE_CXX_COMPILER", self["kokkos"].kokkos_cxx))

        if self.run_tests:
            options.append(self.define("KokkosKernels_ENABLE_TESTS", True))

        for tpl in self.tpls:
            dflt, spackname, rootname, condition, descr = self.tpls[tpl]
            if spec.satisfies(f"+{tpl}"):
                options.append(self.define(f"KokkosKernels_ENABLE_TPL_{tpl.upper()}", True))
                if rootname:
                    options.append(self.define(f"{rootname}_ROOT", spec[spackname].prefix))
                else:
                    pass

        for val in spec.variants["ordinals"].value:
            options.append(self.define(f"KokkosKernels_INST_ORDINAL_{val.upper()}", True))
        for val in spec.variants["offsets"].value:
            options.append(self.define(f"KokkosKernels_INST_OFFSET_{val.upper()}", True))
        for val in spec.variants["scalars"].value:
            options.append(self.define(f"KokkosKernels_INST_{val.upper()}", True))
        layout_value = spec.variants["layouts"].value
        options.append(self.define(f"KokkosKernels_INST_LAYOUT{layout_value.upper()}", True))

        return options
