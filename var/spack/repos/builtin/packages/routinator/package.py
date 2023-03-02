# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Routinator(Package):
    """An RPKI Validator and RTR server written in Rust"""

    homepage = "https://nlnetlabs.nl/projects/rpki/about/"
    url = "https://github.com/NLnetLabs/routinator/archive/refs/tags/v0.11.2.tar.gz"

    maintainers("aweits")

    version("0.11.2", sha256="00f825c53168592da0285e8dbd228018e77248d458214a2c0f86cd0ca45438f5")

    depends_on("rust@1.56:")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")
