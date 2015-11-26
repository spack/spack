from spack import *

class Libxml2(Package):
    """Libxml2 is the XML C parser and toolkit developed for the Gnome
       project (but usable outside of the Gnome platform), it is free
       software available under the MIT License."""
    homepage = "http://xmlsoft.org"
    url      = "http://xmlsoft.org/sources/libxml2-2.9.2.tar.gz"

    version('2.9.2', '9e6a9aca9d155737868b3dc5fd82f788')

    extends('python')
    depends_on('zlib')
    depends_on('xz')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
