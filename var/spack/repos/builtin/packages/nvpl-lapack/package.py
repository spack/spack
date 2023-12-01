# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvplLapack(Package):
    """
    NVPL LAPACK (NVIDIA Performance Libraries LAPACK) is part of NVIDIA Performance Libraries
    that provides standard Fortran 90 LAPACK APIs.
    """

    homepage = "https://docs.nvidia.com/nvpl/_static/lapack/index.html"
    url = ("https://developer.download.nvidia.com/compute/nvpl/redist"
           "/nvpl_lapack/linux-sbsa/nvpl_lapack-linux-sbsa-0.2.0.1-archive.tar.xz")

    maintainers("albestro", "rasolca")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("UNKNOWN")

    version("0.1.0", sha256="7054f775b18916ee662c94ad7682ace53debbe8ee36fa926000fe412961edb0b")

    provides("lapack")

    # TODO add compiler requirements

    def install(self, spec, prefix):
        install_tree(".", prefix)
