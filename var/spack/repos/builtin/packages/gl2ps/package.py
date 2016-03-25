from spack import *

class Gl2ps(Package):
    """GL2PS is a C library providing high quality vector output for any
    OpenGL application."""

    homepage = "http://www.geuz.org/gl2ps/"
    url      = "http://geuz.org/gl2ps/src/gl2ps-1.3.9.tgz"

    version('1.3.9', '377b2bcad62d528e7096e76358f41140')

    depends_on("libpng")

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)

        make()
        make("install")
