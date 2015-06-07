from spack import *
import os
import shutil

class Parpack(Package):
    """ARPACK is a collection of Fortran77 subroutines designed to solve large
       scale eigenvalue problems."""

    homepage = "http://www.caam.rice.edu/software/ARPACK/download.html"
    url      = "http://www.caam.rice.edu/software/ARPACK/SRC/parpack96.tar.Z"

    version('96', 'a175f70ff71837a33ff7e4b0b6054f43')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')

    def patch(self):
        # Filter the CJ makefile to make a spack one.
        shutil.move('ARMAKES/ARmake.CJ', 'ARmake.inc')
        mf = FileFilter('ARmake.inc')

        # Be sure to use Spack F77 wrapper
        mf.filter('^FC.*',     'FC = f77')
        mf.filter('^FFLAGS.*', 'FFLAGS = -O2 -g')

        # Set up some variables.
        mf.filter('^PLAT.*',      'PLAT = ')
        mf.filter('^home.*',      'home = %s' % os.getcwd())
        mf.filter('^BLASdir.*',   'BLASdir = %s' % self.spec['blas'].prefix)
        mf.filter('^LAPACKdir.*', 'LAPACKdir = %s' % self.spec['lapack'].prefix)
        mf.filter('^MAKE.*',      'MAKE = make')

        # build the library in our own prefix.
        mf.filter('^ARPACKLIB.*', 'PARPACKLIB = %s/libparpack.a' % os.getcwd())


    def install(self, spec, prefix):
        with working_dir('PARPACK/SRC/MPI'):
            make('all')

        mkdirp(prefix.lib)
        install('libparpack.a', prefix.lib)
