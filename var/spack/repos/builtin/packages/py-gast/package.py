# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-gast
#
# You can edit this file again by typing:
#
#     spack edit py-gast
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyGast(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://pypi.io/packages/source/g/gast/gast-0.3.2.tar.gz"

    version('0.3.2', sha256='5c7617f1f6c8b8b426819642b16b9016727ddaecd16af9a07753e537eba8a3a5')

    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

#    def install(self, spec, prefix):
#        # FIXME: Unknown build system
#        make()
#        make('install')
