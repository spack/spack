# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyPyshacl(PythonPackage):
    """A Python validator for SHACL.
    """

    homepage = "https://github.com/RDFLib/pySHACL"
    url = "https://pypi.io/packages/source/p/pyshacl/pyshacl-0.11.6.post1.tar.gz"

    version('0.11.6.post1', sha256='addb61272ab8487f9476d229cea08f5dde0e52b2f503c03e03090d50be2a61b8')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-rdflib@4.2.2:5.999', type=('build', 'run'))
    depends_on('py-rdflib-jsonld', type=('build', 'run'))
    depends_on('py-owlrl@5.2.1:', type=('build', 'run'))
