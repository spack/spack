from spack import *

class Arpack(Package):
    """FIXME: put a proper description of your package here."""
    homepage = "http://www.caam.rice.edu/software/ARPACK/"
    url      = "http://www.caam.rice.edu/software/ARPACK/SRC/arpack96.tar.gz"

    version('96', 'fffaa970198b285676f4156cebc8626e')

    depends_on('blas')
    depends_on('lapack')

    def install(self, spec, prefix):
        move('./ARMAKES/ARmake.CRAY', './ARmake.inc')
        filter_file('PLAT          = CRAY', 'PLAT = ', './ARmake.inc', string=True)
        filter_file('home = $(HOME)/ARPACK', 'home = %s' % pwd(), './ARmake.inc', string=True)
        filter_file('BLASdir      = $(home)/BLAS', 'BLASdir = %s' % spec['blas'].prefix, './ARmake.inc', string=True)
        filter_file('LAPACKdir    = $(home)/LAPACK', 'LAPACKdir = %s' % spec['lapack'].prefix, './ARmake.inc', string=True)
        filter_file('ARPACKLIB  = $(home)/libarpack_$(PLAT).a', 'ARPACKLIB = %s/lib/libarpack.a' % prefix, './ARmake.inc', string=True)
        
        cd('./SRC')
        make('all')
