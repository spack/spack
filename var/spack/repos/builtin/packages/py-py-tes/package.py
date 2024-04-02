# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyTes(PythonPackage):
    """Library for communicating with the GA4GH Task Execution API."""

    pypi = "py-tes/py-tes-0.4.2.tar.gz"

    license("MIT")

    version(
        "0.4.2",
        sha256="fc3fa392a15032f3fd2453b9e944eb40d5221a2ad10a86a335983c79c6e0feb2",
        url="https://pypi.org/packages/90/ca/fcd6b5c43cef0575ff8ccaf65ce90d7d515b44a3128e7285e6e24276fc65/py_tes-0.4.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@0.3:1.1.0-rc1")
        depends_on("py-attrs@17.4:", when="@0.4:1.1.0-rc1")
        depends_on("py-future@0.16:", when="@0.3:1.1.0-rc1")
        depends_on("py-python-dateutil@2.6.1:", when="@0.4.2:1.1.0-rc1")
        depends_on("py-requests@2.18.1:", when="@0.3:1.1.0-rc1")
