# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyspatialite(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://files.pythonhosted.org/packages/cc/2a/ffb126f3e8890ab0da951a83906e54528a13ce4b913303dea8bed904e160/pyspatialite-3.0.1-alpha-0.tar.gz"

    version('3.0.1-alpha-0', sha256='f7e135cd5e592b3a0d6627863b46442cb4407ab5a05c6004e73453e078274478')
    version('2.6.2', sha256='63775f20c1c02533477bd89372e6b27b9dde681358ad8ae971ff64c2a9ea702f')

    depends_on('py-setuptools', type='build')
    depends_on('libspatialite', type=('build', 'link', 'run'))
    depends_on('proj@:5')
    depends_on('geos')
    depends_on('freexl')
    depends_on('python@:2.8')

#    def install(self, spec, prefix):
#        # FIXME: Unknown build system
#        make()
#        make('install')
