# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHistoprint(PythonPackage):
    """Pretty print of NumPy (and other) histograms to the console"""

    homepage = "https://github.com/scikit-hep/histoprint"
    pypi = "histoprint/histoprint-2.2.0.tar.gz"

    license("MIT")

    version(
        "2.4.0",
        sha256="db5c07309ab12788c85ea2c679c47d49f1e961a5d4254270521c3e883256236a",
        url="https://pypi.org/packages/4b/f1/b8e4e56241f53f4db673d8927eb92b0a374f0ef57791764597b182cee1cd/histoprint-2.4.0-py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="bb2278172379b82aaa3b79e56896b51aad084902ddea7f076b5c4bf08c19ca6d",
        url="https://pypi.org/packages/a5/a7/435cd9b0955a20d96fbe56e175856ac4dbdb1eeadf717d7b653d431a63c9/histoprint-2.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-click@7:")
        depends_on("py-numpy", when="@2:")
        depends_on("py-uhi@0.2.1:", when="@2.2:")
