# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install libjwt
#
# You can edit this file again by typing:
#
#     spack edit libjwt
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Libjwt(AutotoolsPackage):
    """libjwt JSON Web Token C Library"""

    git      = "https://github.com/benmcollins/libjwt"
    url      = "https://github.com/benmcollins/libjwt/archive/v1.12.0.tar.gz"

    maintainers = ['bollig']

    version('1.12.0', sha256='eaf5d8b31d867c02dde767efa2cf494840885a415a3c9a62680bf870a4511bee')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('jansson')

    def install(self, spec, prefix):
        make('install')
