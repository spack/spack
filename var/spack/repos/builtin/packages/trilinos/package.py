from spack import *
import os

class Trilinos(Package):
    """The Trilinos Project is an effort to develop algorithms and enabling technologies within an object-oriented
    software framework for the solution of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """
    homepage = "https://trilinos.org/"
    url = "http://trilinos.csbsju.edu/download/files/trilinos-12.2.1-Source.tar.gz"

    version('12.6.1', 'adcf2d3aab74cdda98f88fee19cd1442604199b0515ee3da4d80cbe8f37d00e4')
    version('12.4.2', '7c830f7f0f68b8ad324690603baf404e')
    version('12.2.1', '6161926ea247863c690e927687f83be9')
    version('12.0.1', 'bd99741d047471e127b8296b2ec08017')
    version('11.14.3', '2f4f83f8333e4233c57d0f01c4b57426')
    version('11.14.2', 'a43590cf896c677890d75bfe75bc6254')
    version('11.14.1', '40febc57f76668be8b6a77b7607bb67f')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds a debug version of the libraries')

    # Everything should be compiled with -fpic
    depends_on('blas')
    depends_on('lapack')
    depends_on('boost')
    depends_on('matio')
    depends_on('glm')
    depends_on('swig')
    depends_on('metis')
    depends_on('suite-sparse')
    depends_on('tbb')

    # MPI related dependencies
    depends_on('mpi')
    depends_on('netcdf+mpi')
    depends_on('parmetis')
    depends_on('mumps+metis+parmetis')
    depends_on('scalapack')
    depends_on('superlu-dist')
    depends_on('hypre')
    depends_on('hdf5+mpi')

    depends_on('python') #  Needs py-numpy activated

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        options.extend(['-DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON',
                        '-DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=ON',
                        '-DTrilinos_ENABLE_TESTS:BOOL=OFF',
                        '-DTrilinos_ENABLE_EXAMPLES:BOOL=OFF',
                        '-DCMAKE_BUILD_TYPE:STRING=%s' % ('Debug' if '+debug' in spec else 'Release'),
                        '-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if '+shared' in spec else 'OFF'),
                        '-DTPL_ENABLE_MPI:BOOL=ON',
                        '-DMPI_BASE_DIR:PATH=%s' % spec['mpi'].prefix,
                        '-DTPL_ENABLE_BLAS=ON',
                        '-DBLAS_LIBRARY_NAMES=blas',
                        '-DBLAS_LIBRARY_DIRS=/usr/lib', # % spec['blas'].prefix, #FIXME
                        '-DTPL_ENABLE_LAPACK=ON',
                        '-DLAPACK_LIBRARY_NAMES=lapack',
                        '-DLAPACK_LIBRARY_DIRS=/usr/lib', # % spec['lapack'].prefix, #FIXME
                        '-DTPL_ENABLE_Boost:BOOL=ON',
                        '-DBOOST_BASE_DIR:PATH=%s' % spec['boost'].prefix,
                        '-DTrilinos_ENABLE_Fortran=OFF', # FIXME
                        '-DTrilinos_ENABLE_EXPLICIT_INSTANTIATION:BOOL=ON',
                        '-DTrilinos_ENABLE_CXX11:BOOL=ON',
                        '-DTrilinos_CXX11_FLAGS=-std=c++11',
                        '-DTPL_ENABLE_Netcdf:BOOL=ON',
                        '-DTPL_ENABLE_HYPRE:BOOL=ON',
                        '-DTPL_ENABLE_HDF5:BOOL=ON',
                        '-DTPL_ENABLE_TBB:BOOL=ON'
                        ])

        # Amesos, conflicting types of double and complex SLU_D
        # see https://trilinos.org/pipermail/trilinos-users/2015-March/004731.html
        # and https://trilinos.org/pipermail/trilinos-users/2015-March/004802.html
        options.extend([
            '-DTeuchos_ENABLE_COMPLEX:BOOL=OFF',
            '-DKokkosTSQR_ENABLE_Complex:BOOL=OFF'
        ])

        # suite-sparse related
        options.extend([
            '-DTPL_ENABLE_Cholmod:BOOL=ON',
            '-DTPL_ENABLE_UMFPACK:BOOL=ON',
            '-DUMFPACK_LIBRARY_NAMES=umfpack;amd;colamd;cholmod;suitesparseconfig'
        ])

        # metis / parmetis
        options.extend([
            '-DTPL_ENABLE_METIS:BOOL=ON',
            '-DMETIS_LIBRARY_DIRS=%s' % spec['metis'].prefix.lib,
            '-DMETIS_LIBRARY_NAMES=metis',
            '-DTPL_METIS_INCLUDE_DIRS=%s' % spec['metis'].prefix.include,
            '-DTPL_ENABLE_ParMETIS:BOOL=ON',
            '-DParMETIS_LIBRARY_DIRS=%s;%s' % (spec['parmetis'].prefix.lib,spec['metis'].prefix.lib),
            '-DParMETIS_LIBRARY_NAMES=parmetis;metis',
            '-DTPL_ParMETIS_INCLUDE_DIRS=%s' % spec['parmetis'].prefix.include
        ])

        # mumps
        options.extend([
            '-DTPL_ENABLE_MUMPS:BOOL=ON"',
            '-DMUMPS_LIBRARY_DIRS=%s' % spec['mumps'].prefix.lib,
            '-DMUMPS_LIBRARY_NAMES=dmumps;mumps_common;pord' # order is important!
        ])

        # scalapack
        options.extend([
            '-DTPL_ENABLE_SCALAPACK:BOOL=ON',
            '-DSCALAPACK_LIBRARY_NAMES=scalapack' # FIXME: for MKL it's mkl_scalapack_lp64;mkl_blacs_mpich_lp64
        ])

        # superlu_dist
        options.extend([
            '-DTPL_ENABLE_SuperLUDist:BOOL=ON',
            '-DSuperLUDist_INCLUDE_DIRS=%s' % spec['superlu_dist'].prefix.include
        ])
        if spec.satisfies('^superlu-dist@4.0:'):
            options.extend([
                '-DHAVE_SUPERLUDIST_LUSTRUCTINIT_2ARG:BOOL=ON'
            ])


        # disable due to compiler / config errors:
        options.extend([
            '-DTrilinos_ENABLE_SEACAS=OFF',
            '-DTrilinos_ENABLE_Pike=OFF',
            '-DTrilinos_ENABLE_STK=OFF'
        ])

        if self.compiler.name == "clang":
            os.environ['CPPFLAGS']="-Qunused-arguments"

        #os.environ['LDFLAGS']="lgfortran"

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make('install')
