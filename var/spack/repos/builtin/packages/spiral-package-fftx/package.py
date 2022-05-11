# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class SpiralPackageFftx(Package):
    """This is the SPIRAL package for FFTX:  FFTX is the exascale follow-on to
    the FFTW open source discrete FFT package for executing the Fast Fourier
    Transform as well as higher-level operations composed of linear operations
    combined with DFT transforms."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-package-fftx/archive/refs/tags/1.0.0.tar.gz"
    git      = "https://github.com/spiral-software/spiral-package-fftx.git"

    maintainers = ['spiralgen']
    extends('spiral-software')

    version('develop', branch='develop')
    version('main',    branch='main')
    version('1.1.1',   sha256='99ec7fab9274d378524b4933917fae23f9590255518c7a124cb46bd5e8d9af37')
    version('1.1.0',   sha256='979d7e59fc39e7e5423bce64628cea467079667d75ce885febee7c42fa7164aa')
    version('1.0.0',   sha256='9ed352049fcaab31a1a898149d16438c95a1656a2d24df6dee14e3b61efacb5c')

    # FFTX package is an extension for Spiral (spec: spiral-software).  Spiral finds
    # extensions in the "namespaces/packages" folder.  Install the tree in a similarly
    # named folder so that when activated it'll get symlinked to the correct place.

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, 'namespaces', 'packages', 'fftx')
        install_tree('.', spiral_pkgs)
