from spack import *

class M4(Package):
    """GNU M4 is an implementation of the traditional Unix macro processor."""
    homepage = "https://www.gnu.org/software/m4/m4.html"
    url      = "ftp://ftp.gnu.org/gnu/m4/m4-1.4.17.tar.gz"

    version('1.4.17', 'a5e9954b1dae036762f7b13673a2cf76')

    patch('inline-pgi.patch', when='@1.4.17')

    variant('sigsegv', default=True, description="Build the libsigsegv dependency")

    depends_on('libsigsegv', when='+sigsegv')

    def install(self, spec, prefix):
        # After patch, update generated configuration files that depend on extern-inline.m4
        autoreconf = which('autoreconf')
        autoreconf()

        configure_args = []
        if 'libsigsegv' in spec:
            configure_args.append('--with-libsigsegv-prefix=%s' % spec['libsigsegv'].prefix)
        else:
            configure_args.append('--without-libsigsegv-prefix')

        configure("--prefix=%s" % prefix, *configure_args)
        make()
        make("install")
