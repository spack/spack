# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Eza(CargoPackage):
    """A modern, maintained replacement for ls."""

    homepage = "https://github.com/eza-community/eza"
    url = "https://github.com/eza-community/eza/archive/refs/tags/v0.15.3.tar.gz"

    maintainers("trws")

    license("MIT")

    version("0.15.3", sha256="09093e565913104acb7a8eba974f8067c95566b6fbedf31138c9923a8cfde42f")
