from spack import *

class Boxlib(Package):
    """BoxLib, a software framework for massively parallel block-structured adaptive mesh refinement (AMR) codes."""

    homepage = "https://ccse.lbl.gov/BoxLib/"
    url = "https://ccse.lbl.gov/pub/Downloads/BoxLib.git";

    version('master', 'https://ccse.lbl.gov/pub/Downloads/BoxLib.git')

    def install(self, spec, prefix):
        #configure("--prefix=%s" % prefix)
        #make()
        #make("install")
        cd(pwd())
