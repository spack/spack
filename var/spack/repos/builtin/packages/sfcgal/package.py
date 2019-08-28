# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sfcgal(CMakePackage):
    """
    SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
    ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations. SFCGAL
    provides standard compliant geometry types and operations, that can be
    accessed from its C or C++ APIs.
    """

    homepage = "http://www.sfcgal.org/"
    url      = "https://github.com/Oslandia/SFCGAL/archive/v1.3.7.tar.gz"

    version('1.3.7', sha256='30ea1af26cb2f572c628aae08dd1953d80a69d15e1cac225390904d91fce031b')

    variant('viewer', default=False, description='Build viewer and support for 3D format export')

    depends_on('cgal+core')
    depends_on('boost@:1.69.0')
    depends_on('mpfr')
    depends_on('gmp')

    depends_on('openscenegraph@3.1:', when='+viewer')
