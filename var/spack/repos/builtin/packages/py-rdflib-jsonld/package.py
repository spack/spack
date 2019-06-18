# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRdflibJsonld(PythonPackage):
    """RDFLib plugin providing JSON-LD parsing and serialization."""

    homepage = "https://github.com/RDFLib/rdflib-jsonld"
    url      = "https://pypi.io/packages/source/r/rdflib-jsonld/rdflib-jsonld-0.4.0.tar.gz"

    version('0.4.0', '69097f57d302791a2959c07e110c47cf')

    depends_on('py-setuptools', type='build')

    depends_on('py-rdflib', type='run')
