# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cryoef(MakefilePackage):
    """An open-source software package for robust analysis of the orientation distribution
    of cryoelectron microscopy data."""

    homepage = "https://www.mrc-lmb.cam.ac.uk/crusso/cryoEF"
    url = "https://www.mrc-lmb.cam.ac.uk/crusso/cryoEF/cryoEF_v1.1.0.tar.gz"

    version("1.1.0", sha256="655ed8543a0226754bdeb6e0dd4efc0467f15dc4c9c963c44ef7b8d3d0e41b62")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fftw-api@3")

    def patch(self):
        filter_file(
            "-lfftw3", f"-lfftw3 {self.spec['fftw-api'].libs.ld_flags} -no-pie", "Makefile"
        )

    def install(self, spec, prefix):
        install_tree("TestData", prefix.TestData)
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install("PlotOD.py", prefix.bin)
