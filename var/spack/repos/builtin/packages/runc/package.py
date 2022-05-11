# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Runc(MakefilePackage):
    """CLI tool for spawning containers on Linux according to the OCI specification"""

    homepage    = 'https://github.com/opencontainers/runc'
    url         = 'https://github.com/opencontainers/runc/releases/download/v1.0.2/runc.tar.xz'
    maintainers = ['bernhardkaindl']

    version('1.0.2', sha256='740acb49e33eaf4958b5109c85363c1d3900f242d4cab47fbdbefa6f8f3c6909')

    depends_on('go',          type='build')
    depends_on('go-md2man',   type='build')
    depends_on('pkgconfig',   type='build')
    depends_on('libseccomp')

    def install(self, spec, prefix):
        make('install', 'PREFIX=' + prefix)
