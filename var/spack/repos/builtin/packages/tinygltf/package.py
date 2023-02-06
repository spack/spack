# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tinygltf(CMakePackage):
    """Header only C++11 tiny glTF 2.0 library."""

    homepage = "https://github.com/syoyo/tinygltf"
    url = "https://github.com/syoyo/tinygltf/archive/refs/tags/v2.5.0.tar.gz"

    version("2.5.0", sha256="5d85bd556b60b1b69527189293cfa4902957d67fabb8582b6532f23a5ef27ec1")

    depends_on("cmake@3.6:", type="build")
