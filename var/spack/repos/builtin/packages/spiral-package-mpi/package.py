# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SpiralPackageMpi(Package):
    """This is the SPIRAL package for MPI."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-package-mpi/archive/1.0.0.tar.gz"
    git      = "https://github.com/spiral-software/spiral-package-mpi.git"

    maintainers = ['spiralgen']
    extends('spiral-software')

    version('develop', branch='develop')
    version('main',    branch='main')
    version('1.0.0-release', sha256='6ce985555cd8e625230dad266f43e066dbf47726bfa0f336e8b4ddbb9132fa2f')

    # MPI package is an extension for Spiral (spec: spiral-software).  Spiral finds
    # extensions in the "namespaces/packages" folder.  Install the tree in a similarly
    # named folder so that when activated it'll get symlinked to the correct place.

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, 'namespaces', 'packages', 'mpi')
        install_tree('.', spiral_pkgs)
