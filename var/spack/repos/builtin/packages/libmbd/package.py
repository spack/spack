# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmbd(CMakePackage):
    """Implementation of the many-body dispersion (MBD) method
    (https://doi.org/10.1063/1.4865104).
    """

    homepage = "https://github.com/libmbd/libmbd"
    url = "https://github.com/libmbd/libmbd/releases/download/0.12.6/libmbd-0.12.6.tar.gz"
    git = "https://github.com/libmbd/libmbd"

    version("master", branch="master", nocache=True)
    version("0.12.6", sha256="209ead036690eac9e308a0305145c6f88bbfb583a18f0d2e4632335833d22b1a")
    # version("0.12.6", tag="0.12.6")

    variant("scalapack", default=False)

    depends_on("cmake@3.14:", type="build")
    depends_on("blas", type="link")
    depends_on("lapack", type="link")
    depends_on("scalapack", when="+scalapack", type="link")

    def cmake_args(self):
        args = [self.define_from_variant("ENABLE_SCALAPACK_MPI", variant="scalapack")]
        return args
