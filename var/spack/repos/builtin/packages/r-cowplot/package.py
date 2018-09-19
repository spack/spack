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


class RCowplot(RPackage):
    """Some helpful extensions and modifications to the 'ggplot2'
    package. In particular, this package makes it easy to combine
    multiple 'ggplot2' plots into one and label them with letters,
    e.g. A, B, C, etc., as is often required for scientific
    publications. The package also provides a streamlined and clean
    theme that is used in the Wilke lab, hence the package name,
    which stands for Claus O. Wilke's plot package."""

    homepage = "https://cran.r-project.org/package=cowplot"
    url      = "https://cran.rstudio.com/src/contrib/cowplot_0.8.0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/cowplot"

    version('0.8.0', 'bcb19c72734d8eb5d73db393c1235c3d')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
