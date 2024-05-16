# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zerosum(CMakePackage):
    """Utility for monitoring process, thread, OS and HW resources,
    including GPU utilization.
    """

    homepage = "https://github.com/UO-OACISS/zerosum"
    url = "https://github.com/UO-OACISS/zerosum.git"
    git = "https://github.com/UO-OACISS/zerosum"

    maintainers("khuck", "wspear", "sameershende")

    license("MIT", checked_by="khuck")

    # version("1.2.3", md5="0123456789abcdef0123456789abcdef")
    version("main", branch="main")

    variant("perfstubs", default=True, description="Enable PerfStubs support")
    variant("hwloc", default=True, description="Enable HWLOC support")
    variant("mpi", default=True, description="Enable MPI support")
    variant("cuda", default=False, description="Enable CUDA support")
    variant("hip", default=False, description="Enable HIP support")
    variant("sycl", default=False, description="Enable SYCL support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("ompt", default=True, description="Enable OpenMP Tools support")

    depends_on("cmake", type="build")
    depends_on("hwloc", when="+hwloc")
    depends_on("mpi", when="+mpi")
    depends_on("rocm-smi-lib", when="+hip")
    depends_on("cuda", when="+cuda")
    depends_on("hip", when="+hip")
    depends_on("sycl", when="+sycl")

    conflicts("+ompt", when="%gcc")

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("ZeroSum_WITH_PerfStubs", "perfstubs"))
        args.append(self.define_from_variant("ZeroSum_WITH_HWLOC", "hwloc"))
        args.append(self.define_from_variant("ZeroSum_WITH_MPI", "mpi"))
        args.append(self.define_from_variant("ZeroSum_WITH_CUDA", "cuda"))
        args.append(self.define_from_variant("ZeroSum_WITH_HIP", "hip"))
        args.append(self.define_from_variant("ZeroSum_WITH_SYCL", "sycl"))
        args.append(self.define_from_variant("ZeroSum_WITH_OPENMP", "openmp"))
        args.append(self.define_from_variant("ZeroSum_WITH_OMPT", "ompt"))
        if "+cuda" in self.spec:
            args.append("-DCUDAToolkit_ROOT={0}".format(spec["cuda"].prefix))
        if "+hip" in self.spec:
            args.append("-DROCM_ROOT={0}".format(spec["hip"].prefix))

        return args
