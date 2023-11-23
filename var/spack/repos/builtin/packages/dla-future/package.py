# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DlaFuture(CMakePackage, CudaPackage, ROCmPackage):
    """DLA-Future library: Distributed Linear Algebra with Future"""

    homepage = "https://github.com/eth-cscs/DLA-Future"
    url = "https://github.com/eth-cscs/DLA-Future/archive/v0.0.0.tar.gz"
    git = "https://github.com/eth-cscs/DLA-Future.git"
    maintainers = ["rasolca", "albestro", "msimberg", "aurianer"]

    license("BSD-3-Clause")

    version("0.3.1", sha256="350a7fd216790182aa52639a3d574990a9d57843e02b92d87b854912f4812bfe")
    version("0.3.0", sha256="9887ac0b466ca03d704a8738bc89e68550ed33509578c576390e98e76b64911b")
    version("0.2.1", sha256="4c2669d58f041304bd618a9d69d9879a42e6366612c2fc932df3894d0326b7fe")
    version("0.2.0", sha256="da73cbd1b88287c86d84b1045a05406b742be924e65c52588bbff200abd81a10")
    version("0.1.0", sha256="f7ffcde22edabb3dc24a624e2888f98829ee526da384cd752b2b271c731ca9b1")
    version("master", branch="master")

    variant("shared", default=True, description="Build shared libraries.")

    variant(
        "hdf5",
        default=False,
        when="@0.2.0:",
        description="HDF5 support for dealing with matrices on disk.",
    )

    variant("doc", default=False, description="Build documentation.")

    variant("miniapps", default=False, description="Build miniapps.")

    variant(
        "scalapack",
        default=False,
        when="@0.2.0:",
        description="Build C API compatible with ScaLAPACK",
    )

    depends_on("cmake@3.22:", type="build")
    depends_on("doxygen", type="build", when="+doc")
    depends_on("mpi")

    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack", when="+scalapack")
    depends_on("blaspp@2022.05.00:")
    depends_on("lapackpp@2022.05.00:")

    depends_on("umpire~examples")
    depends_on("umpire~cuda", when="~cuda")
    depends_on("umpire~rocm", when="~rocm")
    depends_on("umpire+cuda~shared", when="+cuda")
    depends_on("umpire+rocm~shared", when="+rocm")
    depends_on("umpire@4.1.0:")

    depends_on("pika@0.15.1:", when="@0.1")
    depends_on("pika@0.16:", when="@0.2.0")
    depends_on("pika@0.17:", when="@0.2.1")
    depends_on("pika@0.18:", when="@0.3.0:")
    depends_on("pika-algorithms@0.1:", when="@:0.2")
    depends_on("pika +mpi")
    depends_on("pika +cuda", when="+cuda")
    depends_on("pika +rocm", when="+rocm")

    conflicts("^pika cxxstd=20", when="+cuda")

    depends_on("whip +cuda", when="+cuda")
    depends_on("whip +rocm", when="+rocm")

    depends_on("rocblas", when="+rocm")
    depends_on("rocprim", when="+rocm")
    depends_on("rocsolver", when="+rocm")
    depends_on("rocthrust", when="+rocm")

    depends_on("hdf5 +cxx+mpi+threadsafe+shared", when="+hdf5")

    conflicts("+cuda", when="+rocm")

    with when("+rocm"):
        for val in ROCmPackage.amdgpu_targets:
            depends_on("pika amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val))
            depends_on(
                "rocsolver amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val)
            )
            depends_on(
                "rocblas amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val)
            )
            depends_on(
                "rocprim amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val)
            )
            depends_on(
                "rocthrust amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val)
            )
            depends_on("whip amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val))
            depends_on(
                "umpire amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val)
            )

    with when("+cuda"):
        for val in CudaPackage.cuda_arch_values:
            depends_on("pika cuda_arch={0}".format(val), when="cuda_arch={0}".format(val))
            depends_on("umpire cuda_arch={0}".format(val), when="cuda_arch={0}".format(val))

    def cmake_args(self):
        spec = self.spec
        args = []

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        # BLAS/LAPACK
        if self.spec["lapack"].name in INTEL_MATH_LIBRARIES:
            vmap = {
                "none": "seq",
                "openmp": "omp",
                "tbb": "tbb",
            }  # Map MKL variants to LAPACK target name
            mkl_threads = vmap[spec["intel-mkl"].variants["threads"].value]
            # TODO: Generalise for intel-oneapi-mkl
            args += [
                self.define("DLAF_WITH_MKL", True),
                self.define("MKL_LAPACK_TARGET", f"mkl::mkl_intel_32bit_{mkl_threads}_dyn"),
            ]
            if "+scalapack" in spec:
                if (
                    "^mpich" in spec
                    or "^cray-mpich" in spec
                    or "^intel-mpi" in spec
                    or "^mvapich" in spec
                    or "^mvapich2" in spec
                ):
                    mkl_mpi = "mpich"
                elif "^openmpi" in spec:
                    mkl_mpi = "ompi"
                args.append(
                    self.define(
                        "MKL_SCALAPACK_TARGET",
                        f"mkl::scalapack_{mkl_mpi}_intel_32bit_{mkl_threads}_dyn",
                    )
                )
        else:
            args.append(self.define("DLAF_WITH_MKL", False))
            args.append(
                self.define(
                    "LAPACK_LIBRARY",
                    " ".join([spec[dep].libs.ld_flags for dep in ["blas", "lapack"]]),
                )
            )
            if "+scalapack" in spec:
                args.append(self.define("SCALAPACK_LIBRARY", spec["scalapack"].libs.ld_flags))

        args.append(self.define_from_variant("DLAF_WITH_SCALAPACK", "scalapack"))

        # CUDA/HIP
        args.append(self.define_from_variant("DLAF_WITH_CUDA", "cuda"))
        args.append(self.define_from_variant("DLAF_WITH_HIP", "rocm"))
        if "+rocm" in spec:
            archs = self.spec.variants["amdgpu_target"].value
            if "none" not in archs:
                arch_str = ";".join(archs)
                args.append(self.define("CMAKE_HIP_ARCHITECTURES", arch_str))
        if "+cuda" in spec:
            archs = self.spec.variants["cuda_arch"].value
            if "none" not in archs:
                arch_str = ";".join(archs)
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", arch_str))

        # HDF5 support
        args.append(self.define_from_variant("DLAF_WITH_HDF5", "hdf5"))

        # DOC
        args.append(self.define_from_variant("DLAF_BUILD_DOC", "doc"))

        # TEST
        args.append(self.define("DLAF_BUILD_TESTING", self.run_tests))

        # MINIAPPS
        args.append(self.define_from_variant("DLAF_BUILD_MINIAPPS", "miniapps"))

        return args
