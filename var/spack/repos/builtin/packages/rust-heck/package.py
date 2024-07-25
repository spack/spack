# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustHeck(CargoPackage):
    """A case conversion library for Rust."""

    homepage = "https://docs.rs/heck/0.5.0/heck/"
    git = "https://github.com/withoutboats/heck.git"

    license("APACHE-2.0 OR MIT", checked_by="teaguesterling")

    version("0.5", commit="070693322aee7c5c7fbee7c9964bf8d7d3a29c96")
