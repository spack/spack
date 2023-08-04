# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NimrodAai(CMakePackage):
    """NIMROD infrastructure for FEM evaluation, integration and linear algebra
    solves with device accelerated computing through OpenACC and abstract types
    enabled by modern Fortran.
    """

    homepage = "https://gitlab.com/NIMRODteam/nimrod-abstract"
    url = (
        "https://gitlab.com/NIMRODteam/nimrod-abstract/-/archive/23.6/nimrod-abstract-23.6.tar.gz"
    )
    git = "https://gitlab.com/NIMRODteam/nimrod-abstract.git"

    maintainers("jacobrking")

    version("main", branch="main")
    version("23.6", sha256="1794b89a5a64ff2b3c548818b90d17eef85d819ba4f63a76c41a682d5b76c14f")

    variant("debug", default=False)
    variant("openacc", default=False)
    variant("openacc_autocompare", default=False)
    variant("enable_shared", default=True)
    variant("mpi", default=False)
    variant("time_level1", default=False)
    variant("time_level2", default=False)
    variant("nvtx_profile", default=False)
    variant("openacc_cc", default="native")
    variant("trap_fp_exceptions", default=False)

    depends_on("cmake", type="build")
    depends_on("hdf5+fortran", type="build")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        args = [
            self.define_from_variant("DEBUG", "debug"),
            self.define_from_variant("ENABLE_OPENACC", "openacc"),
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("ENABLE_SHARED", "enable_shared"),
            self.define_from_variant("NVTX_PROFILE", "nvtx_profile"),
            self.define_from_variant("TIME_LEVEL1", "time_level1"),
            self.define_from_variant("TIME_LEVEL2", "time_level2"),
            self.define_from_variant("TRAP_FP_EXCEPTIONS", "trap_fp_exceptions"),
        ]
        if "+openacc" in self.spec:
            addl_args = [
                self.define_from_variant("ENABLE_OPENACC_AUTOCOMPARE", "openacc_autocompare"),
                self.define_from_variant("OPENACC_CC", "openacc_cc"),
            ]
            args.append(addl_args)
        return args
