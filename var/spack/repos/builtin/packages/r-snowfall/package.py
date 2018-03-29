##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class RSnowfall(RPackage):
    """Usability wrapper around snow for easier development of parallel R
       programs. This package offers e.g. extended error checks, and additional
       functions. All functions work in sequential mode, too, if no cluster is
       present or wished. Package is also designed as connector to the cluster
       management tool sfCluster, but can also used without it."""

    homepage = "https://cran.r-project.org/web/packages/snowfall/index.html"
    url      = "https://cran.r-project.org/src/contrib/snowfall_1.84-6.1.tar.gz"

    version('1.84-6.1', '5ec38116aa9cac237d56f59ba5bd60e3')

    depends_on('r-snow', type=('build', 'run'))
