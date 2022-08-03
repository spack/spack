# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpiralPackageMpi(Package):
    """This is the SPIRAL package for MPI."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-package-mpi/archive/refs/tags/1.0.0.tar.gz"
    git      = "https://github.com/spiral-software/spiral-package-mpi.git"

    maintainers = ['spiralgen']
    extends('spiral-software')

    version('develop', branch='develop')
    version('main',    branch='main')
    version('1.0.0',   sha256='64896a82aacce9cc8abe88b921e09ba7a5fceb8262e490f60a7088583c2c2151')

    # MPI package is an extension for Spiral (spec: spiral-software).  Spiral finds
    # extensions in the "namespaces/packages" folder.  Install the tree in a similarly
    # named folder so that when activated it'll get symlinked to the correct place.

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, 'namespaces', 'packages', 'mpi')
        install_tree('.', spiral_pkgs)
