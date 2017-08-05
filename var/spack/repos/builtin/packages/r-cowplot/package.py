##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
    """Some helpful extensions and modifications to the 'ggplot2' package. In
    particular, this package makes it easy to combine multiple 'ggplot2' plots
    into one and label them with letters, e.g. A, B, C, etc., as is often
    required for scientific publications. The package also provides a
    streamlined and clean theme that is used in the Wilke lab, hence the
    package name, which stands for Claus O. Wilke's plot package."""

    homepage = "https://github.com/wilkelab/cowplot"
    url      = "https://cran.r-project.org/src/contrib/cowplot_0.7.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/cowplot"

    version('0.7.0', '31c395c190e8da646a53ce5593ea64ab')

    depends_on('r@3.3.0:', type=('build', 'run'))

    depends_on('r-ggplot2@2.1.0:', type=('build', 'run'))
    depends_on('r-gtable@0.1.2:', type=('build', 'run'))
    depends_on('r-plyr@1.8.2:', type=('build', 'run'))
