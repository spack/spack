# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mstk(CMakePackage):
    """MSTK is a mesh framework that allows users to represent,
    manipulate and query unstructured 3D arbitrary topology meshes
    in a general manner without the need to code their own data
    structures. MSTK is a flexible framework in that it allows a
    variety of underlying representations for the mesh while
    maintaining a common interface. It allows users to choose from
    different mesh representations either at initialization (implemented)
    or during the program execution (not yet implemented) so that the
    optimal data structures are used for the particular algorithm.
    The interaction of users and applications with MSTK is through a
    functional interface that acts as though the mesh always contains
    vertices, edges, faces and regions and maintains connectivity between
    all these entities."""

    homepage = "https://github.com/MeshToolkit/MSTK"
    git      = "https://github.com/MeshToolkit/MSTK"

    maintainers = ['julienloiseau']

    version('master', branch='master')

    variant('parallel', default='none', description='Enable Parallel Support',
            values=('none', 'metis', 'zoltan', 'parmetis'), multi=True)
    variant('exodusii', default=False, description='Enable ExodusII')
    variant('use_markers', default=True, description="Enable MSTK to use markers")

    depends_on("cmake@3.8:", type='build')

    # Parallel variant
    depends_on("mpi", when='parallel=metis')
    depends_on("mpi", when='parallel=zoltan')
    depends_on("mpi", when='parallel=parmetis')
    depends_on("zoltan -fortran", when='parallel=zoltan')
    depends_on("zoltan -fortran +parmetis", when='parallel=parmetis')
    depends_on("zoltan -fortran +parmetis", when="parallel=zoltan +exodusii")
    depends_on("metis", when="parallel=zoltan +exodusii")

    depends_on("metis", when='parallel=metis')
    depends_on("metis", when='parallel=parmetis')

    # Exodusii variant
    # The default exodusii build with mpi support
    # It includes netcdf which includes hdf5
    depends_on("exodusii", when='+exodusii')

    def cmake_args(self):
        options = []
        if '+use_markers' in self.spec:
            options.append('-DMSTK_USE_MARKERS=ON')
        else:
            options.append('-DMSTK_USE_MARKERS=OFF')

        # Parallel variant
        if not self.spec.satisfies('parallel=none'):
            # Use mpi for compilation
            options.append('-DCMAKE_CXX_COMPILER=' + self.spec['mpi'].mpicxx)
            options.append('-DCMAKE_C_COMPILER=' + self.spec['mpi'].mpicc)
            options.append('-DENABLE_PARALLEL=ON')
        else:
            options.append('-DENABLE_PARALLEL=OFF')

        if ("parmetis" in self.spec or "zoltan" in self.spec and
            "+exodusii" in self.spec):
            options.append("-DENABLE_METIS=ON")
            options.append("-DENABLE_ZOLTAN=ON")
            options.append('-DZOLTAN_NEEDS_ParMETIS=ON')
        else:
            if "zoltan" in self.spec:
                options.append("-DENABLE_ZOLTAN=ON")
            else:
                options.append("-DENABLE_ZOLTAN=OFF")
            if "metis" in self.spec:
                options.append("-DENABLE_METIS=ON")
            else:
                options.append("-DENABLE_METIS=OFF")
            options.append('-DZOLTAN_NEEDS_ParMETIS=OFF')

        # ExodusII variant
        if '+exodusii' in self.spec:
            options.append('-DENABLE_ExodusII=ON')
        else:
            options.append('-DENABLE_ExodusII=OFF')

        return options
