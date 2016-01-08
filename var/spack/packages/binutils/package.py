from spack import *

class Binutils(Package):
    """GNU binutils, which contain the linker, assembler, objdump and others"""
    homepage = "http://www.gnu.org/software/binutils/"
    url      = "ftp://ftp.gnu.org/gnu/binutils/binutils-2.25.tar.bz2"

    version('2.25', 'd9f3303f802a5b6b0bb73a335ab89d66')
    version('2.24', 'e0f71a7b2ddab0f8612336ac81d9636b')
    version('2.23.2', '4f8fa651e35ef262edc01d60fb45702e')
    version('2.20.1', '2b9dc8f2b7dbd5ec5992c6e29de0b764')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
