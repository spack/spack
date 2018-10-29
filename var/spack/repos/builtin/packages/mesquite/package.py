# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
