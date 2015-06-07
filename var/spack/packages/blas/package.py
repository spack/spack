from spack import *
import os

class Blas(Package):
    """The BLAS (Basic Linear Algebra Subprograms) are routines that provide standard 
    building blocks for performing basic vector and matrix operations."""

    homepage = "http://www.netlib.org/blas/"

    version('unversioned', '5e99e975f7a1e3ea6abcad7c6e7e42e6', 
        url='http://www.netlib.org/blas/blas.tgz')

    def install(self, spec, prefix):    
        make()
        mkdirp('%s' % prefix.lib) # Create the lib dir inside the install dir.
        move('./blas_LINUX.a', '%s/libblas.a' % prefix.lib) # Rename the generated lib file to libblas.a
        
