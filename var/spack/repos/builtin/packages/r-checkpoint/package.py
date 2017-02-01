##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class RCheckpoint(RPackage):
    """The goal of checkpoint is to solve the problem of package
    reproducibility in R. Specifically, checkpoint allows you to
    install packages as they existed on CRAN on a specific snapshot
    date as if you had a CRAN time machine."""

    homepage = "https://cran.r-project.org/package=checkpoint"
    url      = "https://cran.r-project.org/src/contrib/checkpoint_0.3.18.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/checkpoint"

    version('0.3.18', '021d7faeb72c36167951e103b2b065ea')
    version('0.3.15', 'a4aa8320338f1434a330d984e97981ea')

    depends_on('r@3.0.0:')
