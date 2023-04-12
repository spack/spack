# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class Codecov(Package):
    """Codecov uploads coverage reports to Codecov for processing."""

    homepage = "https://codecov.io"
    _url_base = "https://github.com/codecov/uploader/releases/download/v0.4.1/codecov"

    if platform.system() == "Linux" and platform.machine() == "x86_64":
        version(
            "0.4.1",
            sha256="32cb14b5f3aaacd67f4c1ff55d82f037d3cd10c8e7b69c051f27391d2e66e15c",
            url=_url_base + "-linux",
            expand=False,
        )
    elif platform.system() == "Darwin":
        version(
            "0.4.1",
            sha256="4ab0f06f06e9c4d25464f155b0aff36bfc1e8dbcdb19bfffd586beed1269f3af",
            url=_url_base + "-macos",
            expand=False,
        )
    elif platform.system() == "Windows":
        version(
            "0.4.1",
            sha256="e0cda212aeaebe695509ce8fa2d608760ff70bc932003f544f1ad368ac5450a8",
            url=_url_base + ".exe",
            expand=False,
        )

    def install(self, spec, prefix):
        codecov = self.stage.archive_file
        chmod = which("chmod")
        chmod("+x", codecov)
        mkdirp(prefix.bin)
        install(codecov, join_path(prefix.bin, "codecov"))
