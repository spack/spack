# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class SnapKorf(MakefilePackage):
    """SNAP is a general purpose gene finding program suitable for both
       eukaryotic and prokaryotic genomes."""

    homepage = "http://korflab.ucdavis.edu/software.html"
    url      = "http://korflab.ucdavis.edu/Software/snap-2013-11-29.tar.gz"

    version('2013-11-29', 'dfdf48e37cdb32af4eecd9201506b6e3')

    depends_on('perl', type=('build', 'run'))
    depends_on('boost')
    depends_on('sqlite')
    depends_on('sparsehash')

    conflicts('%gcc@5:', when='@2013-11-29')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        progs  = ['snap', 'fathom', 'forge', 'depend', 'exonpairs', 'hmm-info']
        for p in progs:
            install(p, prefix.bin)

        files = glob.iglob('*.pl')
        for file in files:
            install(file, prefix.bin)

        install_tree('Zoe', prefix.Zoe)
        install_tree('HMM', prefix.HMM)
        install_tree('DNA', prefix.DNA)

    def setup_environment(self, spack_env, run_env):
        run_env.set('ZOE', self.prefix)
        run_env.prepend_path('PATH', self.prefix)
