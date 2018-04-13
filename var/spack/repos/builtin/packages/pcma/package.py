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


class Pcma(MakefilePackage):
    """PCMA is a progressive multiple sequence alignment program that combines
       two different alignment strategies."""

    homepage = "http://prodata.swmed.edu/pcma/pcma.php"
    url      = "http://prodata.swmed.edu/download/pub/PCMA/pcma.tar.gz"

    version('2.0', 'e78449b2f6b0e90348a0a6747d266f9b')

    def edit(self, spec, prefix):
        makefile = FileFilter('makefile')
        makefile.filter('gcc', spack_cc)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('pcma', prefix.bin)
