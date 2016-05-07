from spack import *

class Dia(Package):
    """Dia is a program for drawing structured diagrams."""
    homepage  = 'https://wiki.gnome.org/Apps/Dia'
    url       = 'https://ftp.gnome.org/pub/gnome/sources/dia/0.97/dia-0.97.3.tar.xz'

    version('0.97.3',    '0e744a0f6a6c4cb6a089e4d955392c3c')

    depends_on('intltool')
    depends_on('gtkplus@2.6.0:')
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

    def install(self, spec, prefix):

        # configure, build, install:
        options = ['--prefix=%s' % prefix,
                   '--with-cairo',
                   '--with-xslt-prefix=%s' % spec['libxslt'].prefix,
                   '--with-python',
                   '--with-swig']

        configure(*options)
        make()
        make('install')
