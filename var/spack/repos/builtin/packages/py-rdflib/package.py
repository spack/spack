# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRdflib(PythonPackage):
    """RDFLib is a pure Python package for working with RDF. RDFLib
       contains most things you need to work with RDF, including:
    parsers and serializers for RDF/XML, N3, NTriples, N-Quads,
    Turtle, TriX, Trig and JSON-LD (via a plugin).  a Graph interface
    which can be backed by any one of a number of Store
    implementations store implementations for in-memory storage and
    persistent storage on top of the Berkeley DB a SPARQL 1.1
    implementation - supporting SPARQL 1.1 Queries and Update
    statements """

    homepage = "https://github.com/RDFLib/rdflib"
    url      = "https://pypi.io/packages/source/r/rdflib/rdflib-6.0.0.tar.gz"

    version('6.0.2', sha256='6136ae056001474ee2aff5fc5b956e62a11c3a9c66bb0f3d9c0aaa5fbb56854e')
    version('6.0.0', sha256='7ce4d757eb26f4dd43205ec340d8c097f29e5adfe45d6ea20238c731dc679879')
    version('5.0.0', sha256='78149dd49d385efec3b3adfbd61c87afaf1281c30d3fcaf1b323b34f603fb155')

    depends_on('python@3.7:', when='@6:', type='build')
    depends_on('py-setuptools', when='@:5', type='build')
    depends_on('py-setuptools', when='@6:', type=('build', 'run'))
    depends_on('py-pyparsing', type=('build', 'run'))
    depends_on('py-isodate', type=('build', 'run'))
    depends_on('py-six', when='@:5', type=('build', 'run'))
