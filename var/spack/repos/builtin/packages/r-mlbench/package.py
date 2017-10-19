##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class RMlbench(RPackage):
    """A collection of artificial and real-world machine learning benchmark
    problems, including, e.g., several data sets from the UCI repository."""

    homepage = "https://cran.r-project.org/web/packages/mlbench/index.html"
    url      = "https://cran.r-project.org/src/contrib/mlbench_2.1-1.tar.gz"

    version('2.1-1', '9f06848b8e137b8a37417c92d8e57f3b')

    depends_on('r@2.10:')

    depends_on('r-lattice', type=('build', 'run'))
