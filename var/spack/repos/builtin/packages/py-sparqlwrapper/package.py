# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySparqlwrapper(PythonPackage):
    """SPARQLWrapper is a simple Python wrapper around a SPARQL service to
    remotelly execute your queries."""

    homepage = "https://rdflib.github.io/sparqlwrapper/"
    pypi = "sparqlwrapper/SPARQLWrapper-1.8.4.tar.gz"

    version('1.8.4', sha256='21928e7a97f565e772cdeeb0abad428960f4307e3a13dbdd8f6d3da8a6a506c9')

    depends_on('py-setuptools@:57', type='build')
    depends_on('py-rdflib', type=('build', 'run'))
