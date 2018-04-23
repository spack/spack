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


class Mesquite(AutotoolsPackage):
    """Mesquite (Mesh Quality Improvement Toolkit) is designed to provide a
       stand-alone, portable, comprehensive suite of mesh quality improvement
       algorithms and components that can be used to construct custom quality
       improvement algorithms. Mesquite provides a robust and effective mesh
       improvement toolkit that allows both meshing researchers application
       scientists to benefit from the latest developments in mesh quality
       control and improvement."""

    homepage = "https://software.sandia.gov/mesquite"
    url      = "https://software.sandia.gov/mesquite/mesquite-2.3.0.tar.gz"

    version('2.99',  '92b94167981bb8fcd59b0f0f18fbab64')
    version('2.3.0', 'f64948b5210d5ccffaa9a2482447b322')
    version('2.2.0', '41360c363e541aff7dc10024c90072d3')

    variant('mpi', default=True, description='Enable MPI parallel support')

    depends_on('mpi', when='+mpi')

    def configure_args(self):
        args = [
            'CC=%s' % self.spec['mpi'].mpicc,
            'CXX=%s' % self.spec['mpi'].mpicxx,
            '--with-mpi=%s' % self.spec['mpi'].prefix,
            '--enable-release',
            '--enable-shared',
        ]
        return args
