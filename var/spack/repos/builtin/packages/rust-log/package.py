# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustLog(CargoPackage):
    """Logging implementation for Rust"""

    homepage = "https://docs.rs/log"
    url = "https://github.com/rust-lang/log/archive/refs/tags/0.4.22.tar.gz"

    license("APACHE-2.0 OR MIT", checked_by="teaguesterling")

    version("0.4.22", sha256="d5b9cc6bdd162cd8887702fa0f33963a6a5e686f9d3428247e4593bd0b273e5d")
    version("0.4.21", sha256="480093c38d9ab1aa43f4c8e4233c0b584f8b4a6e63457aeb6307c17632b31a18")
    version("0.4.20", sha256="a24acf26738e61c136187dbf1fffb065571126c38551e67152e7afa4a19d4e1f")
    version("0.4.19", sha256="143161cbd4c54709339e2ce4a5c44d12ebe097435047c19f49f72c1f0bd34dff")
    version("0.4.18", sha256="628a4ebdf8546b6e6dc33a02944f0d04b49d2ebf92208c91d0a160594c6d00e1")
    version("0.4.17", sha256="7163b79b6f8ab1a3175a3dce4b9e7603b65827a77722a25cc78b7917bfebfd20")
    version("0.4.15", sha256="359afe7082386b782fade9bbdd033c737181356b7f648e5c77341969753a342e")
    version("0.4.14", sha256="7c7911338850bb5f189be081866854f50c51a22d6d448ab90446742b5c911393")
    version("0.4.13", sha256="705cd2c4d7c83f4123aa0a72a7a9843f9a899b993b5e4b2831b087cb3f12e52b")
    version("0.4.12", sha256="be36b344650940670caa413b63a61dd5436ace24306e91c0f43f954871b7837e")

    depends_on("rust@1.60:")
