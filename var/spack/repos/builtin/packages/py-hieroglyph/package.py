# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHieroglyph(PythonPackage):
    """Hieroglyph is an extension for Sphinx which builds HTML
    presentations from ReStructured Text documents.
    """

    homepage = "https://github.com/nyergler/hieroglyph"
    pypi = "hieroglyph/hieroglyph-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.1.0",
        sha256="4df61f8df6f18e53d4b1e34b4b832cdc75eb09334d4ba2e723b19b3069eb07f1",
        url="https://pypi.org/packages/aa/7e/f14e6e87d13e729b8b17b065316076f2f3b17111e32dc95646dc5c6a3ab1/hieroglyph-2.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="912cb59829de22f270828c771266b9968613534d6e0a16d8b46be307d272c3ca",
        url="https://pypi.org/packages/e8/dc/d782dd5645a02e81f85e7dd43a18fca9d61680792b317b729226e9b5edc5/hieroglyph-1.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-setuptools", when="@1:")
        depends_on("py-six", when="@1")
        depends_on("py-sphinx@2.0.0:", when="@2:")
        depends_on("py-sphinx@1.2:", when="@1")
