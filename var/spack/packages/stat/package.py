from spack import *

class Stat(Package):
    """Library to create, manipulate, and export graphs Graphlib."""
    homepage = "http://paradyn.org/STAT/STAT.html"
    url      = "https://github.com/lee218llnl/stat/archive/v2.0.0.tar.gz"

    version('2.0.0', 'c7494210b0ba26b577171b92838e1a9b')
    version('2.1.0', 'ece26beaf057aa9134d62adcdda1ba91')

    depends_on('libdwarf')
    depends_on('dyninst')
    depends_on('graphlib')
    depends_on('launchmon')
    depends_on('mrnet')

    patch('configure_mpicxx.patch', when='@2.1.0:')

    def install(self, spec, prefix):
        configure(
            "--enable-gui",
            "--prefix=%s" % prefix,
            "--disable-examples", # Examples require MPI: avoid this dependency.
            "--with-launchmon=%s"   % spec['launchmon'].prefix,
            "--with-mrnet=%s"       % spec['mrnet'].prefix,
            "--with-graphlib=%s"    % spec['graphlib'].prefix,
            "--with-stackwalker=%s" % spec['dyninst'].prefix,
            "--with-libdwarf=%s"    % spec['libdwarf'].prefix)

        make(parallel=False)
        make("install")
