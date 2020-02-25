# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRdflib(PythonPackage):
    """RDFLib is a Python library for working with RDF, a simple yet
    powerful language for representing information as graphs."""

    homepage = "https://rdflib.readthedocs.io/en/stable"
    url      = "https://pypi.io/packages/source/r/rdflib/rdflib-4.2.2.tar.gz"

    version('4.2.2', sha256='da1df14552555c5c7715d8ce71c08f404c988c58a1ecd38552d0da4fc261280d')

    depends_on('py-setuptools', type='build')

    depends_on('py-six', type='run')
    depends_on('py-isodate', type='run')
    depends_on('py-html5lib', type='run')
    depends_on('py-requests', type='run')
    depends_on('py-pyparsing', type='run')
