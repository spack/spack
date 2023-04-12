# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Codecov(Package):
    """Codecov uploads coverage reports to Codecov for processing."""

    homepage = "https://codecov.io"
    url = "https://uploader.codecov.io/v0.4.0/linux/codecov"

    version(
        "0.4.0",
        sha256="671cf0d89d1c149f57e1a9a31f3fb567ab4209e4d5829f13ff7b8c104db7131f",
        expand=False,
    )

    def install(self, spec, prefix):
        chmod = which("chmod")
        chmod("+x", "codecov")
        mkdirp(prefix.bin)
        install("codecov", prefix.bin)
