import spack.compilers
import spack.tty as tty
from spack.colify import colify

description = "List available compilers"

def compilers(parser, args):
    tty.msg("Supported compilers")
    colify(spack.compilers.supported_compilers(), indent=4)
