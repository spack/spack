# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install robodoc
#
# You can edit this file again by typing:
#
#     spack edit robodoc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Robodoc(AutotoolsPackage):
    """ROBODoc is program documentation tool."""

    homepage = "http://www.xs4all.nl/~rfsber/Robo/index.html"
    url      = "https://github.com/gumpu/ROBODoc/archive/refs/tags/v4.99.44.tar.gz"

    maintainers = ['wscullin']

    version('4.99.44', sha256='8ed875bbde2788d7bc986693077577d6cc6e15e4bc660d522164710977952e90')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')


    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def autoreconf(self, spec, prefix):
        # FIXME: Modify the autoreconf method as necessary
        autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        args = []
        return args
