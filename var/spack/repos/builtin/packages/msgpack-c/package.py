from spack import *

class MsgpackC(Package):
    """A small, fast binary interchange format convertible to/from JSON"""
    homepage = "http://www.msgpack.org"
    url      = "https://github.com/msgpack/msgpack-c/archive/cpp-1.4.1.tar.gz"

    version('1.4.1', 'e2fd3a7419b9bc49e5017fdbefab87e0')

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)

        make()
        make("install")
