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


class RAffycoretools(RPackage):
    """Various wrapper functions that have been written to streamline
    the more common analyses that a core Biostatistician might see."""

    homepage = "https://www.bioconductor.org/packages/affycoretools/"
    git      = "https://git.bioconductor.org/packages/affycoretools.git"

    version('1.48.0', commit='e0d52e34eead1ac45d3e60c59efd940e4889eb99')

    depends_on('r@3.4.0:3.4.9', when='@1.48.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-gostats', type=('build', 'run'))
    depends_on('r-gcrma', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-oligoclasses', type=('build', 'run'))
    depends_on('r-reportingtools', type=('build', 'run'))
    depends_on('r-hwriter', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
