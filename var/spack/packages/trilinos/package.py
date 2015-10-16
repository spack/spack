from spack import *


class Trilinos(Package):
    """
    The Trilinos Project is an effort to develop algorithms and enabling technologies within an object-oriented
    software framework for the solution of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """
    homepage = "https://trilinos.org/"
    url = "http://trilinos.csbsju.edu/download/files/trilinos-12.2.1-Source.tar.gz"

    version('12.2.1', '6161926ea247863c690e927687f83be9')
    version('12.0.1', 'bd99741d047471e127b8296b2ec08017')
    version('11.14.3', '2f4f83f8333e4233c57d0f01c4b57426')
    version('11.14.2', 'a43590cf896c677890d75bfe75bc6254')
    version('11.14.1', '40febc57f76668be8b6a77b7607bb67f')

    variant('mpi', default=True, description='Add a dependency on MPI and enables MPI dependent packages')

    # Everything should be compiled with -fpic
    depends_on('blas')
    depends_on('lapack')
    depends_on('boost')
    depends_on('netcdf')
    depends_on('matio')
    depends_on('glm')
    depends_on('swig')
    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):

        options = [
            '-DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON',
            '-DTrilinos_ENABLE_TESTS:BOOL=OFF',
            '-DTrilinos_ENABLE_EXAMPLES:BOOL=OFF',
            '-DBUILD_SHARED_LIBS:BOOL=ON',
            '-DBLAS_LIBRARY_DIRS:PATH=%s' % spec['blas'].prefix,
            '-DLAPACK_LIBRARY_DIRS:PATH=%s' % spec['lapack'].prefix
        ]
        if '+mpi' in spec:
            mpi_options = ['-DTPL_ENABLE_MPI:BOOL=ON']
            options.extend(mpi_options)

        # -DCMAKE_INSTALL_PREFIX and all the likes...
        options.extend(std_cmake_args)
        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make('install')
