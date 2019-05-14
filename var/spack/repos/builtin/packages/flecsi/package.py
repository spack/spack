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
    variant('legion', default=False)

    depends_on("cmake@3.1:")
    depends_on("mpi")
    depends_on("gasnet~pshm")
    depends_on("legion")
    depends_on("legion+shared", when='~mpi')
    depends_on("legion+shared+mpi", when='+mpi')
    depends_on("boost@1.59.0 cxxstd=11 +program_options")
    depends_on("metis@5.1.0:")
    depends_on("parmetis@4.0.3:")
    depends_on("caliper")
    depends_on("gotcha")
    depends_on("graphviz")

    def cmake_args(self):
        options = ['-DCMAKE_BUILD_TYPE=debug -DFLECSI_RUNTIME_MODEL=mpi']
        options.extend(['-DENABLE_UNIT_TESTS=ON -DENABLE_PARMETIS=ON -DENABLE_COLORING=ON']) 
        options.extend(['-DENABLE_DOXYGEN=ON -DENABLE_DOCUMENTATION=OFF -DENABLE_COVERAGE_BUILD=OFF'])

        if '~mpi' in self.spec:
            options.extend([
                '-DENABLE_MPI=OFF',
            ])

        return options
