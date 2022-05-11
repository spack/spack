# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class Muparserx(CMakePackage):
    """A C++ Library for Parsing Expressions with Strings, Complex
    Numbers, Vectors, Matrices and more. """

    homepage = "https://beltoforion.de/en/muparserx/"
    url      = "https://github.com/beltoforion/muparserx/archive/refs/tags/v4.0.8.tar.gz"

    version('4.0.8', sha256='5913e0a4ca29a097baad1b78a4674963bc7a06e39ff63df3c73fbad6fadb34e1')
