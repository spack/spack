# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydap(PythonPackage):
    """An implementation of the Data Access Protocol."""

    homepage = "https://www.pydap.org/en/latest/"
    pypi = "Pydap/Pydap-3.2.2.tar.gz"

    license("MIT")

    version(
        "3.2.2",
        sha256="9655711d8da71192bda78fed15cbf4fc7fb1decc661ea5022263c0143648cf63",
        url="https://pypi.org/packages/9e/ad/01367f79b24015e223dd7679e4c9b16a6792fe5a9772e45e5f81b2c4a021/Pydap-3.2.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-beautifulsoup4", when="@3.2.2:")
        depends_on("py-docopt", when="@3.2.2:")
        depends_on("py-jinja2", when="@3.2.2:")
        depends_on("py-numpy", when="@3.2.2:")
        depends_on("py-six@1.4:", when="@3.2.2:")
        depends_on("py-webob", when="@3.2.2:")
