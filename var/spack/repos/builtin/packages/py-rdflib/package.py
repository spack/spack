# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRdflib(PythonPackage):
    """RDFLib is a pure Python package for working with RDF. RDFLib
       contains most things you need to work with RDF, including:
    parsers and serializers for RDF/XML, N3, NTriples, N-Quads,
    Turtle, TriX, Trig and JSON-LD (via a plugin).  a Graph interface
    which can be backed by any one of a number of Store
    implementations store implementations for in-memory storage and
    persistent storage on top of the Berkeley DB a SPARQL 1.1
    implementation - supporting SPARQL 1.1 Queries and Update
    statements"""

    homepage = "https://github.com/RDFLib/rdflib"
    pypi = "rdflib/rdflib-5.0.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "7.0.0",
        sha256="0438920912a642c866a513de6fe8a0001bd86ef975057d6962c79ce4771687cd",
        url="https://pypi.org/packages/d4/b0/7b7d8b5b0d01f1a0b12cc2e5038a868ef3a15825731b8a0d776cf47566c0/rdflib-7.0.0-py3-none-any.whl",
    )
    version(
        "6.3.2",
        sha256="36b4e74a32aa1e4fa7b8719876fb192f19ecd45ff932ea5ebbd2e417a0247e63",
        url="https://pypi.org/packages/af/92/d7fb1d7fb70c9f7003fa50b7a3880ebcb311cc3f8552b3595e7c8f75aeeb/rdflib-6.3.2-py3-none-any.whl",
    )
    version(
        "6.2.0",
        sha256="85c34a86dfc517a41e5f2425a41a0aceacc23983462b32e68610b9fad1383bca",
        url="https://pypi.org/packages/50/fb/a0f8b6ab6598b49871a48a189dc1942fb0b0543ab4c84f689486233ef1ec/rdflib-6.2.0-py3-none-any.whl",
    )
    version(
        "6.0.2",
        sha256="b7642daac8cdad1ba157fecb236f5d1b2aa1de64e714dcee80d65e2b794d88a6",
        url="https://pypi.org/packages/34/77/2995c0d4b89607ce2c5e062995f7a26ed61a4d9e20cfc3711f5e8adeaa7e/rdflib-6.0.2-py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="88208ea971a87886d60ae2b1a4b2cdc263527af0454c422118d43fe64b357877",
        url="https://pypi.org/packages/d0/6b/6454aa1db753c0f8bc265a5bd5c10b5721a4bb24160fb4faf758cf6be8a1/rdflib-5.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3", when="@7:")
        depends_on("python@3.7:", when="@6:6.2")
        depends_on("python@3.7:3", when="@6.3:6")
        depends_on("py-importlib-metadata@4", when="@6.3:6 ^python@3.7")
        depends_on("py-importlib-metadata", when="@6.1:6.2 ^python@:3.7")
        depends_on("py-isodate@0.6:", when="@6.3:")
        depends_on("py-isodate", when="@4.2.2:6.2")
        depends_on("py-pyparsing@2.1:", when="@6.3:")
        depends_on("py-pyparsing", when="@4.2.2:6.2")
        depends_on("py-setuptools", when="@6:6.2")
        depends_on("py-six", when="@5")

    # Historical dependencies
