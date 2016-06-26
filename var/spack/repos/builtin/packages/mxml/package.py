import os
from spack import *

class Mxml(Package):
    """Mini-XML is a small XML library that you can use to read and write XML 
       and XML-like data files in your application without requiring large 
       non-standard libraries
    """

    homepage = "http://www.msweet.org"
    url      = "http://www.msweet.org/files/project3/mxml-2.9.tar.gz"

    version('2.9', 'e21cad0f7aacd18f942aa0568a8dee19')
    version('2.8', 'd85ee6d30de053581242c4a86e79a5d2')
    version('2.7', '76f2ae49bf0f5745d5cb5d9507774dc9')
    version('2.6', '68977789ae64985dddbd1a1a1652642e')
    version('2.5', 'f706377fba630b39fa02fd63642b17e5')

    # module swap PrgEnv-intel PrgEnv-$COMP (Can use whatever compiler you want to use) 
    # Case statement to change CC and CXX flags

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix, "--disable-shared", 'CFLAGS=-static')
        make()
        make("install")

