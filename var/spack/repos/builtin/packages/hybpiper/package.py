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
import os


class Hybpiper(Package):
    """HybPiper was designed for targeted sequence capture, in which DNA
       sequencing libraries are enriched for gene regions of interest,
       especially for phylogenetics. HybPiper is a suite of Python scripts
       that wrap and connect bioinformatics tools in order to extract target
       sequences from high-throughput DNA sequencing reads"""

    homepage = "https://github.com/mossmatters/HybPiper"
    url      = "https://github.com/mossmatters/HybPiper/archive/v1.2.0.tar.gz"

    version('1.2.0', '0ad78e9ca5e3f23ae0eb6236b07e1780')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-biopython', type=('build', 'run'))
    depends_on('exonerate')
    depends_on('blast-plus')
    depends_on('spades')
    depends_on('parallel')
    depends_on('bwa')
    depends_on('samtools')

    def setup_envionment(self, spack_env, run_env):
        run_env.set('HYBPIPER_HOME', prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.iglob("*.py")
        for file in files:
            if os.path.isfile(file):
                install(file, prefix.bin)
