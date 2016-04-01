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
    urlpat = 'http://prdownloads.sourceforge.net/tcl/tcl%s-src.tar.gz'

    version('8.6.5', '0e6426a4ca9401825fbc6ecf3d89a326', url=urlpat%'8.6.5')
    version('8.6.4', 'd7cbb91f1ded1919370a30edd1534304', url=urlpat%'8.6.4')
    version('8.6.3', 'db382feca91754b7f93da16dc4cdad1f', url=urlpat%'8.6.3')
    version('8.5.19', '0e6426a4ca9401825fbc6ecf3d89a326', url=urlpat%'8.6.5')

    depends_on('zlib')

    def install(self, spec, prefix):
        with working_dir('unix'):
            configure("--prefix=%s" % prefix)
            make()
            make("install")
