from spack import *

class Icu(Package):
    """The International Components for Unicode (ICU) package is a
       mature, widely used set of C/C++ libraries providing Unicode and
       Globalization support for software applications. ICU is widely
       portable and gives applications the same results on all
       platforms."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://download.icu-project.org/files/icu4c/54.1/icu4c-54_1-src.tgz"

    version('54.1', 'e844caed8f2ca24c088505b0d6271bc0')


    def url_for_version(self, version):
        return "http://download.icu-project.org/files/icu4c/%s/icu4c-%s-src.tgz" % (
            version, str(version).replace('.', '_'))


    def install(self, spec, prefix):
        with working_dir("source"):
            configure("--prefix=%s" % prefix)
            make()
            make("install")
