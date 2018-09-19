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


class Nmap(AutotoolsPackage):
    """Nmap ("Network Mapper") is a free and open source (license)
       utility for network discovery and security auditing.
       It also provides ncat an updated nc"""

    homepage = "https://nmap.org"
    url      = "https://nmap.org/dist/nmap-7.70.tar.bz2"

    version('7.70', '84eb6fbe788e0d4918c2b1e39421bf79')
    version('7.31', 'f2f6660142a777862342a58cc54258ea')
    version('7.30', '8d86797d5c9e56de571f9630c0e6b5f8')
