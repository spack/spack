##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class RA4classif(RPackage):
    """Automated Affymetrix Array Analysis Classification Package."""

    homepage = "https://www.bioconductor.org"
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/a4Classif_1.24.0.tar.gz"
    list_url = homepage

    version('1.24.0', 'b3367ba63a5d5a38d94e671d027098ff')

    depends_on('r-a4core', type=('build', 'run'))
    depends_on('r-a4preproc', type=('build', 'run'))
    depends_on('r-mlinterfaces', type=('build', 'run'))
    depends_on('r-rocr', type=('build', 'run'))
    depends_on('r-pamr', type=('build', 'run'))
    depends_on('r-glmnet', type=('build', 'run'))
    depends_on('r-varselrf', type=('build', 'run'))
