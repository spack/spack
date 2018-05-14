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


class RBabel(RPackage):
    """Ribosome Profiling Data Analysis"""

    homepage = "https://cran.r-project.org/package=babel"
    url      = "https://cran.r-project.org/src/contrib/babel_0.3-0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/babel"

    version('0.3-0', '3a3bd668de7bf8f508b70fded934b0c5')
    version('0.2-6', 'e8588ea9d6bf679c6987932fcb021b0f')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
