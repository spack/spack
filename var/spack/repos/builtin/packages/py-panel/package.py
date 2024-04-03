# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPanel(PythonPackage):
    """A high level app and dashboarding solution for Python."""

    homepage = "http://panel.holoviz.org/"
    pypi = "panel/panel-0.14.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.14.4",
        sha256="dd4fcf2fc7276cd3f0df110ce7a6197ac4040d74c4efdc8c092b23771c1f514d",
        url="https://pypi.org/packages/b6/2e/6f47d12d9cd6bf11a028f022b7839c49c8d3cc2e08131f84006b1ca4a3fa/panel-0.14.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@:0")
        depends_on("py-bleach")
        depends_on("py-bokeh@2.4.0:2.4.0.0,2.4.1-rc1:2", when="@:0")
        depends_on("py-markdown")
        depends_on("py-param@1.12.0:", when="@:1.2")
        depends_on("py-pyct@0.4.4:", when="@:1.0.0-beta16")
        depends_on("py-pyviz-comms@0.7.4:", when="@:1.3.1")
        depends_on("py-requests")
        depends_on("py-setuptools@42:", when="@:1.0.2")
        depends_on("py-tqdm@4.48:")
        depends_on("py-typing-extensions")
