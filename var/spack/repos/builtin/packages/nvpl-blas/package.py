# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvplBlas(Package):
    """
    NVPL BLAS (NVIDIA Performance Libraries BLAS) is part of NVIDIA Performance Libraries
    that provides standard Fortran 77 BLAS APIs as well as C (CBLAS).
    """

    homepage = "https://docs.nvidia.com/nvpl/_static/blas/index.html"
    url = ("https://developer.download.nvidia.com/compute/nvpl/redist"
           "/nvpl_blas/linux-sbsa/nvpl_blas-linux-sbsa-0.1.0-archive.tar.xz")

    maintainers("albestro", "rasolca")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("UNKNOWN")

    version("0.1.0", sha256="4ccc894593cbcbfaa1a4f3c54505982691971667acf191c9ab0f4252a37c8063")

    provides("blas")

    # TODO add compiler requirements

    def install(self, spec, prefix):
        install_tree(".", prefix)
