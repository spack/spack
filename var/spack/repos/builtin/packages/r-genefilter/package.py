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


class RGenefilter(RPackage):
    """Some basic functions for filtering genes"""

    homepage = "https://bioconductor.org/packages/genefilter/"
    git      = "https://git.bioconductor.org/packages/genefilter.git"

    version('1.62.0', commit='eb119894f015c759f93f458af7733bdb770a22ad')
    version('1.58.1', commit='ace2556049677f60882adfe91f8cc96791556fc2')

    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.58.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.62.0', type=('build', 'run'))
