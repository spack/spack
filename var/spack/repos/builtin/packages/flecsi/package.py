# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Flecsi(CMakePackage):
    """FleCSI is a compile-time configurable framework designed to support
       multi-physics application development. As such, FleCSI attempts to
       provide a very general set of infrastructure design patterns that can
       be specialized and extended to suit the needs of a broad variety of
       solver and data requirements. Current support includes multi-dimensional
       mesh topology, mesh geometry, and mesh adjacency information,
       n-dimensional hashed-tree data structures, graph partitioning
       interfaces,and dependency closures.
    """
    homepage = "http://flecsi.lanl.gov/"
    git      = "https://github.com/laristra/flecsi.git"

    version('develop', branch='master', submodules=True)

    variant('mpi', default=True,
            description='Build on top of mpi conduit for mpi inoperability')

    depends_on("cmake@3.1:", type='build')
    depends_on("legion+shared", when='~mpi')
    depends_on("legion+shared+mpi", when='+mpi')
    depends_on("parmetis")

    def cmake_args(self):
        options = ['-DENABLE_UNIT_TESTS=ON']

        if '+mpi' in self.spec:
            options.extend([
                '-DENABLE_MPI=ON',
            ])

        return options
