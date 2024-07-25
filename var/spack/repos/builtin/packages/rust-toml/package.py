# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustToml(CargoPackage):
    """Rust TOML Parser"""

    homepage = "https://docs.rs/toml"
    url = "https://github.com/toml-rs/toml/archive/refs/tags/v0.22.16.tar.gz"

    license("APACHE-2.0 OR MIT", checked_by="teaguesterling")

    version("0.22.16", sha256="8cdd73db2290c389f724605244f057c725e91bfd327521c1e566eaf11bd04a96")

