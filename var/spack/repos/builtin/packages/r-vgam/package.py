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


class RVgam(RPackage):
    """An implementation of about 6 major classes of statistical regression
    models."""

    homepage = "https://cran.r-project.org/web/packages/VGAM/index.html"
    url      = "https://cran.r-project.org/src/contrib/VGAM_1.0-4.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/VGAM"

    version('1.0-4', '9d30736842db6d9dcec83df49f11d3c1')
    version('1.0-3', 'a158cd0a6ff956b4bf21d610df361b18')
    version('1.0-2', '813b303d5d956914cf8910db3fa1ba14')
    version('1.0-1', '778182585c774036ac3d10240cf63b40')
    version('1.0-0', '81da7b3a797b5e26b9e859dc2f373b7b')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
