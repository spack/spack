from spack import *

class Binutils(Package):
    """GNU binutils, which contain the linker, assembler, objdump and others"""
    homepage = "http://www.gnu.org/software/binutils/"

    version('2.25', 'd9f3303f802a5b6b0bb73a335ab89d66',url="ftp://ftp.gnu.org/gnu/binutils/binutils-2.25.tar.bz2")
    version('2.24', 'e0f71a7b2ddab0f8612336ac81d9636b',url="ftp://ftp.gnu.org/gnu/binutils/binutils-2.24.tar.bz2")
    version('2.23.2', '4f8fa651e35ef262edc01d60fb45702e',url="ftp://ftp.gnu.org/gnu/binutils/binutils-2.23.2.tar.bz2")
    version('2.20.1', '2b9dc8f2b7dbd5ec5992c6e29de0b764',url="ftp://ftp.gnu.org/gnu/binutils/binutils-2.20.1.tar.bz2")

    # Add a patch that creates binutils libiberty_pic.a which is preferred by OpenSpeedShop and cbtf-krell
    variant('krellpatch', default=False, description="build with openspeedshop based patch.")
    patch('binutilskrell-2.24.patch', when='@2.24+krellpatch')

    def install(self, spec, prefix):

        # Add additional configuration options for use in the OpenSpeedShop project
        if '+krellpatch' in spec:
            configure('--prefix', self.prefix,
                      '--libdir', self.prefix.lib,
                      '--enable-shared',
                      '--enable-install-libiberty',
                      '--disable-multilib'
                      )
        else:
            configure("--prefix=%s" % prefix)


        make()
        make("install")
