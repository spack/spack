# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SpiralPackageSimt(Package):
    """This is the SPIRAL package for SIMT:  SIMT, single instruction multiple
    threads, is used to generate code for GPUs and multi-threading aplications."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-package-simt/archive/1.0.0.tar.gz"
    git      = "https://github.com/spiral-software/spiral-package-simt.git"

    maintainers = ['spiralgen']
    extends('spiral-software')

    version('develop', branch='develop')
    version('main',    branch='main')
    version('1.0.0',   sha256='888ca01aa8fd5df80d6ae1bd64eb1b1e70240b6a36bc3437eb48f5a4b59c2d07')

    # SIMT package is an extension for Spiral (spec: spiral-software).  Extensions
    # packages for Spiral are intended to be installed in the spiral-software prefix,
    # in the "namespaces/packages" folder.  Install the tree in that folder under the
    # name 'simt'.

    def install(self, spec, prefix):
        spec = self.spec
        spiral_locn = '{0}'.format(spec['spiral-software'].prefix)
        spiral_pkgs = join_path(spiral_locn, 'namespaces', 'packages', 'simt')
        install_tree('.', spiral_pkgs)
