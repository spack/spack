from spack import *

class Parpack(Package):
    """ARPACK is a collection of Fortran77 subroutines designed to solve large 
       scale eigenvalue problems."""

    homepage = "http://www.caam.rice.edu/software/ARPACK/download.html"
    url      = "http://www.caam.rice.edu/software/ARPACK/SRC/parpack96.tar.Z"

    version('96', 'a175f70ff71837a33ff7e4b0b6054f43')

    depends_on('blas')
    depends_on('lapack')

    def install(self, spec, prefix):
        move("./ARMAKES/ARmake.CJ", "./ARmake.inc");        
        filter_file('home = /home1/Netlib/ARPACK', 'home = %s' % pwd(), './ARmake.inc', string=True)
        filter_file('PLAT = CJ', 'PLAT = ', './ARmake.inc', string=True)
        filter_file('LAPACKdir    = $(home)/LAPACK', 'LAPACKLIB = %s' % spec['lapack'].prefix, './ARmake.inc', string=True)
        filter_file('BLASdir      = $(home)/BLAS', 'BLASLIB = %s' % spec['blas'].prefix, './ARmake.inc', string=True)
        filter_file('ARPACKLIB  = $(home)/libarpack_$(PLAT).a', 'ARPACKLIB = %s/libarpack.a' % prefix, './ARmake.inc', string=True)
        filter_file('MAKE    = /bin/make', 'MAKE = make', './ARmake.inc', string=True)
        filter_file('FFLAGS', '#FFLAGS', './ARmake.inc', string=True)
        filter_file('FC      = f77', 'FC = gfortran', './ARmake.inc', string=True)
        cd('./PARPACK/SRC/MPI')
        make('all')
