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


class Tensorflow(Package):
    """
    TensorFlow is an open source software library for numerical computation using data flow graphs
    """

    homepage = "https://github.com/tensorflow"

    version('e697cf7', git='https://github.com/tensorflow.git', commit='e697cf787b09193a6921af6d2b7db2d6c4d2a5dd')

    depends_on('zlib')
    depends_on('giflib')
    depends_on('png')
    depends_on('jpeg')
    depends_on('eigen')
    depends_on('gemmlowp')
    depends_on('jsoncpp')
    depends_on('farmhash')
    depends_on('highwayhash')
    depends_on('protobuf')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
