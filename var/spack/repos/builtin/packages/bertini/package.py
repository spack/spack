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


class Bertini(AutotoolsPackage):
    """Bertini is a general-purpose solver, written in C, that was created
    for research about polynomial continuation. It solves for the numerical
    solution of systems of polynomial equations using homotopy continuation."""

    homepage = "https://bertini.nd.edu/"
    url      = "https://bertini.nd.edu/BertiniSource_v1.5.tar.gz"

    version('1.5', 'e3f6cc6e7f9a0cf1d73185e8671af707')

    variant('mpi', default=True, description='Compile in parallel')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('gmp')
    depends_on('mpfr')
    depends_on('mpi', when='+mpi')
