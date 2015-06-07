from spack import *

class PyGenders(Package):
    """Genders is a static cluster configuration database used for cluster configuration management. It is used by a variety of tools and scripts for management of large clusters."""
    homepage = "https://github.com/chaos/genders"
    url      = "https://github.com/chaos/genders/releases/download/genders-1-22-1/genders-1.22.tar.gz"

    version('1.22', '9ea59a024dcbddb85b0ed25ddca9bc8e', url='https://github.com/chaos/genders/releases/download/genders-1-22-1/genders-1.22.tar.gz')
    extends('python')

    def install(self, spec, prefix):
        configure("--prefix=%s" %prefix)
        make(parallel=False)
        make("install")

