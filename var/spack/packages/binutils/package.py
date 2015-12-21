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

    variant('libiberty', default=False, description='Also install libiberty.')

    def install(self, spec, prefix):
        configure_args = [
            '--prefix=%s' % prefix,
            '--disable-dependency-tracking',
            '--enable-interwork',
            '--enable-multilib',
            '--enable-shared',
            '--enable-64-bit-bfd',
            '--enable-targets=all',
            '--with-sysroot=/']

        if '+libiberty' in spec:
            configure_args.append('--enable-install-libiberty')

        configure(*configure_args)
        make()
        make("install")
