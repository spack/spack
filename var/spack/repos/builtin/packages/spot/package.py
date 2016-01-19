from spack import *
import os

class Spot(Package):
    """Spot is a C++11 library for omega-automata manipulation and model checking."""
    homepage = "https://spot.lrde.epita.fr/index.html"
    url      = "http://www.lrde.epita.fr/dload/spot/spot-1.99.3.tar.gz"

    version('1.99.3', 'd53adcb2d0fe7c69f45d4e595a58254e')

    #depends_on("gcc@4.8:")
    depends_on("python@3.2:")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
