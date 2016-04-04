from spack import *

class Dia(Package):
    """Dia is a program for drawing structured diagrams."""
    homepage  = 'https://wiki.gnome.org/Apps/Dia'
    url       = 'https://ftp.gnome.org/pub/gnome/sources/dia/0.97/dia-0.97.3.tar.xz'

    version('0.97.3',    '0e744a0f6a6c4cb6a089e4d955392c3c')

    #variant('ncurses', default=True, description='Enables the build of the ncurses gui')
    #variant('openssl', default=True, description="Enables CMake's OpenSSL features")
    #variant('qt', default=False, description='Enables the build of cmake-gui')
    #variant('doc', default=False, description='Enables the generation of html and man page documentation')

    depends_on('gtkplus@2.6.0:')
    # depends_on('openssl', when='+openssl')
    #depends_on('qt', when='+qt')
    #depends_on('python@2.7.11:', when='+doc')
    depends_on('cairo')
    #depends_on('libart') # optional dependency, not yet supported by spack.
    depends_on('libpng')
    depends_on('libxslt')
    depends_on('python')
    depends_on('swig')
    # depends_on('py-gtk') # optional dependency, not yet supported by spack.

    def url_for_version(self, version):
        """Handle Dia's version-based custom URLs."""
        return 'https://ftp.gnome.org/pub/gnome/source/dia/%s/dia-%s.tar.xz' % (version.up_to(2), version)

    # def validate(self, spec):
    #     """
    #     Checks if incompatible versions of qt were specified

    #     :param spec: spec of the package
    #     :raises RuntimeError: in case of inconsistencies
    #     """

    #     if '+qt' in spec and spec.satisfies('^qt@5.4.0'):
    #         msg = 'qt-5.4.0 has broken CMake modules.'
    #         raise RuntimeError(msg)

    def install(self, spec, prefix):
        # Consistency check
        # self.validate(spec)

        # configure, build, install:
        options = ['--prefix=%s' % prefix,
                   '--with-cairo',
                   '--with-xslt-prefix=%s' % spec['libxslt'].prefix,
                   '--with-python',
                   '--with-swig']

        # if '+qt' in spec:
        #     options.append('--qt-gui')

        # if '+doc' in spec:
        #     options.append('--sphinx-html')
        #     options.append('--sphinx-man')

        # if '+openssl' in spec:
        #     options.append('--')
        #     options.append('-DCMAKE_USE_OPENSSL=ON')

        configure(*options)
        make()
        make('install')
