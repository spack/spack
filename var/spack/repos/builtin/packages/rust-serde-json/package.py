# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustSerdeJson(CargoPackage):
    """Strongly typed JSON library for Rust"""

    homepage = "https://docs.rs/serde_json"
    url = "https://github.com/serde-rs/json/archive/refs/tags/v1.0.120.tar.gz"

    license("APACHE-2.0 OR MIT", checked_by="teaguesterling")

    version("1.0.120", sha256="ce0df93caf71c1ec72a41f66c73979b5259f2a7cfce41465f8f39a540d49dc14")
    version("1.0.119", sha256="3667dc8000c99e24aa7a9e7b450f2818f57dde5eacf4780cc9bfbd37b057ef9d")

    depends_on("rust@1.56:")
    depends_on("rust-serde@1.0.94:")
    depends_on("rust-indexmap@2.2.3:")

