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


class RMethodss3(RPackage):
    """Methods that simplify the setup of S3 generic functions and
    S3 methods. Major effort has been made in making definition of
    methods as simple as possible with a minimum of maintenance for
    package developers. For example, generic functions are created
    automatically, if missing, and naming conflict are automatically
    solved, if possible. The method setMethodS3() is a good start
    for those who in the future may want to migrate to S4. This is
    a cross-platform package implemented in pure R that generates
    standard S3 methods."""

    homepage = "https://cran.r-project.org/package=R.methodsS3"
    url      = "https://cran.r-project.org/src/contrib/R.methodsS3_1.7.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/R.methodsS3"

    version('1.7.1', 'c88e815837f268affd4f2a39c737d969')
