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


class RHttr(RPackage):
    """Useful tools for working with HTTP organised by HTTP verbs (GET(),
    POST(), etc). Configuration functions make it easy to control additional
    request components (authenticate(), add_headers() and so on)."""

    homepage = "https://github.com/hadley/httr"
    url      = "https://cran.r-project.org/src/contrib/httr_1.2.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/httr"

    version('1.2.1', 'c469948dedac9ab3926f23cf484b33d9')
    version('1.1.0', '5ffbbc5c2529e49f00aaa521a2b35600')

    depends_on('r@3.0.0:')

    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-mime', type=('build', 'run'))
    depends_on('r-curl@0.9.1:', type=('build', 'run'))
    depends_on('r-openssl', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
