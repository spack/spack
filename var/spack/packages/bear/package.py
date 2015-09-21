from spack import *

class Bear(Package):
    """Bear is a tool that generates a compilation database for clang tooling from non-cmake build systems."""
    homepage = "https://github.com/rizsotto/Bear"
    url      = "https://github.com/rizsotto/Bear/archive/2.0.4.tar.gz"

    version('2.0.4', 'fd8afb5e8e18f8737ba06f90bd77d011')

    depends_on("cmake")
    depends_on("python")

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)

        make("all")
        make("install")
