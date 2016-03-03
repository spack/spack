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

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')
    version('3.4.2', '61bf1a8a4469d4bdb7604f5897179478')
    version('3.4.1', '44c3869c38c8335c2b9c2a8bb276eb55')
    version('3.4.0', '02d5706ec03ba885fc246e5fa10d8c70')
    version('3.3.1', 'd0d533ec9a5b74933c2a1e84eedc58b4')

    variant('debug', default=False, description='Activates the Debug build type')
    variant('shared', default=True, description="Build shared library version")

    variant('lapacke', default=True, description='Activates the build of the LAPACKE C interface')

    # virtual dependency
    provides('blas')
    provides('lapack')

    depends_on('cmake')

    def install(self, spec, prefix):
        cmake_args = ['-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if '+shared' in spec else 'OFF'),
                      '-DCMAKE_BUILD_TYPE:STRING=%s' % ('Debug' if '+debug' in spec else 'Release'),
                      '-DLAPACKE:BOOL=%s' % ('ON' if '+lapacke' in spec else 'OFF')]
        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make("install")
