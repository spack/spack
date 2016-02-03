from spack import *


class Trilinos(Package):
    """
    The Trilinos Project is an effort to develop algorithms and enabling technologies within an object-oriented
    software framework for the solution of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """
    homepage = "https://trilinos.org/"
    url = "http://trilinos.csbsju.edu/download/files/trilinos-12.2.1-Source.tar.gz"

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

    # MPI related dependencies
    depends_on('mpi')
    depends_on('netcdf+mpi')

    depends_on('python') #  Needs py-numpy activated

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        options.extend(['-DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON',
                        '-DTrilinos_ENABLE_TESTS:BOOL=OFF',
                        '-DTrilinos_ENABLE_EXAMPLES:BOOL=OFF',
                        '-DCMAKE_BUILD_TYPE:STRING=%s' % ('Debug' if '+debug' in spec else 'Release'),
                        '-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if '+shared' in spec else 'OFF'),
                        '-DTPL_ENABLE_MPI:STRING=ON',
                        '-DBLAS_LIBRARY_DIRS:PATH=%s' % spec['blas'].prefix,
                        '-DLAPACK_LIBRARY_DIRS:PATH=%s' % spec['lapack'].prefix
                        ])

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make('install')
