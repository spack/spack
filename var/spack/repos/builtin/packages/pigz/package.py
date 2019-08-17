# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pigz(MakefilePackage):
    """A parallel implementation of gzip for modern multi-processor,
       multi-core machines."""

    homepage = "http://zlib.net/pigz/"
    url      = "https://github.com/madler/pigz/archive/v2.3.4.tar.gz"

    version('2.4', '3c8a601db141d3013ef9fe5f2daaf73f')
    version('2.3.4', 'c109057050b15edf3eb9bb4d0805235e')

    depends_on('zlib')

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)
        install('pigz', "%s/pigz" % prefix.bin)
        install('pigz.1', "%s/pigz.1" % prefix.man.man1)
