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


class RPcapp(RPackage):
        """Provides functions for robust PCA by projection pursuit."""

        homepage = "https://cran.r-project.org/web/packages/pcaPP/index.html"
        url      = "https://cran.r-project.org/src/contrib/pcaPP_1.9-72.tar.gz"
        list_url = "https://cran.rstudio.com/src/contrib/Archive/pcaPP"

        version('1.9-72', '87c08f8ecab69311bba395c026bbc91c')
        version('1.9-70', '3fcc809ec1cdc910f10e9ebf372888e8')
        version('1.9-61', '1bd5bc3aff968b168493e8c523d726ea')
        version('1.9-60', '23dd468abb9fedc11e40166446df1017')
        version('1.9-50', 'be44f173404fd6e86ba0a5515711bfa3')

        depends_on('r@3.4.0:3.4.9')
        depends_on('r-mvtnorm', type=('build', 'run'))
