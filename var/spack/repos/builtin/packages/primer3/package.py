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


class Primer3(MakefilePackage):
    """Primer3 is a widely used program for designing PCR primers
       (PCR = "Polymerase Chain Reaction"). PCR is an essential and
       ubiquitous tool in genetics and molecular biology. Primer3
       can also design hybridization probes and sequencing primers."""

    homepage = "http://primer3.sourceforge.net/"
    url      = "https://sourceforge.net/projects/primer3/files/primer3/2.3.7/primer3-2.3.7.tar.gz/download"

    version('2.3.7', 'c6b89067bf465e62b6b1fd830b5b4418')

    build_directory = 'src'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            for binary in ('primer3_core', 'ntdpal', 'oligotm',
                           'long_seq_tm_test'):
                install(binary, prefix.bin)
