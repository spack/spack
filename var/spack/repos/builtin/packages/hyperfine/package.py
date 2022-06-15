# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hyperfine(Package):
    """A command-line benchmarking tool."""

    homepage = "https://github.com/sharkdp/hyperfine"
    url      = "https://github.com/sharkdp/hyperfine/archive/refs/tags/v1.12.0.tar.gz"

    maintainers = ['michaelkuhn']

    version('1.13.0', sha256='6e57c8e51962dd24a283ab46dde6fe306da772f4ef9bad86f8c89ac3a499c87e')
    version('1.12.0', sha256='2120870a97e68fa3426eac5646a071c9646e96d2309220e3c258bf588e496454')

    depends_on('rust@1.46:')

    def install(self, spec, prefix):
        cargo = which('cargo')
        cargo('install', '--root', prefix, '--path', '.')
