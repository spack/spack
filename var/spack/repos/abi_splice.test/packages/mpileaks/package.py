from spack.package import *


class Mpileaks(Package):
    homepage = "https://www.example.com"
    has_code = False
    depends_on("mpi")
    version("1.0")
    depends_on("mpi@1", when="@1.0")
    version("2.0")
    depends_on("mpi@2", when="@2.0")
    version("3.0")
    depends_on("mpi@3", when="@3.0")

    def install(self, spec, prefix):
        touch(prefix.foo)
