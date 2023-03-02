# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Imath(CMakePackage):
    """Imath is a basic, light-weight, and efficient C++ representation of 2D and 3D
    vectors and matrices and other simple but useful mathematical objects, functions,
    and data types common in computer graphics applications, including the "half"
    16-bit floating-point type."""

    homepage = "https://github.com/AcademySoftwareFoundation/Imath"
    url = "https://github.com/AcademySoftwareFoundation/Imath/archive/refs/tags/v3.1.5.tar.gz"

    version("3.1.5", sha256="1e9c7c94797cf7b7e61908aed1f80a331088cc7d8873318f70376e4aed5f25fb")

    depends_on("cmake@3.12:", type="build")
