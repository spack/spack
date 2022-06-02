# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Pastix(CMakePackage, CudaPackage):
    """a high performance parallel solver for very large sparse linear systems
       based on direct methods"""
    homepage = "https://gitlab.inria.fr/solverstack/pastix/blob/master/README.md"
    url      = "https://gitlab.inria.fr/solverstack/pastix/uploads/baa57033d98378e0f3affbf45900fb6e/pastix-6.2.1.tar.gz"
    git      = "https://gitlab.inria.fr/solverstack/pastix.git"
    maintainers = ['fpruvost', 'mfaverge', 'ramet']

    version('master', branch='master', submodules=True)
    version('6.2.1', '50742cc0e6e03728f7529fc607d5c65b9e14205f192947678d6103a872a6210c')

    # cmake's specific
    variant('shared', default=True, description='Build Pastix as a shared library')

    # pastix's specific
    variant('doc', default=False, description='Enable documentation')
    variant('int64', default=False, description='To use 64 bits integers')
    variant('metis', default=False, description='Enable Metis')
    variant('scotch', default=True, description='Enable Scotch')
    variant(
        'runtime', default='none', description='Runtime support',
        values=('none', 'starpu'), multi=False
    )
    variant('cuda', default=False, when='runtime=starpu', description='Enable CUDA')
    variant('mpi', default=False, description='Enable MPI')

    # Dependencies
    depends_on("pkgconfig", type='build')
    depends_on("hwloc")
    depends_on("lapack")
    # ensure openblas use threads=openmp to be thread-safe
    depends_on('openblas threads=openmp', when='^openblas')
    with when("+metis"):
        depends_on("metis@5.1:")
        depends_on("metis@5.1:+int64", when='+int64')
    with when("+scotch"):
        depends_on("scotch~metis")
        depends_on("scotch~metis+int64", when='+int64')
        depends_on("scotch~metis~mpi", when='~mpi')
    with when("runtime=starpu"):
        depends_on("starpu")
        depends_on("starpu~mpi", when='~mpi')
        depends_on("starpu+mpi", when='+mpi')
        depends_on("starpu~cuda", when='~cuda')
        depends_on("starpu+cuda", when='+cuda')
        depends_on("cuda", when='+cuda')
    depends_on("mpi", when='+mpi')

    def cmake_args(self):
        spec = self.spec

        args = [
            "-Wno-dev",
            self.define("CMAKE_COLOR_MAKEFILE", "ON"),
            self.define("CMAKE_VERBOSE_MAKEFILE", "ON"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("PASTIX_INT64", "int64"),
            self.define_from_variant("PASTIX_ORDERING_METIS", "metis"),
            self.define_from_variant("PASTIX_ORDERING_SCOTCH", "scotch"),
            self.define("PASTIX_WITH_PARSEC", "OFF"),
            self.define_from_variant("PASTIX_WITH_MPI", "mpi")
        ]

        if spec.satisfies('runtime=starpu'):
            args.extend([self.define("PASTIX_WITH_STARPU", "ON")])
            args.extend([self.define_from_variant("PASTIX_WITH_CUDA", "cuda")])

        if ('^intel-mkl' in spec or '^intel-parallel-studio+mkl' in spec):
            args.extend([self.define("BLA_VENDOR", "Intel10_64lp_seq")])
        elif ('^netlib-lapack' in spec):
            args.extend([self.define("BLA_VENDOR", "Generic")])
        elif ('^openblas' in spec):
            args.extend([self.define("BLA_VENDOR", "OpenBLAS")])

        if spec.satisfies('+mpi'):
            args.extend([
                self.define("MPI_C_COMPILER", self.spec['mpi'].mpicc),
                self.define("MPI_CXX_COMPILER", self.spec['mpi'].mpicxx),
                self.define("MPI_Fortran_COMPILER", self.spec['mpi'].mpifc)
            ])

        return args
