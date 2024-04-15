# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVersioneer518(PythonPackage):
    """Versioneer is a tool to automatically update version strings by
    asking your version-control system about the current tree."""

    homepage = "https://github.com/python-versioneer/versioneer-518"
    pypi = "versioneer-518/versioneer-518-0.19.tar.gz"
    git = "https://github.com/python-versioneer/versioneer-518.git"

    # A workaround for invalid URL, most likely due to presence of 518 in the name.
    version(
        "0.19",
        sha256="c0ec39a20525d0eb030ae29d76096131bb09050c71f8dd82bbeda4c24fa79dac",
        url="https://pypi.org/packages/23/fe/36afae1284065be05b5620ee2c22592baf39c71e00dbc11d55f0558b4b38/versioneer_518-0.19-py2.py3-none-any.whl",
    )
