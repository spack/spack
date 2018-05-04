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


class RGgjoy(RPackage):
    """Joyplots provide a convenient way of visualizing changes in distributions
    over time or space."""

    homepage = "https://cran.r-project.org/web/packages/ggjoy/index.html"
    url      = "https://cran.r-project.org/src/contrib/ggjoy_0.4.0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/ggjoy"

    version('0.4.0', 'c63782e2395a9cfc435d08e078e6596b')
    version('0.3.0', '59bd34a846270d43f2eeb1e90b03a127')
    version('0.2.0', '8584cd154e228f8505b324e91d2e50d7')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggridges', type=('build', 'run'))
