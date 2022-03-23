# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
    version('1.1.0-release', sha256='a8f30cd88231deabf575b7410fa646049528d1fbbc08534d43711caf6ae10b4e')
    version('1.0.0',   sha256='888ca01aa8fd5df80d6ae1bd64eb1b1e70240b6a36bc3437eb48f5a4b59c2d07')

    # SIMT package is an extension for Spiral (spec: spiral-software).  Spiral finds
    # extensions in the "namespaces/packages" folder.  Install the tree in a similarly
    # named folder so that when activated it'll get symlinked to the correct place.

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, 'namespaces', 'packages', 'simt')
        install_tree('.', spiral_pkgs)
