# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPastml(PythonPackage):
    """Ancestral character reconstruction and visualisation for rooted
    phylogenetic trees.
    """

    homepage = "https://github.com/evolbioinfo/pastml"
    pypi = "pastml/pastml-1.9.40.tar.gz"

    maintainers("snehring")

    license("GPL-3.0-or-later")

    version(
        "1.9.40",
        sha256="312949473573929302b722add46a65fe0b129a4908184434cb03eb3e85ea53fe",
        url="https://pypi.org/packages/ef/6c/fff82ffaf0606381cb6524f65116e8ae82183963e5e758b755fc63a40621/pastml-1.9.40-py3-none-any.whl",
    )
    version(
        "1.9.38",
        sha256="7f6715544d2a04918ab81731ab225cc97b9fa2a0a664fbc7fa54ca26e12c698d",
        url="https://pypi.org/packages/81/ca/d12c447feb6f433fad3be915ceba50053b824e8b191a7328b4f4c70e93e8/pastml-1.9.38-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.9.39:1.9.40")
        depends_on("py-biopython@1.70:", when="@1.9.36:")
        depends_on("py-ete3@3.1:", when="@1.9.36:")
        depends_on("py-itolapi@4:", when="@1.9.36:")
        depends_on("py-jinja2@2.11:", when="@1.9.36:")
        depends_on("py-numpy@1.22.0:", when="@1.9.39:")
        depends_on("py-numpy@1.19.0:", when="@1.9.36:1.9.38")
        depends_on("py-pandas@1.0.0:", when="@1.9.36:")
        depends_on("py-scipy@1.5.0:", when="@1.9.36:")
