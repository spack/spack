# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPyshacl(PythonPackage):
    """A Python validator for SHACL."""

    homepage = "https://github.com/RDFLib/pySHACL"
    pypi = "pyshacl/pyshacl-0.17.2.tar.gz"

    license("Apache-2.0")

    version(
        "0.25.0",
        sha256="716b65397486b1a306efefd018d772d3c112a3828ea4e1be27aae16aee524243",
        url="https://pypi.org/packages/e0/d9/6d21af0dd75f2df32b18420fca099d05c853406e3e0ec649e578ce3f7ee0/pyshacl-0.25.0-py3-none-any.whl",
    )
    version(
        "0.20.0",
        sha256="5de57ed490748f621301f69e47224fa5bd84b0fb5aab40126118dc8e90d4ede6",
        url="https://pypi.org/packages/2d/c1/f430a347d02d5f7b061c95d9e39b36da4b78a6b47d92728253bd7698eb3a/pyshacl-0.20.0-py3-none-any.whl",
    )
    version(
        "0.17.2",
        sha256="ec147758eabadac13d8a981c5b9da9447ac6eb04cc6f013b92902cf24adad373",
        url="https://pypi.org/packages/39/62/4a4a03b9daefe1046b976e7cf0ff1238942ca51fa0cfa029fad9af4bcaad/pyshacl-0.17.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3", when="@0.25:")
        depends_on("python@3.7:3", when="@0.17:0.17.2,0.18:0.24")
        depends_on("py-html5lib@1.1:", when="@0.20:")
        depends_on("py-importlib-metadata@6.0.1:", when="@0.25: ^python@:3.11")
        depends_on("py-owlrl@6:", when="@0.18:")
        depends_on("py-owlrl@5.2.3:5", when="@0.16.2.post:0.17.2")
        depends_on("py-packaging@21.3:", when="@0.19.1:")
        depends_on("py-prettytable@3.7:", when="@0.24: ^python@3.12:")
        depends_on("py-prettytable@3.5:", when="@0.24: ^python@3.8:3.11")
        depends_on("py-prettytable@2.2.1:2", when="@0.17.2:0.23")
        depends_on("py-rdflib@6.3.2:", when="@0.24: ^python@3.8:")
        depends_on("py-rdflib@6.2:6", when="@0.20:0.22")
        depends_on("py-rdflib@6", when="@0.17")
