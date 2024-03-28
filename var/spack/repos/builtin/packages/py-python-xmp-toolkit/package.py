# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonXmpToolkit(PythonPackage):
    """Python XMP Toolkit for working with metadata."""

    homepage = "https://github.com/python-xmp-toolkit/python-xmp-toolkit"
    pypi = "python-xmp-toolkit/python-xmp-toolkit-2.0.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.0.1",
        sha256="ad7869810687b594d21901ed101906ae4291b270ce09af5ea6886be49202e186",
        url="https://pypi.org/packages/8d/be/1f64e6e9c4e6b6b4689ec9bbc2e3804ac70227c5e3040a86c9afc21402bb/python_xmp_toolkit-2.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pytz", when="@2.0.1:")
