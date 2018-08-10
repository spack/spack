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


class RBindrcpp(RPackage):
    """Provides an easy way to fill an environment with active bindings that
       call a C++ function."""

    homepage = "https://github.com/krlmlr/bindrcpp"
    url      = "https://cran.r-project.org/src/contrib/bindrcpp_0.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/bindrcpp"

    version('0.2.2', '48130709eba9d133679a0e959e49a7b14acbce4f47c1e15c4ab46bd9e48ae467')
    version('0.2', '2ed7f19fd9a12587f882d90060e7a343')

    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-bindr', type=('build', 'run'))
    depends_on('r-plogr', type=('build', 'run'))
