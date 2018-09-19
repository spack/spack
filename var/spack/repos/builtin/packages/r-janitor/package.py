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


class RJanitor(RPackage):
    """The main janitor functions can: perfectly format data.frame column
       names; provide quick one- and two-variable tabulations (i.e., frequency
       tables and crosstabs); and isolate duplicate records. Other janitor
       functions nicely format the tabulation results. These
       tabulate-and-report functions approximate popular features of SPSS and
       Microsoft Excel. This package follows the principles of the "tidyverse"
       and works well with the pipe function %>%. janitor was built with
       beginning-to-intermediate R users in mind and is optimized for
       user-friendliness. Advanced R users can already do everything covered
       here, but with janitor they can do it faster and save their thinking
       for the fun stuff."""

    homepage = "https://github.com/sfirke/janitor"
    url      = "https://cran.r-project.org/src/contrib/janitor_0.3.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/janitor"

    version('0.3.0', '76036c54693b91aef19d468107ae066a')

    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
