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


class RBackports(RPackage):
    """Implementations of functions which have been introduced
    in R since version 3.0.0. The backports are conditionally
    exported which results in R resolving the function names to
    the version shipped with R (if available) and uses the
    implemented backports as fallback. This way package developers
    can make use of the new functions without worrying about the
    minimum required R version."""

    homepage = "https://cran.r-project.org/package=backports"
    url      = "https://cran.r-project.org/src/contrib/backports_1.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/backports"

    version('1.1.1', '969543a0af32dc23bba9bb37ec82008c')
    version('1.1.0', 'b97a71b026fd7ede0e449be93d160c17')
