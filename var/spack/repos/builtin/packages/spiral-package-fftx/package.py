# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SpiralPackageFftx(Package):
    """This is the SPIRAL package for FFTX:  FFTX is the exascale follow-on to
    the FFTW open source discrete FFT package for executing the Fast Fourier
    Transform as well as higher-level operations composed of linear operations
    combined with DFT transforms."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-package-fftx/archive/1.0.0.tar.gz"
    git      = "https://github.com/spiral-software/spiral-package-fftx.git"

    maintainers = ['spiralgen']
    extends('spiral-software')

    version('develop', branch='develop')
    version('main',    branch='main')
    version('1.0.0',   sha256='9ed352049fcaab31a1a898149d16438c95a1656a2d24df6dee14e3b61efacb5c')

    # FFTX package is an extension for Spiral (spec: spiral-software).  Extensions
    # packages for Spiral are intended to be installed in the spiral-software prefix,
    # in the "namespaces/packages" folder.  Install the tree in that folder under the
    # name 'fftx'.

    def install(self, spec, prefix):
        spec = self.spec
        spiral_locn = '{0}'.format(spec['spiral-software'].prefix)
        spiral_pkgs = join_path(spiral_locn, 'namespaces', 'packages', 'fftx')
        install_tree('.', spiral_pkgs)
