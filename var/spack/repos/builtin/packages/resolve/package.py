# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Resolve(CMakePackage, CudaPackage):
    """ReSolve is a library of GPU-resident sparse linear solvers. It contains iterative and direct
    solvers designed to run on NVIDIA and AMD GPUs, as well as CPU devices."""

    homepage = "https://github.com/ORNL/ReSolve"
    url = "https://github.com/ORNL/ReSolve.git"
    maintainers("cameronrutherford", "pelesh", "ryandanehy", "kswirydo")

    # version("1.0.0", submodules=False, branch=develop)
    # version("develop", submodules=False, branch=develop)

    variant("klu", default=True, description="Use KLU, AMD and COLAMD Libraries from SuiteSparse")

    depends_on("suite-sparse", when="+klu")

    # # We do not use CUDA modules of suite-sparse so we don't specify cuda_arch
    # # For other dependencies we could
    # for arch in CudaPackage.cuda_arch_values:
    #   cuda_dep = "+cuda cuda_arch={0}".format(arch)
    #   # depends_on("suite-sparse {0}".format(cuda_dep), when=cuda_dep)

    def cmake_args(self):
        args = []
        spec = self.spec

        args.extend(
            [self.define("RESOLVE_USE_KLU", "klu"), self.define("RESOLVE_TEST_WITH_BSUB", False)]
        )

        # This will error if no arch is provided, which is ok
        # Perhaps there is a more graceful way to handle this:
        # if not spec.satisfies("cuda_arch=none"):
        # I don't think it is a good idea to build without cuda_arch when +cuda?
        if "+cuda" in spec:
            cuda_arch_list = spec.variants["cuda_arch"].value
            if cuda_arch_list[0] != "none":
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", cuda_arch_list))
            else:
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", "70;75;80"))
        else:
            args.append(self.define("RESOLVE_USE_CUDA", False))
            args.append(self.define("RESOLVE_USE_GPU", False))

        return args
