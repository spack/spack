# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfirefly(CMakePackage):
    """A standalone C++ Library for vectors calculations"""

    homepage = "https://libfirefly.tbhaxor.com"
    url = "https://github.com/tbhaxor/firefly/archive/refs/tags/v2.1.0.tar.gz"
    git = "https://github.com/tbhaxor/firefly.git"

    maintainers("tbhaxor")

    license("GPL-3.0-or-later")

    version("master", branch="master")
    version("2.1.0", sha256="4de4b216c73199a1826de7a0d45205b401603315347d7947d8b5950d3e6b893d")

    variant(
        "double-precision",
        description="Enables double type instead of float when enabled",
        default=True,
    )

    def cmake_args(self):
        args = [self.define_from_variant("Firefly_ENABLE_DOUBLE_PRECISION", "double-precision")]
        return args
