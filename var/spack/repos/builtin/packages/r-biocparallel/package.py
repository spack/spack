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


class RBiocparallel(RPackage):
    """This package provides modified versions and novel implementation of
       functions for parallel evaluation, tailored to use with Bioconductor
       objects."""

    homepage = "https://bioconductor.org/packages/BiocParallel/"
    url      = "https://bioconductor.org/packages/3.5/bioc/src/contrib/BiocParallel_1.10.1.tar.gz"
    list_url = homepage

    version('1.10.1', '0b587026c0e2c5945be1d84deb12d7dd')

    depends_on('r-futile-logger', type=('build', 'run'))
    depends_on('r-snow', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.10.1')
