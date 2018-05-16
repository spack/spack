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


class RXlconnectjars(RPackage):
    """Provides external JAR dependencies for the XLConnect package."""

    homepage = "http://miraisolutions.wordpress.com/"
    url      = "https://cran.r-project.org/src/contrib/XLConnectJars_0.2-9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/XLConnectJars"

    version('0.2-12', '6984e5140cd1c887c017ef6f88cbba81')
    version('0.2-9', 'e6d6b1acfede26acaa616ee421bd30fb')

    depends_on('r-rjava', type=('build', 'run'))
