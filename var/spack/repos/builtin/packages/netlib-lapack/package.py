from spack import *

class NetlibLapack(Package):
    """
    LAPACK version 3.X is a comprehensive FORTRAN library that does
    linear algebra operations including matrix inversions, least
    squared solutions to linear sets of equations, eigenvector
    analysis, singular value decomposition, etc. It is a very
    comprehensive and reputable package that has found extensive
    use in the scientific community.
    """
    homepage = "http://www.netlib.org/lapack/"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.6.0', 'f2f6c67134e851fe189bb3ca1fbb5101')
    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')
    version('3.4.2', '61bf1a8a4469d4bdb7604f5897179478')
    version('3.4.1', '44c3869c38c8335c2b9c2a8bb276eb55')
    version('3.4.0', '02d5706ec03ba885fc246e5fa10d8c70')
    version('3.3.1', 'd0d533ec9a5b74933c2a1e84eedc58b4')

    variant('shared', default=True, description="Build shared library version")

    # virtual dependency
    provides('lapack')

    # blas is a virtual dependency.
    depends_on('blas')

    depends_on('cmake')

    # Doesn't always build correctly in parallel
    parallel = False

    @when('^netlib-blas')
    def get_blas_libs(self):
        blas = self.spec['netlib-blas']
        return [join_path(blas.prefix.lib, 'blas.a')]


    @when('^atlas')
    def get_blas_libs(self):
        blas = self.spec['atlas']
        return [join_path(blas.prefix.lib, l)
                for l in ('libf77blas.a', 'libatlas.a')]


    def install(self, spec, prefix):
        blas_libs = ";".join(self.get_blas_libs())
        cmake_args = [".", '-DBLAS_LIBRARIES=' + blas_libs]

        if '+shared' in spec:
            cmake_args.append('-DBUILD_SHARED_LIBS=ON')

        cmake_args += std_cmake_args

        cmake(*cmake_args)
        make()
        make("install")

