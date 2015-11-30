##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Gmp(Package):
    """GMP is a free library for arbitrary precision arithmetic,
       operating on signed integers, rational numbers, and
       floating-point numbers."""
    homepage = "https://gmplib.org"
    url      = "https://gmplib.org/download/gmp/gmp-6.0.0a.tar.bz2"

    version('6.0.0a', 'b7ff2d88cae7f8085bd5006096eed470')
    version('6.0.0' , '6ef5869ae735db9995619135bd856b84')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
