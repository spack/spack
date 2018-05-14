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


class Hisea(MakefilePackage):
    """HISEA is an efficient all-vs-all long read aligner for SMRT sequencing
       data. Its algorithm is designed to produce highest alignment sensitivity
       among others."""

    homepage = "https://doi.org/10.1186/s12859-017-1953-9"
    url      = "https://github.com/lucian-ilie/HISEA"

    version('2017.12.26', '54211bdc33b7ce52a8f1e76845935eb8',
            url='https://github.com/lucian-ilie/HISEA/tarball/39e01e98caa0f2101da806ca59306296effe789c')

    depends_on('boost')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('hisea', prefix.bin)
