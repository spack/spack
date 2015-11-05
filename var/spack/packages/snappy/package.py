import os
from spack import *

class Snappy(Package):
    """A fast compressor/decompressor: https://code.google.com/p/snappy"""

    homepage = "https://code.google.com/p/snappy"
    url      = "https://github.com/google/snappy/releases/download/1.1.3/snappy-1.1.3.tar.gz"

    version('1.1.3', '7358c82f133dc77798e4c2062a749b73')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
