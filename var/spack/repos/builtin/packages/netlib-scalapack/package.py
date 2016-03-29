from spack import *
import sys

class NetlibScalapack(Package):
    """ScaLAPACK is a library of high-performance linear algebra routines for parallel distributed memory machines"""

    homepage = "http://www.netlib.org/scalapack/"
    url      = "http://www.netlib.org/scalapack/scalapack-2.0.2.tgz"

    version('2.0.2', '2f75e600a2ba155ed9ce974a1c4b536f')
    version('2.0.1', '17b8cde589ea0423afe1ec43e7499161')
    version('2.0.0', '9e76ae7b291be27faaad47cfc256cbfe')
    # versions before 2.0.0 are not using cmake and requires blacs as
    # a separated package

    variant('shared', default=True, description='Build the shared library version')
    variant('fpic', default=False, description="Build with -fpic compiler option")

    provides('scalapack')

    depends_on('mpi')
    depends_on('lapack')

    def install(self, spec, prefix):
        options = [
            "-DBUILD_SHARED_LIBS:BOOL=%s" % ('ON' if '+shared' in spec else 'OFF'),
            "-DBUILD_STATIC_LIBS:BOOL=%s" % ('OFF' if '+shared' in spec else 'ON'),
            "-DUSE_OPTIMIZED_LAPACK_BLAS:BOOL=ON", # forces scalapack to use find_package(LAPACK)
            ]

        if '+fpic' in spec:
            options.extend([
                "-DCMAKE_C_FLAGS=-fPIC",
                "-DCMAKE_Fortran_FLAGS=-fPIC"
            ])

        options.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            which('cmake')('..', *options)
            make()
            make("install")

    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec
        lib_dsuffix = '.dylib' if sys.platform == 'darwin' else '.so'
        lib_suffix = lib_dsuffix if '+shared' in spec else '.a'

        spec.fc_link = '-L%s -lscalapack' % spec.prefix.lib
        spec.cc_link = spec.fc_link
        spec.libraries = [join_path(spec.prefix.lib, 'libscalapack%s' % lib_suffix)]
