# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClickPlugins(PythonPackage):
    """An extension module for py-click to register external CLI
    commands via setuptools entry-points."""

    pypi = "click-plugins/click-plugins-1.0.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.1.1",
        sha256="5d262006d3222f5057fd81e1623d4443e41dcda5dc815c06b442aa3c02889fc8",
        url="https://pypi.org/packages/e9/da/824b92d9942f4e472702488857914bdd50f73021efea15b4cad9aca8ecef/click_plugins-1.1.1-py2.py3-none-any.whl",
    )
    version(
        "1.0.4",
        sha256="b1ee1ccc9421c73007fe290680d97984eb6eaf5f4512b7620c6aa46031d6cb6b",
        url="https://pypi.org/packages/95/dd/fef84cf1678418f241ef542c0288bdf215bdd3e35f1fe03dc5223a2e80ba/click_plugins-1.0.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-click@4:", when="@1.1:")
        depends_on("py-click@3:", when="@1.0.2,1.0.4:1.0")
