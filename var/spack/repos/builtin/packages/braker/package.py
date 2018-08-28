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


class Braker(Package):
    """BRAKER is a pipeline for unsupervised RNA-Seq-based genome annotation
       that combines the advantages of GeneMark-ET and AUGUSTUS"""

    homepage = "http://exon.gatech.edu/braker1.html"
    url      = "http://bioinf.uni-greifswald.de/augustus/binaries/BRAKER_v2.1.0.tar.gz"
    list_url = "http://bioinf.uni-greifswald.de/augustus/binaries/old"

    version('2.1.0', '5f974abcceb9f96a11668fa20a6f6a56')
    version('1.11', '297efe4cabdd239b710ac2c45d81f6a5',
            url='http://bioinf.uni-greifswald.de/augustus/binaries/old/BRAKER1_v1.11.tar.gz')

    depends_on('perl', type=('build', 'run'))
    depends_on('augustus@3.2.3')
    depends_on('genemark-et')
    depends_on('bamtools')
    depends_on('samtools')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        install('braker.pl', prefix.bin)
        install('filterGenemark.pl', prefix.bin)
        install('filterIntronsFindStrand.pl', prefix.bin)
        install('helpMod.pm', prefix.lib)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', prefix.lib)
