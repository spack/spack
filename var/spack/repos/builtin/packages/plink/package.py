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


class Plink(Package):
    """PLINK is a free, open-source whole genome association analysis toolset,
       designed to perform a range of basic, large-scale analyses in a
       computationally efficient manner."""

    homepage = "https://www.cog-genomics.org/plink/1.9/"

    version('1.9', 'a2325881594856c0f1b7523290d1e04f',
            url='https://www.cog-genomics.org/static/bin/plink170815/plink_linux_x86_64.zip')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('plink', prefix.bin)
        install('prettify', prefix.bin)
