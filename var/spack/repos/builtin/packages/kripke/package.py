# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kripke(CMakePackage, CudaPackage, ROCmPackage):
    """Kripke is a simple, scalable, 3D Sn deterministic particle
    transport proxy/mini app.
    """

    homepage = "https://computing.llnl.gov/projects/co-design/kripke"
    git = "https://github.com/LLNL/Kripke.git"

    tags = ["proxy-app"]

    maintainers("vsrana01")

    version("develop", branch="develop", submodules=False)
    version("1.2.4", submodules=False, tag="v1.2.4")
    version("1.2.3", submodules=True, tag="v1.2.3")
    version("1.2.2", submodules=True, tag="v1.2.2-CORAL2")
    version("1.2.1", submodules=True, tag="v1.2.1-CORAL2")
    version("1.2.0", submodules=True, tag="v1.2.0-CORAL2")

    variant("mpi", default=True, description="Build with MPI.")
    variant("openmp", default=False, description="Build with OpenMP enabled.")
    variant("caliper", default=False, description="Build with Caliper support enabled.")

    depends_on("mpi", when="+mpi")
    depends_on("blt")
    depends_on("cmake")
    depends_on("caliper", when="+caliper")
    depends_on("chai~examples+raja")
    depends_on("raja~exercises~examples")
    depends_on("umpire~examples")

    def cmake_args(self):
        spec = self.spec
        args = []

        args.extend(
            [
                "-DCAMP_DIR=%s" % self.spec["camp"].prefix,
                "-DBLT_SOURCE_DIR=%s" % self.spec["blt"].prefix,
                "-Dumpire_DIR=%s" % self.spec["umpire"].prefix,
                "-DRAJA_DIR=%s" % self.spec["raja"].prefix,
                "-Dchai_DIR=%s" % self.spec["chai"].prefix,
                "-DENABLE_CHAI=ON",
            ]
        )

        if "+caliper" in spec:
            args.append("-DENABLE_CALIPER=ON")

        if "+mpi" in spec:
            args.append("-DENABLE_MPI=ON")
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx))

        if "+rocm" in spec:
            # Set up the hip macros needed by the build
            args.append("-DENABLE_HIP=ON")
            args.append("-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix))
            rocm_archs = spec.variants["amdgpu_target"].value
            if "none" not in rocm_archs:
                args.append("-DHIP_HIPCC_FLAGS=--amdgpu-target={0}".format(",".join(rocm_archs)))
                args.append("-DCMAKE_HIP_ARCHITECTURES={0}".format(rocm_archs))
        else:
            # Ensure build with hip is disabled
            args.append("-DENABLE_HIP=OFF")

        if "+cuda" in spec:
            args.append("-DENABLE_CUDA=ON")
            args.append(self.define("CMAKE_CUDA_HOST_COMPILER", self.spec["mpi"].mpicxx))
            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                args.append("-DCUDA_ARCH={0}".format(cuda_arch[0]))
                args.append("-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch[0]))
                args.append(
                    "-DCMAKE_CUDA_FLAGS=--expt-extended-lambda -I%s -I=%s"
                    % (self.spec["cub"].prefix.include, self.spec["mpi"].prefix.include)
                )
        else:
            args.append("-DENABLE_CUDA=OFF")

        return args

    def install(self, spec, prefix):
        # Kripke does not provide install target, so we have to copy
        # things into place.
        mkdirp(prefix.bin)
        install(join_path(self.build_directory, "kripke.exe"), prefix.bin)
