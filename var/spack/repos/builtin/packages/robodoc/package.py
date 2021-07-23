# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Robodoc(AutotoolsPackage):
    """ROBODoc is program documentation tool."""

    homepage = "https://www.xs4all.nl/~rfsber/Robo/index.html"
    url      = "https://github.com/gumpu/ROBODoc/archive/refs/tags/v4.99.44.tar.gz"

    maintainers = ['wscullin']

    version('develop', git='https://github.com/gumpu/ROBODoc.git')
    version('4.99.44', sha256='8ed875bbde2788d7bc986693077577d6cc6e15e4bc660d522164710977952e90')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def autoreconf(self, spec, prefix):
        autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        args = []
        return args
