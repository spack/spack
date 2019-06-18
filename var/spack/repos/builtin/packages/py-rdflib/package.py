# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRdflib(PythonPackage):
    """RDFLib is a Python library for working with RDF, a simple yet powerful language for
    representing information as graphs."""

    homepage = "https://rdflib.readthedocs.io/en/stable"
    url      = "https://pypi.io/packages/source/r/rdflib/rdflib-4.2.2.tar.gz"

    version('4.2.2', '534fe35b13c5857d53fa1ac5a41eca67')

    depends_on('py-setuptools', type='build')

    depends_on('py-six', type='run')
    depends_on('py-isodate', type='run')
    depends_on('py-html5lib', type='run')
    depends_on('py-requests', type='run')
    depends_on('py-pyparsing', type='run')
