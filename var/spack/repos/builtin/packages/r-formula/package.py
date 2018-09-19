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


class RFormula(RPackage):
    """Infrastructure for extended formulas with multiple parts on the right-hand
    side and/or multiple responses on the left-hand side."""

    homepage = "https://cran.r-project.org/package=Formula"
    url      = "https://cran.rstudio.com/src/contrib/Formula_1.2-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Formula"

    version('1.2-2', 'c69bb0522811cf8eb9f1cc6c3d182b6e')
    version('1.2-1', '2afb31e637cecd0c1106317aca1e4849')
