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


class Elpa(Package):
    """
    Eigenvalue solvers for Petaflop-Applications (ELPA)
    """

    homepage = 'http://elpa.mpcdf.mpg.de/'
    url = 'http://elpa.mpcdf.mpg.de/elpa-2015.11.001.tar.gz'

    version('2015.11.001', 'de0f35b7ee7c971fd0dca35c900b87e6', url='http://elpa.mpcdf.mpg.de/elpa-2015.11.001.tar.gz')

    variant('openmp', default=False, description='Activates OpenMP support')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')

    def install(self, spec, prefix):

        options = ["--prefix=%s" % prefix]

        if '+openmp' in spec:
            options.append("--enable-openmp")

        configure(*options)
        make()
        make("install")
