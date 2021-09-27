# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRdflibJsonld(PythonPackage):
    """RDFLib plugin providing JSON-LD parsing and serialization."""

    homepage = "https://github.com/RDFLib/rdflib-jsonld"
    url      = "https://pypi.io/packages/source/r/rdflib-jsonld/rdflib-jsonld-0.5.0.tar.gz"

    version('0.5.0', sha256='4f7d55326405071c7bce9acf5484643bcb984eadb84a6503053367da207105ed')
    version('0.4.0', sha256='144774786a2fc7de09b24a9309cbcccc78bc48b152536d2ea1c1df2ad715bc2d')

    depends_on('py-setuptools', type='build')
    depends_on('py-rdflib', type='run')
