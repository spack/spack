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


class RPbapply(RPackage):
    """A lightweight package that adds progress bar to vectorized R
    apply functions."""

    homepage = "https://cran.r-project.org/web/packages/pbapply/index.html"
    url      = "https://cran.r-project.org/src/contrib/pbapply_1.3-3.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/pbapply"

    version('1.3-3', '570db6795179a1439c174be881c77d18')
    version('1.3-2', 'd72a777bfe4a28ba4e1585e31680f82e')
    version('1.3-1', '13d64dead441426aa96a3bf3fde29daf')
    version('1.3-0', 'a3f93cd05054657a01893a3817fa1f08')
    version('1.2-2', '23e2bfe531c704b79308b0b5fbe1ace8')

    depends_on('r@3.4.0:3.4.9')
