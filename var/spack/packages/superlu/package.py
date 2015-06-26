from spack import *

class Superlu(Package):
    """SuperLU is a general purpose library for the direct solution of large, sparse, nonsymmetric systems of linear equations on high performance machines."""
    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    url      = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_dist_4.0.tar.gz"

    version('4.0', 'c0b98b611df227ae050bc1635c6940e0')
    version('3.3', 'f4805659157d93a962500902c219046b')
    version('3.2', 'b67bab5bb1ee92d38ad6c345b3c2b18d')
    version('3.1', '5b114d6f97d9e94d643f51bb3c6cf03f')
    version('3.0', '1d77f10a265f5751d4e4b59317d778f8')

    depends_on("metis")
    depends_on("parmetis")

    def install(self, spec, prefix):
        filter_file('PLAT		= _sp', 'PLAT = ', './make.inc', string=True)
        filter_file('DSuperLUroot 	= ${HOME}/Release_Codes/SuperLU_DIST-branch', 'DSuperLUroot = ' + prefix, string=True)
        filter_file('PARMETISLIB := -L${PARMETIS_DIR}/build/Linux-x86_64/libparmetis -lparmetis', 'PARMETIS_DIR := ' + spec['parmetis'].prefix + '/libparmetis -lparmetis', './make.inc', string=True)
        filter_file('METISLIB := -L${PARMETIS_DIR}/build/Linux-x86_64/libmetis -lmetis', 'METISLIB := ' + spec['metis'].prefix + '/libparmetis -lparmetis', './make.inc', string=True)
        filter_file('CFLAGS          = ${CUDA_FLAGS} ${INCS} -std=c99 -O3 -Wall -w2 -mkl -openmp \\', 'CFLAGS = -O2 -std=c99', './make.inc', string=True)
        filter_file('		-DDEBUGlevel=0 -DPRNTlevel=1 -DPROFlevel=0 \\', '', './make.inc', string=True)
        filter_file('F90FLAGS	= -fast -Mnomain', 'F90FLAGS = -O2', './make.inc', string=True)

        make('all')
