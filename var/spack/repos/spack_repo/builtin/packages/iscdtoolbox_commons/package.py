# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IscdtoolboxCommons(CMakePackage):
    """ISCDtoolbox -- Common definitions and functions (linear algebra, chrono, i/o...)"""

    homepage = "https://github.com/ISCDtoolbox"
    url = "https://github.com/ISCDtoolbox/Commons/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/ISCDtoolbox/Commons.git"

    license("LGPL-3.0-only", checked_by="jcortial-safran")

    maintainers("jcortial-safran")

    version(
        "1.0.0",
        sha256="d230f8a786bf8f6a14db21243c71ccb9c5d408da5da89ae6f334d1339c10f83e",
        preferred=True,
    )

    variant("openmp", default=False, description="Enable OpenMP support")

    # Allow to specify the compilation options and the install prefix
    # instead of being forced to use built-in ones
    patch("user-defined-prefix-path.patch")

    def cmake_args(self):
        return [self.define_from_variant("OPENMP", "openmp")]
