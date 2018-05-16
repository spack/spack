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


class RForeach(RPackage):
    """Support for the foreach looping construct. Foreach is an idiom that
    allows for iterating over elements in a collection, without the use of an
    explicit loop counter. This package in particular is intended to be used
    for its return value, rather than for its side effects. In that sense, it
    is similar to the standard lapply function, but doesn't require the
    evaluation of a function. Using foreach without side effects also
    facilitates executing the loop in parallel."""

    homepage = "https://cran.r-project.org/web/packages/foreach/index.html"
    url      = "https://cran.r-project.org/src/contrib/foreach_1.4.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/foreach"

    version('1.4.3', 'ef45768126661b259f9b8994462c49a0')

    depends_on('r-codetools', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
