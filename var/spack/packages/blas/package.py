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
        mv = which('mv') # Create a shell wrapper for the mv command.
        mkdir = which('mkdir') # Create a shell wrapper for the mkdir command.
        pwd = os.getcwd() # Retrieve the current working dir.
        mkdir('%s' % prefix.lib) # Create the lib dir inside the install dir.
        mv('%s/blas_LINUX.a' % pwd, '%s/libblas.a' % pwd) # Rename the generated lib file to libblas.a
        mv('%s/libblas.a' % pwd, '%s/libblas.a' % prefix.lib) # Move the library file to the install dir.
        
