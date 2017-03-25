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


class Protobuf(AutotoolsPackage):
    """Google's data interchange format."""

    homepage = "https://developers.google.com/protocol-buffers"
    url      = "https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.bz2"

    version('3.0.2', '845b39e4b7681a2ddfd8c7f528299fbb', url='https://github.com/google/protobuf/archive/v3.0.2.tar.gz')
    version('2.5.0', 'a72001a9067a4c2c4e0e836d0f92ece4')

    depends_on('m4', when='@3.0.2:')
    depends_on('autoconf', when='@3.0.2:')
    depends_on('automake', when='@3.0.2:')
    depends_on('libtool', when='@3.0.2:')
