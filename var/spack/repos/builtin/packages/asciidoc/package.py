from spack import *

class Asciidoc(Package):
    """ A presentable text document format for writing articles, UNIX man
    pages and other small to medium sized documents."""
    homepage = "http://asciidoc.org"
    url      = "http://downloads.sourceforge.net/project/asciidoc/asciidoc/8.6.9/asciidoc-8.6.9.tar.gz"

    version('8.6.9', 'c59018f105be8d022714b826b0be130a')

    depends_on('libxml2')
    depends_on('libxslt')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
