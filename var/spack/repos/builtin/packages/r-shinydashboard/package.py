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


class RShinydashboard(RPackage):
    """Create Dashboards with 'Shiny'"""

    homepage = "https://cran.r-project.org/package=shinydashboard"
    url      = "https://cran.r-project.org/src/contrib/shinydashboard_0.7.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/shinydashboard"

    version('0.7.0', 'a572695884e3b45320b0ab5a7b364ffd')
    version('0.6.1', '0f6ad0448237e10d53d4d27ade1c6863')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-htmltools@0.2.6:', type=('build', 'run'))
    depends_on('r-shiny@1.0.0:', type=('build', 'run'))
