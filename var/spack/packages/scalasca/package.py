# FIXME: Add copyright

from spack import *

class Scalasca(Package):
    """Scalasca is a software tool that supports the performance optimization
       of parallel programs by measuring and analyzing their runtime behavior. 
       The analysis identifies potential performance bottlenecks - in 
       particular those concerning communication and synchronization - and 
       offers guidance in exploring their causes."""

    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.scalasca.org"
    url      = "http://apps.fz-juelich.de/scalasca/releases/scalasca/2.1/dist/scalasca-2.1-rc2.tar.gz"

    version('2.1-rc2', '1a95a39e5430539753e956a7524a756b')

    depends_on("mpi")
    depends_on("otf2@1.4")
    depends_on("cube")

    def install(self, spec, prefix):
        configure_args = ["--prefix=%s" % prefix,
                          "--with-otf2=%s" % spec['otf2'].prefix.bin,
                          "--with-cube=%s" % spec['cube'].prefix.bin,
                          "--enable-shared"]

        if spec.satisfies('%gcc'):
            configure_args.append('--with-nocross-compiler-suite=gcc')
        if spec.satisfies('%intel'):
            configure_args.append('--with-nocross-compiler-suite=intel')

        configure(*configure_args)

        make()
        make("install")

        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
