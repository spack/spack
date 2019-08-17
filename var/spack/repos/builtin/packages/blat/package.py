# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Blat(Package):
    """BLAT (BLAST-like alignment tool) is a pairwise sequence
       alignment algorithm."""

    homepage = "https://genome.ucsc.edu/FAQ/FAQblat.html"
    url      = "https://users.soe.ucsc.edu/~kent/src/blatSrc35.zip"

    version('35', '16e546b8843b85e0b0f2fa603cd78724')

    depends_on('libpng')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('MACHTYPE', 'x86_64')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("BINDIR=%s" % prefix.bin)
