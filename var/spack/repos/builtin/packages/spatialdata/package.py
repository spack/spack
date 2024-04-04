# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spatialdata(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://github.com/geodynamics/spatialdata/archive/refs/tags/v3.1.0.tar.gz"

    license("UNKNOWN", checked_by="github_user1")

    version("develop", git="https://github.com/geodynamics/spatialdata/", submodules="true")
    version("3.1.0", sha256="dd6caccbf41a51928183d6a1caf2380aa0ed0f2c8c71ecc9b2cd9e3f23aa418c")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("swig", type="build")

    depends_on("py-cig-pythia")
    depends_on("proj")
    depends_on("catch2")
    depends_on("py-numpy")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = []
        args.append("--enable-swig")
        return args
