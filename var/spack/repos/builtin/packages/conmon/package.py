# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Conmon(MakefilePackage):
    """An OCI container runtime monitor"""

    homepage    = 'https://github.com/containers/conmon'
    url         = 'https://github.com/containers/conmon/archive/v2.0.30.tar.gz'
    maintainers = ['bernhardkaindl']

    version('2.0.30', sha256='4b0a98fbe8a63c42f60edac25c19aa6606caa7b1e4fe7846fc7f7de0b566ba25')

    depends_on('go',         type='build')
    depends_on('go-md2man',  type='build')
    depends_on('pkgconfig',  type='build')
    depends_on('libseccomp')
    depends_on('glib')

    def install(self, spec, prefix):
        make('install', 'PREFIX=' + prefix)
