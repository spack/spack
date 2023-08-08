# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# contribute
from spack.package import *


class Wsclean(CMakePackage):
    """
    WSClean (w-stacking clean) is a fast generic widefield imager. It uses the w-stacking algorithm
    and can make use of the w-snapshot algorithm. As of Feb 2014, it is 2-12 times faster than CASA's
    w-projection, depending on the array configuration. It supports full-sky imaging and proper beam
    correction for homogeneous dipole arrays such as the MWA.
    WSClean allows Hogbom and Cotton-Schwab cleaning and has wideband, multiscale, compressed
    sensing and joined-polarization deconvolution modes. All operations are performed on the CPU.
    """

    homepage = "https://wsclean.readthedocs.io/en/latest/"
    git = "https://gitlab.com/aroffringa/wsclean.git"

    version("master", branch="master")
    version("3.1", commit="ea18d0139e35050d58b2758cf5015539f3e2d870")
    version("3.0.1", commit="1a4e5928689b23d3034549c2541829427d91fa8e")
    version("3.0", commit="9ee587c576caad779dc127bb3f83858513679333")
    version("2.10.1", commit="6567e4891467c23a27391b49273b3fbb94c45831")
    version("2.10", commit="7b82d8c19ccb09cf2d7872a338d8266d09dd0481")

    variant(
        "idg",
        default=True,
        description="To enable Image Domain Gridder (a fast GPU-enabled gridder) for version >=3",
    )
    variant("everybeam", default=False, description="To apply primary beams for version >=3")
    variant("mpi", default=False, description="To enable distributed mode")

    depends_on("chgcentre", type="build")
    depends_on("casacore")
    depends_on("fftw-api@3")
    depends_on("gsl")
    depends_on("cfitsio")
    depends_on("hdf5 +cxx ~mpi api=v110", when="@2.10.1")
    depends_on("boost")
    depends_on("idg@0.8.1", when="@3.0 +idg")
    depends_on("idg@1.0.0", when="@3.1 +idg")
    depends_on("everybeam@0.2.0", when="@3.0 +everybeam")
    depends_on("everybeam@0.3.1", when="@3.1 +everybeam")
    depends_on("mpi", when="+mpi")
    depends_on("blas", when="@3.0:")
    depends_on("doxygen", when="@3.0:")
    depends_on("python", when="@3.0:")
    patch("cmake.patch", when="@3.0:")
    patch("mpi1.patch", when="@3.0:")
    patch("mpi2.patch", when="@3.0:")
    patch("cmake.for.v2.0.patch", when="@2.10.1")

    def cmake_args(self):
        args = []
        spec = self.spec
        args.append(self.define_from_variant("USE_MPI", "mpi"))

        return args
