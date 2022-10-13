# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioNvcomp(CMakePackage, CudaPackage):
    """LibPressio Bindings for NVCOMP"""

    homepage = "https://github.com/robertu94/libpressio-nvcomp"
    url = "https://github.com/robertu94/libpressio-nvcomp/archive/refs/tags/0.0.3.tar.gz"
    git = "https://github.com/robertu94/libpressio-nvcomp"

    maintainers = ["robertu94"]

    version("0.0.3", sha256="21409d34f9281bfd7b83b74f5f8fc6d34794f3161391405538c060fb59534597")

    depends_on("nvcomp@2.2.0:")
    depends_on("libpressio@0.88.0:")

    conflicts("~cuda")
    conflicts("cuda_arch=none", when="+cuda")

    def cmake_args(self):
        cuda_arch = self.spec.variants["cuda_arch"].value
        args = [
            ("-DCMAKE_CUDA_ARCHITECTURES=%s" % cuda_arch)
        ]
        return args
