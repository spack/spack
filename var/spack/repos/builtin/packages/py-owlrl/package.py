# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyOwlrl(PythonPackage):
    """A simple implementation of the OWL2 RL Profile, as well as a basic
    RDFS inference, on top of RDFLib. Based mechanical forward chaining.
    """

    homepage = "https://github.com/RDFLib/OWL-RL"
    url = "https://pypi.io/packages/source/o/owlrl/owlrl-5.2.3.tar.gz"

    version('5.2.3', sha256='b1891d75b2c2fb0db9e1504a9b12dab738ed89236414c51393d1030597004342')

    depends_on('py-setuptools', type='build')
    depends_on('py-rdflib@5.0.0:', type=('build', 'run'))
