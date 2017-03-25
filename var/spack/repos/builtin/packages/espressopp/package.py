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


class Espressopp(CMakePackage):
    """ESPResSo++ is an extensible, flexible, fast and parallel simulation
       software for soft matter research. It is a highly versatile software
       package for the scientific simulation and analysis of coarse-grained
       atomistic or bead-spring models as they are used in soft matter research
    """
    homepage = "https://espressopp.github.io"
    url      = "https://github.com/espressopp/espressopp/tarball/v1.9.4.1"

    version('develop', git='https://github.com/espressopp/espressopp.git', branch='master')
    version('1.9.4.1', '0da74a6d4e1bfa6a2a24fca354245a4f')
    version('1.9.4', 'f2a27993a83547ad014335006eea74ea')

    variant('debug', default=False, description='Build debug version')
    variant('ug', default=False, description='Build user guide')
    variant('pdf', default=False, description='Build user guide in pdf format')
    variant('dg', default=False, description='Build developer guide')

    depends_on("cmake@2.8:", type='build')
    depends_on("mpi")
    depends_on("boost+serialization+filesystem+system+python+mpi", when='@1.9.4:')
    extends("python")
    depends_on("python@2:2.7.13")
    depends_on("py-mpi4py@2.0.0:", when='@1.9.4', type=('build', 'run'))
    depends_on("py-mpi4py@1.3.1:", when='@1.9.4.1:', type=('build', 'run'))
    depends_on("fftw")
    depends_on("py-sphinx", when="+ug", type='build')
    depends_on("py-sphinx", when="+pdf", type='build')
    depends_on('py-numpy', when="+ug", type='build')
    depends_on('py-numpy', when="+pdf", type='build')
    depends_on('py-matplotlib', when="+ug", type='build')
    depends_on('py-matplotlib', when="+pdf", type='build')
    depends_on("texlive", when="+pdf", type='build')
    depends_on("doxygen", when="+dg", type='build')

    def build_type(self):
        spec = self.spec
        if '+debug' in spec:
            return 'Debug'
        else:
            return 'Release'

    def cmake_args(self):
        return ['-DEXTERNAL_MPI4PY=ON', '-DEXTERNAL_BOOST=ON']

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()
            if '+ug' in spec:
                make("ug", parallel=False)
            if '+pdf' in spec:
                make("ug-pdf", parallel=False)
            if '+dg' in spec:
                make("doc", parallel=False)
