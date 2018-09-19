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


class RVcd(RPackage):
    """Visualization techniques, data sets, summary and inference procedures
    aimed particularly at categorical data. Special emphasis is given to highly
    extensible grid graphics. The package was package was originally inspired
    by the book "Visualizing Categorical Data" by Michael Friendly and is now
    the main support package for a new book, "Discrete Data Analysis with R" by
    Michael Friendly and David Meyer (2015)."""

    homepage = "https://cran.r-project.org/package=vcd"
    url      = "https://cran.r-project.org/src/contrib/vcd_1.4-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/vcd"

    version('1.4-1', '7db150a77f173f85b69a1f86f73f8f02')

    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-lmtest', type=('build', 'run'))
