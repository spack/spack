# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Resolve(CMakePackage, CudaPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://code.ornl.gov/ecpcitest/exasgd/resolve"
    url = "https://code.ornl.gov/ecpcitest/exasgd/resolve.git"
    maintainers("cameronrutherford", "pelesh", "ryandanehy")

    # version("0.1.0", submodules=False, branch=develop)
    # version("develop", submodules=False, branch=develop)

    variant("klu", default=True, description="Use KLU, AMD and COLAMD Libraries from SuiteSparse")

    depends_on("suite-sparse", when="+klu")

    # # suite-sparse is not a CudaPackage so we cannot specify cuda_arch
    # # for other dependencies we could
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

        return args

