# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    # MPI package is an extension for Spiral (spec: spiral-software).  Extensions
    # packages for Spiral are intended to be installed in the spiral-software prefix,
    # in the "namespaces/packages" folder.  Install the tree in that folder under the
    # name 'mpi'.

    def install(self, spec, prefix):
        spec = self.spec
        spiral_locn = '{0}'.format(spec['spiral-software'].prefix)
        spiral_pkgs = join_path(spiral_locn, 'namespaces', 'packages', 'mpi')
        install_tree('.', spiral_pkgs)
