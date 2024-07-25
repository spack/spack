# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustSerde(CargoPackage):
    """Serialization framework for Rust"""

    homepage = "https://serde.rs/"
    url = "https://github.com/serde-rs/serde/archive/refs/tags/v1.0.204.tar.gz"

    license("APACHE-2.0 OR MIT", checked_by="teaguesterling")

    version("1.0.204", sha256="a80905a74f9bf0bafd5950965e78ead1f67403e2ed86039db97c794d382353bc")
    version("1.0.203", sha256="6094e68bfe1c55a4604bff1e13317d995ace06ddefaa2976d6f051a56a6fc5e7")
    version("1.0.103", sha256="5ed0bf592dee65691c221ce30b0f690938506d3b310178d55278f47f65e540ea")

    variant("derive", default=False, description="Build with derive feature")

    def build_args(self):
        args = []
        if self.spec.satisfies("+derive"):
            args += ["--features", "derive"]
        return args
