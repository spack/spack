# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Editorconfig(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://editorconfig.org/"
    url = "https://github.com/editorconfig/editorconfig-core-c/archive/refs/tags/v0.12.7.tar.gz"

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("BSD-2-Clause", checked_by="taliaferro")

    version("0.12.7", sha256="f89d2e144fd67bdf0d7acfb2ac7618c6f087e1b3f2c3a707656b4180df422195")

    depends_on("pcre2")

    # def cmake_args(self):
    #     # FIXME: Add arguments other than
    #     # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
    #     # FIXME: If not needed delete this function
    #     args = []
    #     return args
