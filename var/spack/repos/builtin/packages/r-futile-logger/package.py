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


class RFutileLogger(RPackage):
    """Provides a simple yet powerful logging utility. Based loosely on log4j,
       futile.logger takes advantage of R idioms to make logging a convenient
       and easy to use replacement for cat and print statements."""

    homepage = "https://cran.rstudio.com/web/packages/futile.logger/index.html"
    url      = "https://cran.rstudio.com/src/contrib/futile.logger_1.4.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/futile.logger"

    version('1.4.3', 'ba0e8d2dfb5a970b51c21907bbf8bfc2')

    depends_on('r-lambda-r', type=('build', 'run'))
    depends_on('r-futile-options', type=('build', 'run'))
