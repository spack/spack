# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class SpiralPackageHcol(Package):
    """This is the SPIRAL package for the Hybrid Control Operator Language
    (HCOL)."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-package-hcol/archive/refs/tags/1.0.0.tar.gz"
    git      = "https://github.com/spiral-software/spiral-package-hcol.git"

    maintainers = ['spiralgen']
    extends('spiral-software')

    version('master',  branch='master')
    version('1.0.0', sha256='18ae6f0a090de03723612a6c91ca17cf62971129540936d8c2738bd8f807a511')

    # HCOL package is an extension for Spiral (spec: spiral-software).  Extensions
    # packages for Spiral are intended to be installed in the spiral-software prefix,
    # in the "namespaces/packages" folder.  Install the tree in that folder under the
    # name 'hcol'.

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, 'namespaces', 'packages', 'hcol')
        install_tree('.', spiral_pkgs)
