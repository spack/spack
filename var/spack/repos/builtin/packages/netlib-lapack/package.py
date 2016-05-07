from spack import *


class NetlibLapack(Package):
    """
    LAPACK version 3.X is a comprehensive FORTRAN library that does linear algebra operations including matrix
    inversions, least squared solutions to linear sets of equations, eigenvector analysis, singular value
    decomposition, etc. It is a very comprehensive and reputable package that has found extensive use in the
    scientific community.
    """
    homepage = "http://www.netlib.org/lapack/"
    url = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.6.0', 'f2f6c67134e851fe189bb3ca1fbb5101')
    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')
    version('3.4.2', '61bf1a8a4469d4bdb7604f5897179478')
    version('3.4.1', '44c3869c38c8335c2b9c2a8bb276eb55')
    version('3.4.0', '02d5706ec03ba885fc246e5fa10d8c70')
    version('3.3.1', 'd0d533ec9a5b74933c2a1e84eedc58b4')

    variant('debug', default=False, description='Activates the Debug build type')
    variant('shared', default=True, description="Build shared library version")
    variant('external-blas', default=False, description='Build lapack with an external blas')

    variant('lapacke', default=True, description='Activates the build of the LAPACKE C interface')

    # virtual dependency
    provides('blas', when='~external-blas')
    provides('lapack')

    depends_on('cmake')
    depends_on('blas', when='+external-blas')


    def patch(self):
        # Fix cblas CMakeLists.txt -- has wrong case for subdirectory name.
        if self.spec.satisfies('@3.6.0:'):
            filter_file('${CMAKE_CURRENT_SOURCE_DIR}/CMAKE/',
                        '${CMAKE_CURRENT_SOURCE_DIR}/cmake/', 'CBLAS/CMakeLists.txt', string=True)

    def install_one(self, spec, prefix, shared):
        cmake_args = ['-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if shared else 'OFF'),
                      '-DCMAKE_BUILD_TYPE:STRING=%s' % ('Debug' if '+debug' in spec else 'Release'),
                      '-DLAPACKE:BOOL=%s' % ('ON' if '+lapacke' in spec else 'OFF')]
        if spec.satisfies('@3.6.0:'):
            cmake_args.extend(['-DCBLAS=ON']) # always build CBLAS

        if '+external-blas' in spec:
            # TODO : the mechanism to specify the library should be more general,
            # TODO : but this allows to have an hook to an external blas
            cmake_args.extend([
                '-DUSE_OPTIMIZED_BLAS:BOOL=ON',
                '-DBLAS_LIBRARIES:PATH=%s' % join_path(spec['blas'].prefix.lib, 'libblas.a')
            ])

        cmake_args.extend(std_cmake_args)

        build_dir = 'spack-build' + ('-shared' if shared else '-static')
        with working_dir(build_dir, create=True):
            cmake('..', *cmake_args)
            make()
            make("install")


    def install(self, spec, prefix):
        # Always build static libraries.
        self.install_one(spec, prefix, False)

        # Build shared libraries if requested.
        if '+shared' in spec:
            self.install_one(spec, prefix, True)


    def setup_dependent_package(self, module, dspec):
        # This is WIP for a prototype interface for virtual packages.
        # We can update this as more builds start depending on BLAS/LAPACK.
        libdir = find_library_path('libblas.a', self.prefix.lib64, self.prefix.lib)

        self.spec.blas_static_lib   = join_path(libdir, 'libblas.a')
        self.spec.lapack_static_lib = join_path(libdir, 'liblapack.a')

        if '+shared' in self.spec:
            self.spec.blas_shared_lib   = join_path(libdir, 'libblas.%s' % dso_suffix)
            self.spec.lapack_shared_lib = join_path(libdir, 'liblapack.%s' % dso_suffix)
