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
        my_mrnet = spec['mrnet']
        my_graphlib = spec['graphlib']
        #my_launchmon = spec['launchmon']
        my_dyninst = spec['dyninst']
        my_libdwarf = spec['libdwarf']

        # TODO: this uses the launchmon package, but path is too long (see depends_on above) (Jira SPACK-21)
        #configure("--enable-gui", "--prefix=%s" %prefix, "--with-launchmon=%s" %my_launchmon.prefix, "--with-mrnet=%s" %my_mrnet.prefix, "--with-graphlib=%s" %my_graphlib.prefix, "--with-stackwalker=%s" %my_dyninst.prefix, "--with-libdwarf=%s" %my_libdwarf.prefix)

        # TODO: the configure line above is the proper one once Jira SPACK-21 is fixed
        configure("--enable-gui", "--prefix=%s" %prefix, "--with-launchmon=/collab/usr/global/tools/launchmon/chaos_5_x86_64_ib/launchmon-1.0.0-20140312", "--with-mrnet=%s" %my_mrnet.prefix, "--with-graphlib=%s" %my_graphlib.prefix, "--with-stackwalker=%s" %my_dyninst.prefix, "--with-libdwarf=%s" %my_libdwarf.prefix)

        # TODO: remove once Jira SPACK-19 is fixed
        import shutil
        shutil.copy2('/usr/bin/libtool', 'libtool')
    
        make(parallel=False)
        make("install")
