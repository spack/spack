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


class RNp(RPackage):
    """This package provides a variety of nonparametric (and semiparametric)
    kernel methods that seamlessly handle a mix of continuous, unordered, and
    ordered factor data types. We would like to gratefully acknowledge support
    from the Natural Sciences and Engineering Research Council of Canada
    (NSERC:www.nserc.ca), the Social Sciences and Humanities Research Council
    of Canada (SSHRC:www.sshrc.ca), and the Shared Hierarchical Academic
    Research Computing Network (SHARCNET:www.sharcnet.ca)."""

    homepage = "https://github.com/JeffreyRacine/R-Package-np/"
    url      = "https://cran.r-project.org/src/contrib/np_0.60-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/np"

    version('0.60-2', 'e094d52ddff7280272b41e6cb2c74389')

    depends_on('r-boot', type=('build', 'run'))
    depends_on('r-cubature', type=('build', 'run'))
