# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpiralPackageFftx(Package):
    """This is the SPIRAL package for FFTX:  FFTX is the exascale follow-on to
    the FFTW open source discrete FFT package for executing the Fast Fourier
    Transform as well as higher-level operations composed of linear operations
    combined with DFT transforms."""

    homepage = "https://spiralgen.com"
    url = "https://github.com/spiral-software/spiral-package-fftx/archive/refs/tags/1.2.1.tar.gz"
    git = "https://github.com/spiral-software/spiral-package-fftx.git"

    maintainers("spiralgen")
    extends("spiral-software")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.2.1", sha256="3f15aa5949c1b09eb59257cf1c5f6fcddc6e46f77ae9d5fce8acd8b9f99ce941")
    version("1.1.1", sha256="99ec7fab9274d378524b4933917fae23f9590255518c7a124cb46bd5e8d9af37")

    # FFTX package is an extension for Spiral (spec: spiral-software).  Spiral finds
    # extensions in the "namespaces/packages" folder.  Install the tree in a similarly
    # named folder so that when activated it'll get symlinked to the correct place.

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, "namespaces", "packages", "fftx")
        install_tree(".", spiral_pkgs)
