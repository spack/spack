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


class RRappdirs(RPackage):
    """An easy way to determine which directories on the users computer
    you should use to save data, caches and logs. A port of Python's
    'Appdirs' to R."""

    homepage = "https://cran.r-project.org/package=rappdirs"
    url      = "https://cran.rstudio.com/src/contrib/rappdirs_0.3.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/rappdirs"

    version('0.3.1', 'fbbdceda2aa49374e61c7d387bf9ea21')

    depends_on('r@2.14:', type=('build', 'run'))
