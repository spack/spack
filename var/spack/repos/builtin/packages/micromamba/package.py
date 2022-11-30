# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Micromamba(CMakePackage):
    """Mamba is a fast, robust, and cross-platform package manager (Miniconda alternative).

    Micromamba is faster and more standalone than Miniconda."""

    homepage = "https://mamba.readthedocs.io/"
    url = "https://github.com/mamba-org/mamba/archive/micromamba-1.0.0.tar.gz"

    maintainers = ["charmoniumQ"]

    version("1.0.0", sha256="7303d983b49a1a52b302ceae355af1c05afef3a07aa3ad6dd27c36d64c43f991")

    variant("shared", default=True, description="Link with shared libraries, otherwise static")

    with when("~shared"):
        # See https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L276
        depends_on("curl", type="link")
        depends_on("libssh2~shared", type="link")
        depends_on("krb5~shared", type="link")
        depends_on("openssl", type="link")
        depends_on("libarchive", type="link")
        depends_on("iconv", type="link")
        depends_on("bzip2", type="link")
        depends_on("lz4", type="link")
        depends_on("zstd", type="link")
        depends_on("zlib", type="link")
        depends_on("xz libs=static", type="link")
        depends_on("lzo", type="link")
        depends_on("libsolv+conda~shared", type="link")
        depends_on("nghttp2", type="link")
        depends_on("yaml-cpp~shared", type="link")
        depends_on("libreproc+cxx~shared", type="link")
        # See https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L342
        depends_on("fmt", type="link")
        depends_on("spdlog~shared", type="link")

        # Not specified, but needed:
        depends_on("tl-expected@b74fecd", type="link")
        depends_on("nlohmann-json", type="link")
        depends_on("cpp-termcolor", type="link")
        depends_on("cli11@2.2:", type="link")

    # See https://github.com/mamba-org/mamba/blob/micromamba-1.0.0/libmamba/CMakeLists.txt#L423
    with when("+shared"):
        depends_on("libsolv+conda", type=("link", "run"))
        depends_on("curl", type=("link", "run"))
        depends_on("libarchive", type=("link", "run"))
        depends_on("openssl", type=("link", "run"))
        depends_on("yaml-cpp", type=("link", "run"))
        depends_on("libreproc+cxx", type=("link", "run"))
        depends_on("tl-expected@b74fecd", type=("link", "run"))
        depends_on("fmt", type=("link", "run"))
        depends_on("spdlog", type=("link", "run"))

        # Not specified, but needed
        depends_on("nlohmann-json", type="link")
        depends_on("cpp-termcolor", type="link")
        depends_on("cli11@2.2:", type="link")

    patch("fix-threads.patch")

    def cmake_args(self):
        # See https://mamba.readthedocs.io/en/latest/developer_zone/build_locally.html#build-micromamba
        if "~shared" in self.spec:
            return [
                "-DBUILD_LIBMAMBA=ON",
                "-DBUILD_STATIC_DEPS=ON",
                "-DBUILD_MICROMAMBA=ON",
                "-DMICROMAMBA_LINKAGE=FULL_STATIC",
            ]
        else:
            return [
                "-DBUILD_LIBMAMBA=ON",
                "-DBUILD_MICROMAMBA=ON",
                "-DBUILD_SHARED=ON",
                "-DMICROMAMBA_LINKAGE=DYNAMIC",
            ]

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        Executable("mamba")("--version")
