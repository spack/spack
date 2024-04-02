# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQtconsole(PythonPackage):
    """Jupyter Qt console"""

    homepage = "https://ipython.org"
    pypi = "qtconsole/qtconsole-4.2.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.2.0",
        sha256="a287f9f0f7365ccb2f2a88e0cd4da883822e94d15b75dc19098cd8eec44d70d1",
        url="https://pypi.org/packages/47/2f/33e54c15ad70afa34146136b2a95d9689d17f85063d5408361a402284415/qtconsole-5.2.0-py3-none-any.whl",
    )
    version(
        "4.5.1",
        sha256="60d61d93f7d67ba2b265c6d599d413ffec21202fec999a952f658ff3a73d252b",
        url="https://pypi.org/packages/79/0b/efb5a694b6922bb85c35e4f1db6197daae23c764dd384023fc9517d79e26/qtconsole-4.5.1-py2.py3-none-any.whl",
    )
    version(
        "4.2.1",
        sha256="2725b13171152fcadda581e4189a6365d1eee47559e4c734db6dcd7241eff74e",
        url="https://pypi.org/packages/52/0e/082c44dd1f41027bcc83ee347c778f5a9f6adead20f64db6001fba4aaf0d/qtconsole-4.2.1-py2.py3-none-any.whl",
    )

    variant("docs", default=False, description="Build documentation")

    with default_args(type="run"):
        depends_on("py-ipykernel@4.1:", when="@4.2:4.3,4.4.3:")
        depends_on("py-ipython-genutils", when="@4.3,4.4.3:5.4")
        depends_on("py-jupyter-client@4.1:", when="@4.2:4.3,4.4.3:")
        depends_on("py-jupyter-core", when="@4.2:4.3,4.4.3:")
        depends_on("py-pygments", when="@4.2:4.3,4.4.3:")
        depends_on("py-pyzmq@17.1:", when="@4.7.2:")
        depends_on("py-qtpy", when="@4.7:5.2")
        depends_on("py-traitlets", when="@4.2:4.3,4.4.3:5.3.0")
