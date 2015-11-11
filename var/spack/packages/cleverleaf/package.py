from spack import *

class Cleverleaf(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/cleverleaf-1.0.tar.gz"

    version('develop', git='git@github.com:UK-MAC/CleverLeaf_ref.git', branch='develop')

    depends_on("SAMRAI@3.8.0")

    def install(self, spec, prefix):
        cmake(*std_cmake_args)
        make()
        make("install")
