# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ftxui(CMakePackage):
    """Functional Terminal (X) User interface.
    A simple C++ library for terminal based user interfaces."""

    homepage = "https://arthursonzogni.github.io"
    url = "https://github.com/ArthurSonzogni/FTXUI/archive/refs/tags/v2.0.0.tar.gz"

    version("4.0.0", sha256="7276e4117429ebf8e34ea371c3ea4e66eb99e0f234cb4c5c85fca17174a53dfa")
    version("2.0.0", sha256="d891695ef22176f0c09f8261a37af9ad5b262dd670a81e6b83661a23abc2c54f")
