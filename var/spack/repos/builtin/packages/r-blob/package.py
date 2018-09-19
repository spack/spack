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


class RBlob(RPackage):
    """R's raw vector is useful for storing a single binary object.
    What if you want to put a vector of them in a data frame? The blob
    package provides the blob object, a list of raw vectors, suitable
    for use as a column in data frame."""

    homepage = "https://cran.rstudio.com/web/packages/blob/index.html"
    url      = "https://cran.rstudio.com/src/contrib/blob_1.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/blob"
    version('1.1.0', '1c729aca36fd5193d81b1cd5ed9d8a00')

    depends_on('r-tibble', type=('build', 'run'))
