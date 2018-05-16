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


class GlobusToolkit(AutotoolsPackage):
    """The Globus Toolkit is an open source software toolkit used for building
       grids"""

    homepage = "http://toolkit.globus.org"
    url      = "http://toolkit.globus.org/ftppub/gt6/installers/src/globus_toolkit-6.0.1506371041.tar.gz"

    version('6.0.1506371041', 'e17146f68e03b3482aaea3874d4087a5')
    version('6.0.1493989444', '9e9298b61d045e65732e12c9727ceaa8')

    depends_on('openssl')
