# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyProv(PythonPackage):
    """A Python library for W3C Provenance Data Model (PROV).

    A library for W3C Provenance Data Model supporting PROV-JSON, PROV-XML and
    PROV-O (RDF)
    """

    homepage = "prov.readthedocs.io/"
    pypi     = "prov/prov-2.0.0.tar.gz"

    version('2.0.0', sha256='b6438f2195ecb9f6e8279b58971e02bc51814599b5d5383366eef91d867422ee')

    variant('dot', default=False, description='Graphical visualisation support for prov.model')

    depends_on('python@3.6:3', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-lxml@3.3.5:', type=('build', 'run'))
    depends_on('py-networkx@2.0:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.2:', type=('build', 'run'))
    depends_on('py-rdflib@4.2.1:', type=('build', 'run'))
    depends_on('py-pydot@1.2.0:', when='+dot', type=('build', 'run'))
    depends_on('graphviz', when='+dot', type=('build', 'run'))
