##############################################################################
# Copyright (c) 2017 Christian Schulz
# Karlsruhe Institute of Technology (KIT), Karlsruhe, Germany
#
# This file is released as part of Spack under the LGPL license
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE file for the LLNL notice and LGPL.
#
# License
# -------
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

import os
import re


class Kahip(SConsPackage):
    """KaHIP - Karlsruhe High Quality Partitioning - is a family of graph
    partitioning programs. It includes KaFFPa (Karlsruhe Fast Flow
    Partitioner), which is a multilevel graph partitioning algorithm,
    in its variants Strong, Eco and Fast, KaFFPaE (KaFFPaEvolutionary)
    which is a parallel evolutionary algorithm that uses KaFFPa to
    provide combine and mutation operations, as well as KaBaPE which
    extends the evolutionary algorithm. Moreover, specialized
    techniques are included to partition road networks (Buffoon), to
    output a vertex separator from a given partition or techniques
    geared towards efficient partitioning of social networks.
    """

    homepage  = 'http://algo2.iti.kit.edu/documents/kahip/index.html'
    url       = 'http://algo2.iti.kit.edu/schulz/software_releases/KaHIP_2.00.tar.gz'
    git       = 'https://github.com/schulzchristian/KaHIP.git'

    version('develop', branch='master')
    version('2.00', '0a66b0a604ad72cfb7e3dce00e2c9fdfac82b855')

    depends_on('argtable')
    depends_on('mpi')  # Note: upstream package only tested on openmpi

    conflicts('%clang')

    def patch(self):
        """Internal compile.sh scripts hardcode number of cores to build with.
        Filter these out so Spack can control it."""

        files = [
            'compile.sh',
            'parallel/modified_kahip/compile.sh',
            'parallel/parallel_src/compile.sh',
        ]

        for f in files:
            filter_file('NCORES=.*', 'NCORES={0}'.format(make_jobs), f)

    def build(self, spec, prefix):
        """Build using the KaHIP compile.sh script. Uses scons internally."""
        builder = Executable('./compile.sh')
        builder()

    def install(self, spec, prefix):
        """Install under the prefix"""
        # Ugly: all files land under 'deploy' and we need to disentangle them
        mkdirp(prefix.bin)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        with working_dir('deploy'):
            for f in os.listdir('.'):
                if re.match(r'.*\.(a|so|dylib)$', f):
                    install(f, prefix.lib)
                elif re.match(r'.*\.h$', f):
                    install(f, prefix.include)
                else:
                    install(f, prefix.bin)
