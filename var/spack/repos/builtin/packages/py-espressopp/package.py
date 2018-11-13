# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyEspressopp(CMakePackage):
    """ESPResSo++ is an extensible, flexible, fast and parallel simulation
       software for soft matter research. It is a highly versatile software
       package for the scientific simulation and analysis of coarse-grained
       atomistic or bead-spring models as they are used in soft matter research
    """
    homepage = "https://espressopp.github.io"
    url      = "https://github.com/espressopp/espressopp/tarball/v1.9.4.1"
    git      = "https://github.com/espressopp/espressopp.git"

    version('develop', branch='master')
    version('1.9.5',   '13a93c30b07132b5e5fa0d828aa17d79')
    version('1.9.4.1', '0da74a6d4e1bfa6a2a24fca354245a4f')
    version('1.9.4',   'f2a27993a83547ad014335006eea74ea')

    variant('ug', default=False, description='Build user guide')
    variant('pdf', default=False, description='Build user guide in pdf format')
    variant('dg', default=False, description='Build developer guide')

    depends_on("cmake@2.8:", type='build')
    depends_on("mpi")
    depends_on("boost+serialization+filesystem+system+python+mpi", when='@1.9.4:')
    extends("python")
    depends_on("python@2:2.8")
    depends_on("py-mpi4py@2.0.0:", when='@1.9.4', type=('build', 'run'))
    depends_on("py-mpi4py@1.3.1:", when='@1.9.4.1:', type=('build', 'run'))
    depends_on("fftw")
    depends_on("py-sphinx", when="+ug", type='build')
    depends_on("py-sphinx", when="+pdf", type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', when="+ug", type='build')
    depends_on('py-matplotlib', when="+pdf", type='build')
    depends_on("texlive", when="+pdf", type='build')
    depends_on("doxygen", when="+dg", type='build')

    def cmake_args(self):
        return [
            '-DEXTERNAL_MPI4PY=ON',
            '-DEXTERNAL_BOOST=ON',
            '-DWITH_RC_FILES=OFF'
        ]

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()
            if '+ug' in spec:
                make("ug", parallel=False)
            if '+pdf' in spec:
                make("ug-pdf", parallel=False)
            if '+dg' in spec:
                make("doc", parallel=False)
