# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vt(MakefilePackage):
    """A tool set for short variant discovery in genetic sequence data."""

    homepage = "http://genome.sph.umich.edu/wiki/vt"
    url      = "https://github.com/atks/vt/archive/0.577.tar.gz"

    version('0.577',  '59807456022bcecf978314c93254fe15')

    depends_on('zlib')

    def install(self, spec, spack):
        mkdirp(prefix.bin)
        install('vt', prefix.bin)
