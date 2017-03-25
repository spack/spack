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


class Czmq(AutotoolsPackage):
    """ A C interface to the ZMQ library """
    homepage = "http://czmq.zeromq.org"
    url      = "https://github.com/zeromq/czmq/archive/v3.0.2.tar.gz"

    version('3.0.2', '23e9885f7ee3ce88d99d0425f52e9be1',
            url='https://github.com/zeromq/czmq/archive/v3.0.2.tar.gz')

    depends_on('libtool', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('pkg-config', type='build')
    depends_on('zeromq')
