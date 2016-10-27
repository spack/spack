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


class Espressopp(Package):
    """ESPResSo++ is an extensible, flexible, fast and parallel simulation
       software for soft matter research. It is a highly versatile software
       package for the scientific simulation and analysis of coarse-grained
       atomistic or bead-spring models as they are used in soft matter research
    """
    homepage = "https://espressopp.github.io"
    url      = "https://github.com/espressopp/espressopp/archive/v1.9.4.zip"

    version('develop', git='https://github.com/espressopp/espressopp.git', branch='master')
    version('1.9.4', git='https://github.com/espressopp/espressopp.git', tag='v1.9.4')

    variant('debug', default=False, description='Build debug version')
    variant('ug', default=False, description='Build user guide')
    variant('pdf', default=False, description='Build user guide in pdf format')
    variant('dg', default=False, description='Build developer guide')
    variant('tests', default=False, description='Run the tests')

    depends_on("cmake@3.7.1:", type='build')
    depends_on("mpi", type=('build', 'link', 'run'))
    depends_on("boost+serialization+filesystem+system+python+mpi", when='@1.9.4:', type=('build', 'link', 'run'))
    extends("python")
    depends_on("python@2:")
    depends_on("py-mpi4py@2.0.0", when='@1.9.4:', type=('build', 'link', 'run'))
    depends_on("fftw", type=('build', 'link', 'run'))
    depends_on("py-sphinx", when="+ug", type='build')
    depends_on("py-sphinx", when="+pdf", type='build')
    depends_on("texlive", when="+pdf", type='build')
    depends_on("doxygen", when="+dg", type='build')

    def install(self, spec, prefix):
        options = []
        options.append('-DEXTERNAL_MPI4PY=ON')
        options.append('-DEXTERNAL_BOOST=ON')
        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')
        options.extend(std_cmake_args)
        with working_dir('build', create=True):
            cmake('..', *options)
            make("clean")
            make()
            if '+ug' in spec:
                make("ug", parallel=False)
            if '+pdf' in spec:
                make("ug-pdf", parallel=False)
            if '+dg' in spec:
                make("doc", parallel=False)
            if '+tests' in spec:
                make("test", parallel=False)
            make("install")
