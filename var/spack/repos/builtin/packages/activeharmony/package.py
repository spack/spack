from spack import *

class Activeharmony(Package):
    """Active Harmony: a framework for auto-tuning (the automated search for values to improve the performance of a target application)."""
    homepage = "http://www.dyninst.org/harmony"
    url      = "http://www.dyninst.org/sites/default/files/downloads/harmony/ah-4.5.tar.gz"

    version('4.5', 'caee5b864716d376e2c25d739251b2a9')

    def install(self, spec, prefix):
        make("CFLAGS=-O3")
        make("install", 'PREFIX=%s' % prefix)

from spack import *

