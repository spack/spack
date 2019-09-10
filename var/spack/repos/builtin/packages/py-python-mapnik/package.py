# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonMapnik(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/mapnik/python-mapnik/archive/v3.0.16.tar.gz"

    version('3.0.16', sha256='643117752fa09668a1e26a360d13cd137329ae2013eb14ad92ab72fbc479fc70')
    version('3.0.13', sha256='ced684745e778c0cac0edba89c09c6f9b9f1db18fc12744ed4710a88b78a3389')

    depends_on('py-setuptools', type='build')
    depends_on('mapnik', type=('build', 'link', 'run'))

#    def install(self, spec, prefix):
#        # FIXME: Unknown build system
#        make()
#        make('install')
