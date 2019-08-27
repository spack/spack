# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPlanar(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://pypi.io/packages/source/p/planar/planar-0.4.zip"

    version('0.4', sha256='cbfb9cbae8b0e296e6e7e3552b7d685c7ed5cae295b7a61f2b2b096b231dad76')

    # FIXME: Add dependencies if required.
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))

#    def install(self, spec, prefix):
#        # FIXME: Unknown build system
#        make()
#        make('install')
