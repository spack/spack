# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Micromamba(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://mamba.readthedocs.io/"
    url = "https://github.com/mamba-org/mamba"

    maintainers = ["charmoniumQ"]

    version("1.0.0", sha256="7303d983b49a1a52b302ceae355af1c05afef3a07aa3ad6dd27c36d64c43f991")

    # See https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L276
    depends_on("curl", type="build")
    depends_on("libssh2~shared", type="build")
    depends_on("krb5~shared", type="build")
    depends_on("openssl", type="build")
    depends_on("libarchive", type="build")
    depends_on("iconv", type="build")
    depends_on("bzip2", type="build")
    depends_on("lz4", type="build")
    depends_on("zstd", type="build")
    depends_on("zlib", type="build")
    depends_on("xz libs=static", type="build")
    depends_on("lzo", type="build")
    depends_on("libsolv~shared", type="build")
    depends_on("nghttp2", type="build")
    depends_on("yaml-cpp~shared", type="build")
    depends_on("libreproc+cxx~shared", type="build")

    depends_on("fmt", type="build")
    depends_on("spdlog", type="build")
    depends_on("nlohmann-json", type="build")
    depends_on("python", type="build")

    def url_for_version(self, version):
        return f"{self.url}/archive/refs/tags/micromamba-{version}.tar.gz"

    def cmake_args(self):
        # See https://mamba.readthedocs.io/en/latest/developer_zone/build_locally.html#build-micromamba
        return [
            "-DBUILD_LIBMAMBA=ON",
            "-DBUILD_STATIC_DEPS=ON",
            "-DBUILD_MICROMAMBA=ON",
            "-DMICROMAMBA_LINKAGE=DYNAMIC",
        ]
