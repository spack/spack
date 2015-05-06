from spack import *
import os

class Jasper(Package):
    """Description"""

    homepage = "http://www.example.com/jasper-1.0.tar.gz"
    url	     = "http://www.ece.uvic.ca/~frodo/jasper/software/jasper-1.900.1.zip"

    version('1.900.1')

    def setup_dependent_environment(self, module, spec, dep_spec):
        os.environ['JASPERLIB'] = self.prefix.lib
        os.environ['JASPERINC'] = self.prefix.include
        

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
