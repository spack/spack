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
import os


class Trinotate(Package):
    """Trinotate is a comprehensive annotation suite designed for
       automatic functional annotation of transcriptomes, particularly
       de novo assembled transcriptomes, from model or non-model organisms"""

    homepage = "https://trinotate.github.io/"
    url      = "https://github.com/Trinotate/Trinotate/archive/Trinotate-v3.1.1.tar.gz"

    version('3.1.1', sha256='f8af0fa5dbeaaf5a085132cd4ac4f4206b05cc4630f0a17a672c586691f03843')

    depends_on('trinity', type='run')
    depends_on('transdecoder', type='run')
    depends_on('sqlite', type='run')
    depends_on('ncbi-rmblastn', type='run')
    depends_on('hmmer', type='run')
    depends_on('perl', type='run')
    depends_on('lighttpd', type='run')
    depends_on('perl-dbi', type='run')
    depends_on('perl-dbd-mysql', type='run')
    depends_on('perl-cgi', type='run')

    def install(self, spec, prefix):
        # most of the perl modules have local deps, install the whole tree
        mkdirp(prefix.lib)
        install_tree('.', join_path(prefix.lib, 'trinotate'))

        mkdirp(prefix.bin)
        os.symlink(join_path(prefix.lib, 'trinotate/Trinotate'),
                   join_path(prefix.bin, 'Trinotate'))

        os.symlink(join_path(prefix.lib,
                             'trinotate/run_TrinotateWebserver.pl'),
                   join_path(prefix.bin, 'run_TrinotateWebserver.pl'))
