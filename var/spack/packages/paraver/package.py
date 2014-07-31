from spack import *
import os

class Paraver(Package):
    """"A very powerful performance visualization and analysis tool
        based on traces that can be used to analyse any information that
        is expressed on its input trace format.  Traces for parallel MPI,
        OpenMP and other programs can be genereated with Extrae."""
    homepage = "http://www.bsc.es/computer-sciences/performance-tools/paraver"
    url      = "http://www.bsc.es/ssl/apps/performanceTools/files/paraver-sources-4.5.2.tar.gz"

    version('4.5.2', 'ea463dd494519395c99ebae294edee17')

    depends_on("boost")
    #depends_on("extrae")
    depends_on("wx")
    depends_on("wxpropgrid")

    def install(self, spec, prefix):
        os.chdir("ptools_common_files")
        configure("--prefix=%s" % prefix)
        make()
        make("install")

        os.chdir("../paraver-kernel")
		#"--with-extrae=%s" % spec['extrae'].prefix,
        configure("--prefix=%s" % prefix, "--with-ptools-common-files=%s" % prefix, "--with-boost=%s" % spec['boost'].prefix, "--with-boost-serialization=boost_serialization")
        make()
        make("install")

        os.chdir("../paraver-toolset")
        configure("--prefix=%s" % prefix)
        make()
        make("install")

        os.chdir("../wxparaver")
		#"--with-extrae=%s" % spec['extrae'].prefix,
        configure("--prefix=%s" % prefix, "--with-paraver=%s" % prefix, "--with-boost=%s" % spec['boost'].prefix, "--with-boost-serialization=boost_serialization", "--with-wxdir=%s" % spec['wx'].prefix.bin)
        make()
        make("install")

