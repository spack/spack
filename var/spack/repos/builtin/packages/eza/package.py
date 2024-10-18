# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Eza(CargoPackage):
    """A modern, maintained replacement for ls."""

    homepage = "https://github.com/eza-community/eza"
    url = "https://github.com/eza-community/eza/archive/refs/tags/v0.15.3.tar.gz"

    maintainers("trws")

    license("EUPL-1.2", when="@0.20:", checked_by="pranav-sivaraman")
    license("MIT", when="@:0.19", checked_by="pranav-sivaraman")

    version("0.20.2", sha256="8d5a573906fd362e27c601e8413b2c96b546bbac7cdedcbd1defe1332f42265d")
    version("0.20.1", sha256="e78a84cc5324ebb6481293d32edfdbc7de78511d5190b4808a0896f8ce4d652e")
    version("0.20.0", sha256="e6c058b13aecbed9f037c0607f0df19bc0a3532fea14dacd0090878ed4bbfadc")
    version("0.19.4", sha256="c0094b3ee230702d4dd983045e38ea2bd96375c16381c0206c88fae82fb551a4")
    version("0.19.3", sha256="c85760bcc14259f87937357cd1c8c9d301fe3d4d2da2e6129b572899e97345b1")
    version("0.19.2", sha256="db4897ef7f58d0802620180e0b13bb35563e03c9de66624206b35dcad21007f8")
    version("0.19.1", sha256="a256ecdb9996933300bb54e19a68df61e27385e5df20ba1f780f2e454a7f8e8a")
    version("0.19.0", sha256="440fff093c23635d7c1a9955d42489a2f5c5839a0e85a03e39daeca39e9dbf84")
    version("0.18.24", sha256="bdcf83f73f6d5088f6dc17c119d0d288fed4acd122466404772be5ef278887de")
    version("0.18.23", sha256="34b0e8a699ac1a8a308448f417f0c0137a67ea34e261fd6f106e8be9fd5bb54c")
    version("0.15.3", sha256="09093e565913104acb7a8eba974f8067c95566b6fbedf31138c9923a8cfde42f")
