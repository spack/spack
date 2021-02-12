# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCherrypy(PythonPackage):
    """CherryPy is a pythonic, object-oriented HTTP framework."""

    homepage = "https://cherrypy.org/"
    pypi = "CherryPy/CherryPy-18.1.1.tar.gz"

    version('18.6.0', sha256='56608edd831ad00991ae585625e0206ed61cf1a0850e4b2cc48489fb2308c499')
    version('18.5.0', sha256='63b2f61c38c469112145bd4e4e2385cd18f3233799e7a33bd447df468916d22b')
    version('18.4.0', sha256='e5be00304ca303d7791d14b5ce1436428e18939b91806250387c363ae56c8f8f')
    version('18.3.0', sha256='683e687e7c7b1ba31ef86a113b1eafd0407269fed175bf488d3c839d37d1cc60')
    version('18.2.0', sha256='16fc226a280cd772ede7c309d3964002196784ac6615d8bface52be12ff51230')
    version('18.1.2', sha256='48de31ba3db04c5354a0fcf8acf21a9c5190380013afca746d50237c9ebe70f0')
    version('18.1.1', sha256='6585c19b5e4faffa3613b5bf02c6a27dcc4c69a30d302aba819639a2af6fa48b')

    depends_on('py-setuptools',     type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-more-itertools', type=('build', 'run'))
    depends_on('py-zc-lockfile',    type=('build', 'run'))
    depends_on('py-cheroot@6.2.4:', type=('build', 'run'))
    depends_on('py-portend@2.1.1:', type=('build', 'run'))
    depends_on('python@3.5:',       when='@18.0.0:',  type=('build', 'run'))
