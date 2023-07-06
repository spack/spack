# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Spot(AutotoolsPackage):
    """Spot is a C++11 library for omega-automata manipulation and model
    checking."""

    homepage = "https://spot.lrde.epita.fr/"
    url = "https://www.lrde.epita.fr/dload/spot/spot-1.99.3.tar.gz"

    version("2.11.5", sha256="3acfd5cd112d00576ac234baeb34e1c6adf8c03155d4cda973e6317ac8bd1774")
    version("2.11.4", sha256="91ecac6202819ea1de4534902ce457ec6eec0573d730584d6494d06b0bcaa0b4")
    version("2.9.4", sha256="e11208323baabe9b5f98098d4b9bb39803fb102a68abbbaf900f1fcd578f0f85")
    version("1.99.3", sha256="86964af559994af4451a8dca663a9e1db6e869ed60e747ab60ce72dddc31b61b")
    version("1.2.6", sha256="360678c75f6741f697e8e56cdbc9937f104eb723a839c3629f0dc5dc6de11bfc")

    variant("python", default=True, description="Enable python API")

    depends_on("python@3.3:", when="@1.99.5: +python")
    depends_on("python@3.2:", when="@1.99: +python")
    depends_on("python@2:", when="+python")
    depends_on("boost", when="@:1.2.6")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@:1.2.6")
