# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Aragorn(Package):
    """ARAGORN, a program to detect tRNA genes and tmRNA genes in nucleotide
    sequences."""

    homepage = "http://mbio-serv2.mbioekol.lu.se/ARAGORN"
    url      = "http://mbio-serv2.mbioekol.lu.se/ARAGORN/Downloads/aragorn1.2.38.tgz"

    version('1.2.38', '1df0ed600069e6f520e5cd989de1eaf0')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        cc = Executable(spack_cc)
        cc('-O3', '-ffast-math', '-finline-functions',
           '-oaragorn', 'aragorn' + format(spec.version.dotted) + '.c')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('aragorn', prefix.bin)
