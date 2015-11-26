from spack import *

class Libxslt(Package):
    """Libxslt is the XSLT C library developed for the GNOME
       project. XSLT itself is a an XML language to define
       transformation for XML. Libxslt is based on libxml2 the XML C
       library developed for the GNOME project. It also implements
       most of the EXSLT set of processor-portable extensions
       functions and some of Saxon's evaluate and expressions
       extensions."""
    homepage = "http://www.xmlsoft.org/XSLT/index.html"
    url      = "http://xmlsoft.org/sources/libxslt-1.1.28.tar.gz"

    version('1.1.28', '9667bf6f9310b957254fdcf6596600b7')

    depends_on("libxml2")
    depends_on("xz")
    depends_on("zlib")
    depends_on("libgcrypt")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
