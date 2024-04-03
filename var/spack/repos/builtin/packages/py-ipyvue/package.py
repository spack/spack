# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyvue(PythonPackage):
    """
    Jupyter widgets base for Vue libraries.
    """

    homepage = "https://github.com/widgetti/ipyvue"
    pypi = "ipyvue/ipyvue-1.10.1.tar.gz"

    license("MIT")

    maintainers("jeremyfix")

    version(
        "1.10.1",
        sha256="572057b4b003b5a1b8cbe04eef2c41baa561fa74199cd2b9dd76cc4b5f2c5985",
        url="https://pypi.org/packages/5f/dc/107a9756ce488fbf4bb2dc8c08a3c4a680c96f2c7476b5014e14e9b71868/ipyvue-1.10.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-ipywidgets@7.0.0:")
