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


class DeconseqStandalone(Package):
    """The DeconSeq tool can be used to automatically detect and efficiently
    remove sequence contaminations from genomic and metagenomic datasets."""

    homepage = "http://deconseq.sourceforge.net"
    url      = "https://sourceforge.net/projects/deconseq/files/standalone/deconseq-standalone-0.4.3.tar.gz"

    version('0.4.3', 'cb3fddb90e584d89fd9c2b6b8f2e20a2')

    depends_on('perl@5:')

    def install(self, spec, prefix):

        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl', 'deconseq.pl')
        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl', 'splitFasta.pl')

        mkdirp(prefix.bin)
        install('bwa64', prefix.bin)
        install('bwaMAC', prefix.bin)
        install('deconseq.pl', prefix.bin)
        install('splitFasta.pl', prefix.bin)
        install('DeconSeqConfig.pm', prefix)

        chmod = which('chmod')
        chmod('+x', join_path(prefix.bin, 'bwa64'))
        chmod('+x', join_path(prefix.bin, 'bwaMAC'))
        chmod('+x', join_path(prefix.bin, 'deconseq.pl'))
        chmod('+x', join_path(prefix.bin, 'splitFasta.pl'))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PERL5LIB', prefix)
