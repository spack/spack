# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWaitress(PythonPackage):
    """Waitress: a production-quality pure-Python WSGI server with very acceptable performance."""

    homepage = "https://github.com/Pylons/waitress/"
    pypi = "waitress/waitress-2.1.2.tar.gz"

    license("ZPL-2.1")

    version(
        "2.1.2",
        sha256="7500c9625927c8ec60f54377d590f67b30c8e70ef4b8894214ac6e4cad233d2a",
        url="https://pypi.org/packages/58/6a/b4b5c582e04e837e4422cab6ec9de7fc10ca7ad7f4e370bb89d280d39552/waitress-2.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.1:2")
