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


class Isl(AutotoolsPackage):
    """isl (Integer Set Library) is a thread-safe C library for manipulating
    sets and relations of integer points bounded by affine constraints."""

    homepage = "http://isl.gforge.inria.fr"
    url      = "http://isl.gforge.inria.fr/isl-0.18.tar.bz2"

    version('0.18', '11436d6b205e516635b666090b94ab32')
    version('0.14', 'acd347243fca5609e3df37dba47fd0bb')

    depends_on('gmp')

    def configure_args(self):
        return [
            '--with-gmp-prefix={0}'.format(self.spec['gmp'].prefix)
        ]
