##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Bml(CMakePackage):
    """The basic matrix library (bml) is a collection of various matrix data
    formats (in dense and sparse) and their associated algorithms for basic
    matrix operations."""

    homepage = "http://lanl.github.io/bml/"
    url      = "https://github.com/lanl/bml/tarball/v1.2.2"

    version('1.2.2', 'c86959cb0188e9d0a9a2cbad03b2782d')
    version('1.1.0', '271adecee08aee678be9eeceee06b6fb')
    version('develop', git='https://github.com/lanl/bml', branch='master')

    variant('shared', default=True, description='Build shared libs')

    depends_on("blas")
    depends_on("lapack")

    def cmake_args(self):
        return [
            '-DBUILD_SHARED_LIBS={0}'.format(
                'ON' if '+shared' in self.spec else 'OFF')
        ]
