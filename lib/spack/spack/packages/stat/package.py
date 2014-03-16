from spack import *

class Stat(Package):
    """Library to create, manipulate, and export graphs Graphlib."""
    homepage = "http://paradyn.org/STAT/STAT.html"
    url      = "https://github.com/lee218llnl/stat/archive/v2.0.0.tar.gz"

    versions = { '2.0.0' : 'c7494210b0ba26b577171b92838e1a9b', }

    depends_on('libdwarf')
    depends_on('dyninst')
    depends_on('graphlib')
    #depends_on('launchmon') # TODO: when added, path gets too long (Jira SPACK-21)!
    depends_on('mrnet')

    def install(self, spec, prefix):
        configure(
            "--enable-gui",
            "--prefix=%s" % prefix,

            # TODO: this uses the launchmon package, but path is
            # too long (see depends_on above) (Jira SPACK-21)
            # "--with-launchmon=%s" % spec['launchmon'].prefix,

            # TODO: launchmon line above is the proper one once
            # SPACK-21 is fixed
            "--with-launchmon=/collab/usr/global/tools/launchmon/chaos_5_x86_64_ib/launchmon-1.0.0-20140312",

            "--with-mrnet=%s" % spec['mrnet'].prefix,
            "--with-graphlib=%s" % spec['graphlib'].prefix,
            "--with-stackwalker=%s" % spec['dyninst'].prefix,
            "--with-libdwarf=%s" % spec['libdwarf'].prefix)

        # TODO: remove once SPACK-19 is fixed
        import shutil
        shutil.copy2('/usr/bin/libtool', 'libtool')

        make(parallel=False)
        make("install")
