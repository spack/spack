##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class PrinseqLite(Package):
    """PRINSEQ will help you to preprocess your genomic or metagenomic
    sequence data in FASTA or FASTQ format."""

    homepage = "http://prinseq.sourceforge.net"
    url      = "https://sourceforge.net/projects/prinseq/files/standalone/prinseq-lite-0.20.4.tar.gz"

    version('0.20.4', '3be1a572073ebbbecfeba42a42853ff5')

    variant('nopca', default=True, description="Graphs version without PCA")

    depends_on('perl', type='run')
    depends_on('perl-cairo', type='run')
    depends_on('perl-digest-md5', type='run')
    depends_on('perl-json', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl',
                    'prinseq-graphs-noPCA.pl')

        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl',
                    'prinseq-lite.pl')

        install('prinseq-graphs-noPCA.pl', prefix.bin)
        install('prinseq-lite.pl', prefix.bin)

        chmod = which('chmod')
        chmod('+x', join_path(self.prefix.bin, 'prinseq-graphs-noPCA.pl'))
        chmod('+x', join_path(self.prefix.bin, 'prinseq-lite.pl'))
