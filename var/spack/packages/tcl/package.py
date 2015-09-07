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
    

    version('8.6.4', 'd7cbb91f1ded1919370a30edd1534304',
            url = "http://prdownloads.sourceforge.net/tcl/tcl8.6.4-src.tar.gz")
    version('8.6.3', 'db382feca91754b7f93da16dc4cdad1f',
            url = "http://prdownloads.sourceforge.net/tcl/tcl8.6.3-src.tar.gz")

    variant('threads', default=False, description="enable threads")

    depends_on('zlib')

    def install(self, spec, prefix):
        configure_args = [
            "--prefix=%s" % prefix
            ]

        if '+threads' in spec:
            configure_args.append('--enable-threads')

        with working_dir('unix'):
            configure(*configure_args)
            make()
            make("install")

