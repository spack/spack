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


class RQuantro(RPackage):
    """A data-driven test for the assumptions of quantile normalization using
       raw data such as objects that inherit eSets (e.g. ExpressionSet,
       MethylSet). Group level information about each sample (such as
       Tumor / Normal status) must also be provided because the test assesses
       if there are global differences in the distributions between the
       user-defined groups."""

    homepage = "https://www.bioconductor.org/packages/quantro/"
    git      = "https://git.bioconductor.org/packages/quantro.git"

    version('1.10.0', commit='111337c0aba052aa49c3d2e2d3042794b28858c9')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-minfi', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.10.0')
