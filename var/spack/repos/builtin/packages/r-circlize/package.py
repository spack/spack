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


class RCirclize(RPackage):
    """Circular layout is an efficient way for the visualization of huge
       amounts of information. Here this package provides an implementation
       of circular layout generation in R as well as an enhancement of
       available software. The flexibility of the package is based on the
       usage of low-level graphics functions such that self-defined
       high-level graphics can be easily implemented by users for specific
       purposes. Together with the seamless connection between the powerful
       computational and visual environment in R, it gives users more
       convenience and freedom to design figures for better understanding
       complex patterns behind multiple dimensional data."""

    homepage = "https://cran.r-project.org/package=circlize"
    url      = "https://cran.r-project.org/src/contrib/circlize_0.4.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/circlize"

    version('0.4.1', '6818830654f485abbdc8c74ec9087377')
    version('0.4.0', '0dbf1b481930a759d6f413d17f8ae1c4')

    depends_on('r-globaloptions', type=('build', 'run'))
    depends_on('r-shape', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
