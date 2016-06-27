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


class Glpk(Package):
    """
    The GLPK (GNU Linear Programming Kit) package is intended for solving large-scale linear programming (LP), mixed
    integer programming (MIP), and other related problems. It is a set of routines written in ANSI C and organized in
    the form of a callable library
    """
    homepage = "https://www.gnu.org/software/glpk"
    url = "http://ftp.gnu.org/gnu/glpk/glpk-4.57.tar.gz"

    version('4.57', '237531a54f73155842f8defe51aedb0f')

    variant('gmp', default=False, description='Activates support for GMP library')

    depends_on('gmp', when='+gmp')

    def install(self, spec, prefix):

        options = ['--prefix=%s' % prefix]

        if '+gmp' in spec:
            options.append('--with-gmp')

        configure(*options)
        make()
        make("install")
