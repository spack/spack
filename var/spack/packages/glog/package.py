import os
from spack import *

class Glog(Package):
    """C++ implementation of the Google logging module."""

    homepage = "https://github.com/google/glog"
    url      = "https://github.com/google/glog/archive/v0.3.3.tar.gz"

    version('0.3.3', 'c1f86af27bd9c73186730aa957607ed0')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
