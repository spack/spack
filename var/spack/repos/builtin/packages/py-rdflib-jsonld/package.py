# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRdflibJsonld(PythonPackage):
    """rdflib extension adding JSON-LD parser and serializer"""

    homepage = "https://github.com/RDFLib/rdflib-jsonld"
    pypi = "rdflib-jsonld/rdflib-jsonld-0.6.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.6.2",
        sha256="011afe67672353ca9978ab9a4bee964dff91f14042f2d8a28c22a573779d2f8b",
        url="https://pypi.org/packages/29/92/da92898b2aab0da78207afc9c035a71bedef3544966374c44e9627d761c5/rdflib_jsonld-0.6.2-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="d290c03c5097ec3d96bd20dad8ff8b535e3e7cf53d05acf8ac48983eb36a4572",
        url="https://pypi.org/packages/89/26/cc1ec0d5da9288ac308733b888220dbfc41824384261cd881f27e2b68bd5/rdflib_jsonld-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-rdflib@5.0.0:", when="@0.6.1:")
        depends_on("py-rdflib", when="@0.6:0.6.0")
