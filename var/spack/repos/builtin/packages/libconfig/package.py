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


class Libconfig(AutotoolsPackage):
    """C/C++ Configuration File Library"""

    homepage = "http://www.hyperrealm.com/libconfig/"
    url      = "https://github.com/hyperrealm/libconfig/archive/v1.5.tar.gz"

    force_autoreconf = True
    # there is currently a build error with version 1.6, see:
    # https://github.com/hyperrealm/libconfig/issues/47
    # version('1.6', '2ccd24b6a2ee39f7ff8a3badfafb6539')
    version('1.5', 'e92a91c2ddf3bf77bea0f5ed7f09e492', preferred=True)

    depends_on('m4', type=('build'))
    depends_on('autoconf', type=('build'))
    depends_on('automake', type=('build'))
    depends_on('libtool', type=('build'))
