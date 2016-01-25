from spack import *
import os
import shutil

class Arpack(Package):
    """A collection of Fortran77 subroutines designed to solve large scale
       eigenvalue problems.
    """
    homepage = "http://www.caam.rice.edu/software/ARPACK/"
    url      = "http://www.caam.rice.edu/software/ARPACK/SRC/arpack96.tar.gz"

    version('96', 'fffaa970198b285676f4156cebc8626e')

    depends_on('blas')
    depends_on('lapack')

    def patch(self):
        # Filter the cray makefile to make a spack one.
        shutil.move('ARMAKES/ARmake.CRAY', 'ARmake.inc')
        makefile = FileFilter('ARmake.inc')

        # Be sure to use Spack F77 wrapper
        makefile.filter('^FC.*', 'FC = f77')
        makefile.filter('^FFLAGS.*', 'FFLAGS = -O2 -g')

        # Set up some variables.
        makefile.filter('^PLAT.*',      'PLAT = ')
        makefile.filter('^home.*',    'home = %s' % os.getcwd())
        makefile.filter('^BLASdir.*',   'BLASdir = %s' % self.spec['blas'].prefix)
        makefile.filter('^LAPACKdir.*', 'LAPACKdir = %s' % self.spec['lapack'].prefix)

        # build the library in our own prefix.
        makefile.filter('^ARPACKLIB.*', 'ARPACKLIB = %s/libarpack.a' % os.getcwd())


    def install(self, spec, prefix):
        with working_dir('SRC'):
            make('all')

        mkdirp(prefix.lib)
        install('libarpack.a', prefix.lib)
