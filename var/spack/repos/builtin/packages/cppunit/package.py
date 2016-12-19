from spack import *

class Cppunit(Package):
    """Obsolete Unit testing framework for C++"""

    homepage = "https://wiki.freedesktop.org/www/Software/cppunit/"
    url      = "http://dev-www.libreoffice.org/src/cppunit-1.13.2.tar.gz"

    version('1.13.2', '0eaf8bb1dcf4d16b12bec30d0732370390d35e6f')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
