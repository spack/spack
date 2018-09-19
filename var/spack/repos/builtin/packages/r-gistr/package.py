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


class RGistr(RPackage):
    """Work with 'GitHub' 'gists' from 'R'. This package allows the user to
    create new 'gists', update 'gists' with new files, rename files, delete
    files, get and delete 'gists', star and 'un-star' 'gists', fork 'gists',
    open a 'gist' in your default browser, get embed code for a 'gist', list
    'gist' 'commits', and get rate limit information when 'authenticated'. Some
    requests require authentication and some do not."""

    homepage = "https://github.com/ropensci/gistr"
    url      = "https://cran.r-project.org/src/contrib/gistr_0.3.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gistr"

    version('0.3.6', '49d548cb3eca0e66711aece37757a2c0')

    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-rmarkdown', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
