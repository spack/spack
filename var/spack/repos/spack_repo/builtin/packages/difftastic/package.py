# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Difftastic(CargoPackage):
    """Difftastic is a structural diff tool that compares files based on their syntax."""

    homepage = "https://difftastic.wilfred.me.uk/"
    url = "https://github.com/Wilfred/difftastic/archive/refs/tags/0.63.0.tar.gz"

    maintainers("alecbcs")

    license("MIT")

    version("0.63.0", sha256="f96bcf4fc961921d52cd9fe5aa94017924abde3d5a3b5a4727b103e9c2d4b416")

    depends_on("rust@0.64.0:", type="build")
