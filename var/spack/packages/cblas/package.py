from spack import *
import os

class Cblas(Package):
    """The BLAS (Basic Linear Algebra Subprograms) are routines that provide standard 
    building blocks for performing basic vector and matrix operations."""

    homepage = "http://www.netlib.org/blas/_cblas/"

    version('unversioned', '1e8830f622d2112239a4a8a83b84209a', 
        url='http://www.netlib.org/blas/blast-forum/cblas.tgz')

    depends_on('blas')
    parallel = False

    def install(self, spec, prefix):    
        filter_file('BLLIB = /Users/julie/Documents/Boulot/lapack-dev/lapack/trunk/blas_LINUX.a', 'BLLIB = %s/libblas.a' % spec['blas'].prefix.lib, './Makefile.in', string=True)
        
        make('all') # Compile.
        mkdirp('%s' % prefix.lib) # Create the lib dir inside the install dir.
        move('./lib/cblas_LINUX.a', '%s/libcblas.a' % prefix.lib) # Rename the generated lib file to libcblas.a
        
