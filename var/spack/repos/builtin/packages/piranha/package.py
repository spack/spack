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


class Piranha(CMakePackage):
    """Piranha is a computer-algebra library for the symbolic manipulation of
    sparse multivariate polynomials and other closely-related symbolic objects
    (such as Poisson series)."""

    homepage = "https://bluescarni.github.io/piranha/sphinx/"
    url      = "https://github.com/bluescarni/piranha/archive/v0.5.tar.gz"
    git      = "https://github.com/bluescarni/piranha.git"

    version('develop', branch='master')
    version('0.5', '99546bae2be115737b6316751eb0b84d')

    variant('python',   default=True,
            description='Build the Python bindings')

    # Build dependencies
    depends_on('cmake@3.2.0:', type='build')
    extends('python',         when='+pyranha')
    depends_on('python@2.6:', type='build', when='+pyranha')

    # Other dependencies
    depends_on('boost+iostreams+regex+serialization',
               when='~python')
    depends_on('boost+iostreams+regex+serialization+python',
               when='+python')
    depends_on('bzip2')
    depends_on('gmp')   # mpir is a drop-in replacement for this
    depends_on('mpfr')  # Could also be built against mpir

    def cmake_args(self):
        return [
            '-DBUILD_PYRANHA=%s' % ('ON' if '+python' in self.spec else 'OFF'),
            '-DBUILD_TESTS:BOOL=ON',
        ]
