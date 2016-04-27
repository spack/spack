from spack import *
import sys
import os
import llnl.util.tty as tty

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

    depends_on('cmake')
    depends_on('mpi')
    depends_on('lapack')
    depends_on('blas')

    def install(self, spec, prefix):
        # Look for both shared and static libraries, since we don't know what was built
        exts = ['.a', '.so']
        if '+shared' in spec:
            exts.reverse()

        # Find BLAS for the not-so-powerful CMake script
        blas_lib = None
        for ext in exts:
            blas_lib = os.path.join(spec['blas'].prefix, 'lib', 'libblas' + ext)
            if os.path.exists(blas_lib):
                break
        if blas_lib is None:
            tty.error('Cannot find libblas in path %s')


        # Find LAPACK for the not-so-powerful CMake script
        lapack_lib = None
        for ext in exts:
            lapack_lib = os.path.join(spec['lapack'].prefix, 'lib', 'liblapack' + ext)
            if os.path.exists(lapack_lib):
                break
        if lapack_lib is None:
            tty.error('Cannot find liblapack in path %s')


        # Prefer shared libraries
        options = [
            "-DBUILD_SHARED_LIBS:BOOL=%s" % ('ON' if '+shared' in spec else 'OFF'),
            "-DBUILD_STATIC_LIBS:BOOL=%s" % ('OFF' if '+shared' in spec else 'ON'),
            "-DUSE_OPTIMIZED_LAPACK_BLAS:BOOL=ON", # forces scalapack to use find_package(LAPACK)
            "-DBLAS_LIBRARIES=%s" % blas_lib,
            "-DLAPACK_LIBRARIES=%s" % lapack_lib,
            "-DBLAS_DIR=%s" % spec['blas'].prefix,
            "-DLAPACK_DIR=%s" % spec['lapack'].prefix,
            ]

        if '+fpic' in spec:
            options.extend([
                "-DCMAKE_C_FLAGS=-fPIC",
                "-DCMAKE_Fortran_FLAGS=-fPIC"
            ])

        options.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make("install")

        # The shared libraries are not installed correctly on Darwin; correct this
        if (sys.platform == 'darwin') and ('+shared' in spec):
            fix_darwin_install_name(prefix.lib)


    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec
        lib_dsuffix = '.dylib' if sys.platform == 'darwin' else '.so'
        lib_suffix = lib_dsuffix if '+shared' in spec else '.a'

        spec.fc_link = '-L%s -lscalapack' % spec.prefix.lib
        spec.cc_link = spec.fc_link
        spec.libraries = [join_path(spec.prefix.lib, 'libscalapack%s' % lib_suffix)]
