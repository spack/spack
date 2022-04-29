# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RDesc(RPackage):
    """Manipulate DESCRIPTION Files.

    Tools to read, write, create, and manipulate DESCRIPTION files. It is
    intended for packages that create or manipulate other packages."""

    cran = "desc"

    version('1.4.0', sha256='8220e4c706449b8121b822e70b1414f391ef419aed574836a234c63b83e5d649')
    version('1.2.0', sha256='e66fb5d4fc7974bc558abcdc107a1f258c9177a29dcfcf9164bc6b33dd08dae8')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-rprojroot', type=('build', 'run'))

    depends_on('r-assertthat', type=('build', 'run'), when='@:1.2')
