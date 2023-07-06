# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fd(Package):
    """A simple, fast and user-friendly alternative to 'find'"""

    homepage = "https://github.com/sharkdp/fd"
    url = "https://github.com/sharkdp/fd/archive/refs/tags/v8.4.0.tar.gz"

    version("8.7.0", sha256="13da15f3197d58a54768aaad0099c80ad2e9756dd1b0c7df68c413ad2d5238c9")
    version("8.4.0", sha256="d0c2fc7ddbe74e3fd88bf5bb02e0f69078ee6d2aeea3d8df42f508543c9db05d")
    version("7.4.0", sha256="33570ba65e7f8b438746cb92bb9bc4a6030b482a0d50db37c830c4e315877537")

    maintainers("alecbcs", "ashermancinelli")

    depends_on("rust")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")
