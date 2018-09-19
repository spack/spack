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


class Poamsa(MakefilePackage):
    """POA is Partial Order Alignment, a fast program for multiple sequence
       alignment in bioinformatics. Its advantages are speed, scalability,
       sensitivity, and the superior ability to handle branching / indels
       in the alignment."""

    homepage = "https://sourceforge.net/projects/poamsa"
    url      = "https://downloads.sourceforge.net/project/poamsa/poamsa/2.0/poaV2.tar.gz"

    version('2.0', '9e2eb270d4867114406f53dab1311b2b')

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/poamsa/poamsa/{0}/poaV{1}.tar.gz"
        return url.format(version.dotted, version.up_to(1))

    def build(self, spec, prefix):
        make('poa')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        install('poa', prefix.bin)
        install('liblpo.a', prefix.lib)
