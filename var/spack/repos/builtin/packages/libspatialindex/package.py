from spack import *

class Libspatialindex(Package):
    homepage = "http://http://libspatialindex.github.io"
    url      = "https://github.com/libspatialindex/libspatialindex/tarball/1.8.5"

    version('1.8.5', 'a95d8159714dbda9a274792cd273d298')

    depends_on("cmake")

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)
        make()
        make("install")
