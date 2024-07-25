# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustIndexmap(CargoPackage):
    """A hash table with consistent order and fast iteration; access items by key or sequence index"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://docs.rs/indexmap/"
    url = "https://github.com/indexmap-rs/indexmap/archive/refs/tags/2.2.6.tar.gz"

    license("APACHE-2.0 OR MIT", checked_by="teaguesterling")

    version("2.2.6", sha256="11a8a9fa470e76b0f23f323511b31ffadb6813392993ca95003284829815d5e4")


