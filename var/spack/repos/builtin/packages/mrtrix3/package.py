# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mrtrix3(Package):
    """MRtrix provides a set of tools to perform various advanced diffusion MRI
    analyses, including constrained spherical deconvolution (CSD),
    probabilistic tractography, track-density imaging, and apparent fibre
    density."""

    homepage = "https://www.mrtrix.org/"
    url = "https://github.com/MRtrix3/mrtrix3/archive/refs/tags/3.0.3.tar.gz"
    git = "https://github.com/MRtrix3/mrtrix3.git"

    version(
        "3.0.3",
        sha256="6ec7d5a567d8d7338e85575a74565189a26ec8971cbe8fb24a49befbc446542e",
        preferred=True,
    )
    version("2017-09-25", commit="72aca89e3d38c9d9e0c47104d0fb5bd2cbdb536d")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("glu")
    depends_on("qt+opengl@4.7:")
    depends_on("eigen")
    depends_on("zlib-api")
    depends_on("libtiff")
    depends_on("fftw")

    conflicts("%gcc@7:", when="@2017-09-25")  # MRtrix3/mrtrix3#1041

    def install(self, spec, prefix):
        configure = Executable("./configure")
        build = Executable("./build")
        configure()
        build()
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
