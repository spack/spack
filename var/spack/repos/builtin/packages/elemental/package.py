from spack import *

class Elemental(Package):
    """Elemental is an open-source library for distributed-memory dense and sparse-direct linear algebra and optimization which builds on top of BLAS, LAPACK, and MPI"""
    homepage = "http://libelemental.org"
    url      = "http://libelemental.org/pub/releases/Elemental-0.85.tgz"

    version('0.85', 'b2d70758ad03e3f532010bd621bf9591')
    version('0.84', 'eb0b1bc7d8ddd15ac2a290a2f9d6573b')

    depends_on("cmake @2.8.8:")   # build dependency
    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = [arg
                for arg in std_cmake_args
                if not arg.startswith('-DCMAKE_BUILD_TYPE=')]
            cmake_args += [
                '-DCMAKE_BUILD_TYPE=HybridRelease',
                '-DMATH_LIBS=-L%s -llapack -L%s -lblas' %
                    (spec['lapack'].prefix.lib, spec['blas'].prefix.lib)]
            cmake('..', *cmake_args)
            make()
            make("install")
