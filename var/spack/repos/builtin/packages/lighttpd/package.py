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


class Lighttpd(CMakePackage):
    """a secure, fast, compliant and very flexible web-server"""

    homepage = "https://www.lighttpd.net"
    url      = "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.50.tar.gz"

    version('1.4.50', sha256='c9a9f175aca6db22ebebbc47de52c54a99bbd1dce8d61bb75103609a3d798235')
    version('1.4.49', sha256='8b744baf9f29c386fff1a6d2e435491e726cb8d29cfdb1fe20ab782ee2fc2ac7')
