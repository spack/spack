# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.executable import which


class Hugo(Package):
    """The world's fastest framework for building websites."""

    homepage = "https://gohugo.io"
    url      = "https://github.com/gohugoio/hugo/archive/v0.53.tar.gz"

    version('0.53', sha256='48e65a33d3b10527101d13c354538379d9df698e5c38f60f4660386f4232e65c')

    # Uses go modules.
    # See https://gohugo.io/getting-started/installing/#fetch-from-github
    depends_on('go@1.11:', when='@0.48:', type='build')

    def install(self, spec, prefix):
        go = which('go')
        go('build')
        mkdir(prefix.bin)
        install('hugo', prefix.bin)
