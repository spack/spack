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


class RRlang(RPackage):
    """A toolbox for working with base types, core R features like the
       condition system, and core 'Tidyverse' features like tidy evaluation."""

    homepage = "https://cran.r-project.org/web/packages/rlang/index.html"
    url      = "https://cran.r-project.org/src/contrib/rlang_0.1.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rlang"

    version('0.1.4', 'daed5104d557c0cbfb4a654ec8ffb579')
    version('0.1.2', '170f8cf7b61898040643515a1746a53a')
    version('0.1.1', '38a51a0b8f8487eb52b4f3d986313682')
