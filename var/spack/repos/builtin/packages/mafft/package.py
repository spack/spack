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


class Mafft(Package):
    """MAFFT is a multiple sequence alignment program for unix-like
       operating systems.  It offers a range of multiple alignment
       methods, L-INS-i (accurate; for alignment of <~200 sequences),
       FFT-NS-2 (fast; for alignment of <~30,000 sequences), etc."""

    homepage = "http://mafft.cbrc.jp/alignment/software/index.html"
    url      = "http://mafft.cbrc.jp/alignment/software/mafft-7.221-with-extensions-src.tgz"

    version('7.221', 'b1aad911e51024d631722a2e061ba215')

    def install(self, spec, prefix):
        with working_dir('core'):
            make('PREFIX=%s' % prefix)
            make('PREFIX=%s' % prefix, 'install')
