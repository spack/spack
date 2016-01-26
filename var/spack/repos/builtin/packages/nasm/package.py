from spack import *

class Nasm(Package):
    """NASM (Netwide Assembler) is an 80x86 assembler designed for
       portability and modularity. It includes a disassembler as well."""
    homepage = "http://www.nasm.us"
    url      = "http://www.nasm.us/pub/nasm/releasebuilds/2.11.06/nasm-2.11.06.tar.xz"

    version('2.11.06', '2b958e9f5d200641e6fc9564977aecc5')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
