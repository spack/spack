from spack import *

class Stat(Package):
    """Library to create, manipulate, and export graphs Graphlib."""
    homepage = "http://paradyn.org/STAT/STAT.html"
    url      = "https://github.com/lee218llnl/stat/archive/v2.0.0.tar.gz"

    versions = { '2.0.0' : 'c7494210b0ba26b577171b92838e1a9b', }
    versions = { '2.1.0' : 'ece26beaf057aa9134d62adcdda1ba91', }

    depends_on('libdwarf')
    depends_on('dyninst')
    depends_on('graphlib')
    depends_on('launchmon')
    depends_on('mrnet')

    def install(self, spec, prefix):
        configure(
            "--enable-gui",
            "--prefix=%s" % prefix,
            "--with-launchmon=%s"   % spec['launchmon'].prefix,
            "--with-mrnet=%s"       % spec['mrnet'].prefix,
            "--with-graphlib=%s"    % spec['graphlib'].prefix,
            "--with-stackwalker=%s" % spec['dyninst'].prefix,
            "--with-libdwarf=%s"    % spec['libdwarf'].prefix)

        # TODO: remove once SPACK-19 is fixed
        import shutil
        shutil.copy2('/usr/bin/libtool', 'libtool')

        make(parallel=False)
        make("install")
