# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQtawesome(PythonPackage):
    """FontAwesome icons in PyQt and PySide applications"""

    homepage = "https://github.com/spyder-ide/qtawesome"
    pypi = "QtAwesome/QtAwesome-0.4.1.tar.gz"

    license("MIT")

    version(
        "0.4.1",
        sha256="30c17c731961fe84364a5f52b313944e9068c702ade39b9d3a0c0e8e3b7ec412",
        url="https://pypi.org/packages/10/1e/46b08f21313c7b5bd162d9f9d8410d7bd25939a9898f97fbdbac4fff2f52/QtAwesome-0.4.1-py2.py3-none-any.whl",
    )
    version(
        "0.3.3",
        sha256="50dade7769c2fa6b447e6fa7e766ffd5bdbfa1944e548fc178890095b0a744ed",
        url="https://pypi.org/packages/ba/53/c3a629cb11f22d14510fc1546e2327b1af812d19565ebcab2b9a91958b9a/QtAwesome-0.3.3-py2.py3-none-any.whl",
    )
