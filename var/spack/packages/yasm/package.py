from spack import *

class Yasm(Package):
    """Yasm is a complete rewrite of the NASM-2.11.06 assembler. It
       supports the x86 and AMD64 instruction sets, accepts NASM and
       GAS assembler syntaxes and outputs binary, ELF32 and ELF64
       object formats."""
    homepage = "http://yasm.tortall.net"
    url      = "http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz"

    version('1.3.0', 'fc9e586751ff789b34b1f21d572d96af')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
