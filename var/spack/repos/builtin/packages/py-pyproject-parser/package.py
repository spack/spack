# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyprojectParser(PythonPackage):
    """Parser for 'pyproject.toml'"""

    homepage = "https://github.com/repo-helper/pyproject-parser"
    pypi = "pyproject_parser/pyproject-parser-0.9.1.tar.gz"

    license("MIT")

    version(
        "0.9.1",
        sha256="800dbf9f24ec1d55bbdb703cf0c49c5a3f02570b13424157c9adab947b1bc899",
        url="https://pypi.org/packages/ff/5e/91d23fa308a7ee93513b9ca84580eafb57fe1bd1deb8609116e202225dbd/pyproject_parser-0.9.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-apeye-core@1.0.0:", when="@0.7:")
        depends_on("py-attrs@20.3:")
        depends_on("py-dom-toml@0.4:")
        depends_on("py-domdf-python-tools@2.8:")
        depends_on("py-natsort@7.1.1:")
        depends_on("py-packaging@20.9:")
        depends_on("py-shippinglabel@1:")
        depends_on("py-toml@0.10.2:")
        depends_on("py-tomli@1.2.3:", when="@0.9: ^python@:3.10")
        depends_on("py-typing-extensions@3.7.4.3:4.7.0-rc1,4.7.1:", when="@0.9.1:")

    conflicts("^py-setuptools@61")
    conflicts("^py-typing-extensions@4.7.0")
