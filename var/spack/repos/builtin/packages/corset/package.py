# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Corset(Package):
    """Corset is a command-line software program to go from a de novo
       transcriptome assembly to gene-level counts."""

    homepage = "https://github.com/Oshlack/Corset/wiki"
    url      = "https://github.com/Oshlack/Corset/releases/download/version-1.06/corset-1.06-linux64.tar.gz"

    version('1.06', '0a6d0bb1f2d1bdbcb8b47656a7f12f23')

    def url_for_version(self, version):
        url = 'https://github.com/Oshlack/Corset/releases/download/version-{0}/corset-{0}-linux64.tar.gz'
        return url.format(version)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('corset', prefix.bin)
        install('corset_fasta_ID_changer', prefix.bin)
