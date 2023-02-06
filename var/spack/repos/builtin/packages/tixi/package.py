# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tixi(CMakePackage):
    """TiXI is a fast and simple XML interface library and could be used
    from applications written in C, C++, Fortran, JAVA and Python."""

    homepage = "https://github.com/DLR-SC/tixi"
    url = "https://github.com/DLR-SC/tixi/archive/v3.0.3.tar.gz"
    git = "https://github.com/DLR-SC/tixi.git"

    version("3.3.0", sha256="988d79ccd53c815d382cff0c244c0bb8e393986377dfb45385792766adf6f6a9")
    version("3.2.0", sha256="8df65c4d252d56e98c5ef2657c7aff6086a07b5686716e786891609adaca9d2d")
    version("3.1.0", sha256="4547133e452f3455b5a39045a8528955dce55faf059afe652a350ecf37d709ba")
    version("3.0.3", sha256="3584e0cec6ab811d74fb311a9af0663736b1d7f11b81015fcb378efaf5ad3589")
    version("2.2.4", sha256="9080d2a617b7c411b9b4086de23998ce86e261b88075f38c73d3ce25da94b21c")

    variant(
        "shared", default=True, description="Enables the build of shared libraries", when="@3.0.3:"
    )
    variant("fortran", default=True, description="Enable Fortran bindings", when="@3.1.1:")

    depends_on("python", type="build")
    depends_on("expat")
    depends_on("curl")
    depends_on("libxml2")
    depends_on("libxslt")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")
        if self.spec.satisfies("+fortran"):
            args.append("-DTIXI_ENABLE_FORTRAN=ON")
        return args
