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


class RPlyr(RPackage):
    """A set of tools that solves a common set of problems: you need to break a
    big problem down into manageable pieces, operate on each piece and then put
    all the pieces back together. For example, you might want to fit a model to
    each spatial location or time point in your study, summarise data by panels
    or collapse high-dimensional arrays to simpler summary statistics. The
    development of 'plyr' has been generously supported by 'Becton
    Dickinson'."""

    homepage = "http://had.co.nz/plyr"
    url      = "https://cran.r-project.org/src/contrib/plyr_1.8.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/plyr"

    version('1.8.4', 'ef455cf7fc06e34837692156b7b2587b')

    depends_on('r-rcpp', type=('build', 'run'))
