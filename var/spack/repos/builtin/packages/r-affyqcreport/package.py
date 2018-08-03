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


class RAffyqcreport(RPackage):
    """This package creates a QC report for an AffyBatch object.
    The report is intended to allow the user to quickly assess the
    quality of a set of arrays in an AffyBatch object."""

    homepage = "https://www.bioconductor.org/packages/affyQCReport/"
    git      = "https://git.bioconductor.org/packages/affyQCReport.git"

    version('1.54.0', commit='5572e9981dc874b78b4adebf58080cac3fbb69e1')

    depends_on('r@3.4.0:3.4.9', when='@1.54.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-affyplm', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-simpleaffy', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
