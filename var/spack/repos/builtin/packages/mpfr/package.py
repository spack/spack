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


class Mpfr(AutotoolsPackage):
    """The MPFR library is a C library for multiple-precision
       floating-point computations with correct rounding."""

    homepage = "http://www.mpfr.org"
    url      = "https://gforge.inria.fr/frs/download.php/latestfile/159/mpfr-3.1.2.tar.bz2"

    version('3.1.5', 'b1d23a55588e3b2a13e3be66bc69fd8d')
    version('3.1.4', 'b8a2f6b0e68bef46e53da2ac439e1cf4')
    version('3.1.3', '5fdfa3cfa5c86514ee4a241a1affa138')
    version('3.1.2', 'ee2c3ac63bf0c2359bf08fc3ee094c19')

    depends_on('gmp@4.1.0:')  # mpir is a drop-in replacement for this

    patch('vasprintf.patch', when='@3.1.5')
    patch('strtofr.patch',   when='@3.1.5')
