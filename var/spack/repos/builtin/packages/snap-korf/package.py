##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
