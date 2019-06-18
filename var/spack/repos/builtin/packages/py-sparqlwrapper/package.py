# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySparqlwrapper(PythonPackage):
    """SPARQLWrapper is a simple Python wrapper around a SPARQL service to remotelly execute your
    queries. It helps in creating the query invokation and, possibly, convert the result into a
    more manageable format."""

    homepage = "https://rdflib.github.io/sparqlwrapper/"
    url      = "https://pypi.io/packages/source/s/sparqlwrapper/SPARQLWrapper-1.8.4.tar.gz"

    version('1.8.4', '66f03ea95b75cb6dd652b110f395658c')

    depends_on('py-setuptools', type='build')

    depends_on('py-rdflib', type='run')
