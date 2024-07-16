
from spack.package import *


class Openmpi(Package):

    homepage = "https://www.example.com"
    has_code = False


    provides("mpi")

    version("1.0")    
    can_splice("xmpi@6.0 abi=openmpi", when="@1.0")
    provides("mpi@1", when="@1.0")

    version("2.0")    
    provides("mpi@2", when="@2.0")
    can_splice("xmpi@7.0 abi=openmpi", when="@2.0")

    version("3.0")    
    provides("mpi@3", when="@3.0")
    can_splice("xmpi@8.0 abi=openmpi", when="@3.0")

    def install(self, spec, prefix):
        touch(prefix.foo)
    