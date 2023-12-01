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

    variant("ilp64", default=False, description="Force 64-bit Fortran native integers")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )

    conflicts("%gcc@:7")
    conflicts("%clang@:13")

    conflicts("threads=openmp", when="%clang")

    @property
    def lapack_headers(self):
        return find_all_headers(self.spec.prefix.include)

    @property
    def lapack_libs(self):
        spec = self.spec

        if "+ilp64" in spec:
          int_type = "ilp64"
        else:
          int_type = "lp64"

        if spec.satisfies("threads=openmp"):
          threading_type="gomp"
        else:
          # threads=none
          threading_type = "seq"

        name = ["libnvpl_lapack_core", f"libnvpl_lapack_{int_type}_{threading_type}"]

        return find_libraries(name, spec.prefix.lib, shared=True, recursive=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)
