# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import shutil

from spack.package import *


class QtDeclarative(CMakePackage):
    """Qt Declarative (Quick 2)."""

    homepage = "https://www.qt.io"
    url = "https://github.com/qt/qtdeclarative/archive/refs/tags/v6.2.3.tar.gz"
    list_url = "https://github.com/qt/qtdeclarative/tags"

    maintainers = ["wdconinc", "sethrj"]

    version("6.3.2", sha256="140a3c4973d56d79abf5fea9ae5cf13b3ef7693ed1d826b263802926a4ba84b6")
    version("6.3.1", sha256="1606723c2cc150c9b7339fd33ca5e2ca00d6e738e119c52a1d37ca12d3329ba9")
    version("6.3.0", sha256="b7316d6c195fdc31ecbf5ca2acf2888737539919a02ff8f11a911432d50c17ac")
    version("6.2.4", sha256="cd939d99c37e7723268804b9516e32f8dd64b985d847469c78b66b5f4481c548")
    version("6.2.3", sha256="eda82abfe685a6ab5664e4268954622ccd05cc9ec8fb16eaa453c54900591baf")

    generator = "Ninja"

    # Changing default to Release for typical use in HPC contexts
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo", "MinSizeRel"),
        description="CMake build type",
    )

    depends_on("cmake@3.16:", type="build")
    depends_on("ninja", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python", when="@5.7.0:", type="build")

    _versions = ["6.3.2", "6.3.1", "6.3.0", "6.2.4", "6.2.3"]
    for v in _versions:
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-shadertools@" + v, when="@" + v)

    def patch(self):
        vendor_dir = join_path(self.stage.source_path, "src", "3rdparty")
        vendor_deps_to_keep = ["masm"]
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep not in vendor_deps_to_keep:
                        shutil.rmtree(dep)
