# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrojanzooSphinxTheme(PythonPackage):
    """TrojanZoo Sphinx Theme"""

    homepage = "https://github.com/ain-soph/trojanzoo_sphinx_theme"
    pypi = "trojanzoo_sphinx_theme/trojanzoo_sphinx_theme-0.1.0.tar.gz"

    license("GPL-3.0-or-later")

    version(
        "0.1.0",
        sha256="fed7602d10c9810e4242473e1a457a6aeaa69bd8de372bc7bd1234f14481d2b9",
        url="https://pypi.org/packages/3e/e6/cd7d8fbb6303309eb9d3dcaef733dc3a65358bee639dc1cd3a30aaa0b513/trojanzoo_sphinx_theme-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-docutils@0.17.1:", when="@0.0.29:0")
        depends_on("py-sphinx@4.2:", when="@0.0.29:0.1.4")
