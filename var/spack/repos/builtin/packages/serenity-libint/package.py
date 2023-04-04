# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SerenityLibint(CMakePackage):
    """Serenity fork of libint, which is difficult to reproduce from libint itself"""

    homepage = "https://thclab.uni-muenster.de/serenity/libint"
    url = "https://thclab.uni-muenster.de/serenity/libint/-/raw/e3eb756c/libint-2.7.0-beta.6.tgz"

    version("2.7.0-beta.6", "53af60c7be74374b2a2d893b3d2d37fa6a3078a72d98067bf71ba4ede4e807df")

    depends_on("boost")
    depends_on("eigen@3:")  # Probably overdepending?
    depends_on("gmp+cxx")

    def cmake_args(self):
        args = [self.define("BUILD_SHARED_LIBS", True)]
        return args
