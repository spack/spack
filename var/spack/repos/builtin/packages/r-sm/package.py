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


class RSm(RPackage):
    """This is software linked to the book 'Applied Smoothing Techniques for
       Data Analysis - The Kernel Approach with S-Plus Illustrations'
       Oxford University Press."""

    homepage = "http://www.stats.gla.ac.uk/~adrian/sm"
    url      = "https://cran.r-project.org/src/contrib/sm_2.2-5.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/sm"

    version('2.2-5.5', sha256='43e212a14c364b98b10018b56fe0a619ccffe4bde1294e6c45b3eafe7caf82e7')

    depends_on('r@3.1.0:', type=('build', 'run'))
