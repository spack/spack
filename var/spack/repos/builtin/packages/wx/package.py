from spack import *

class Wx(Package):
    """wxWidgets is a C++ library that lets developers create
       applications for Windows, Mac OS X, Linux and other platforms
       with a single code base. It has popular language bindings for
       Python, Perl, Ruby and many other languages, and unlike other
       cross-platform toolkits, wxWidgets gives applications a truly
       native look and feel because it uses the platform's native API
       rather than emulating the GUI. It's also extensive, free,
       open-source and mature."""
    homepage = "http://www.wxwidgets.org/"

    version('2.8.12', '2fa39da14bc06ea86fe902579fedc5b1',
            url="https://sourceforge.net/projects/wxwindows/files/2.8.12/wxWidgets-2.8.12.tar.gz")
    version('3.0.1', 'dad1f1cd9d4c370cbc22700dc492da31',
            url="https://sourceforge.net/projects/wxwindows/files/3.0.1/wxWidgets-3.0.1.tar.bz2")

    depends_on('gtkplus')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--enable-unicode", "--disable-precomp-headers")

        make(parallel=False)
        make("install")

