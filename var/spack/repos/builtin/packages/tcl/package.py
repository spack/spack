from spack import *

class Tcl(Package):
    """Tcl (Tool Command Language) is a very powerful but easy to
       learn dynamic programming language, suitable for a very wide
       range of uses, including web and desktop applications,
       networking, administration, testing and many more. Open source
       and business-friendly, Tcl is a mature yet evolving language
       that is truly cross platform, easily deployed and highly
       extensible."""
    homepage = "http://www.tcl.tk"

    version('8.6.3', 'db382feca91754b7f93da16dc4cdad1f',
            url="http://prdownloads.sourceforge.net/tcl/tcl8.6.3-src.tar.gz")

    depends_on('zlib')

    def install(self, spec, prefix):
        with working_dir('unix'):
            configure("--prefix=%s" % prefix)
            make()
            make("install")
