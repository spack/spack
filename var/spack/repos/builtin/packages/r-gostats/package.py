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


class RGostats(RPackage):
    """A set of tools for interacting with GO and microarray data.
    A variety of basic manipulation tools for graphs, hypothesis
    testing and other simple calculations."""

    homepage = "https://www.bioconductor.org/packages/GOstats/"
    git      = "https://git.bioconductor.org/packages/GOstats.git"

    version('2.42.0', commit='8b29709064a3b66cf1d963b2be0c996fb48c873e')

    depends_on('r@3.4.1:3.4.9', when='@2.42.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-category', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-annotationforge', type=('build', 'run'))
