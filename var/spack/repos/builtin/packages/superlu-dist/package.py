from spack import *

class SuperluDist(Package):
    """A general purpose library for the direct solution of large, sparse, nonsymmetric systems of linear equations on high performance machines."""
    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    url      = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_dist_4.1.tar.gz"

    version('4.3', 'ee66c84e37b4f7cc557771ccc3dc43ae')
    version('4.2', 'ae9fafae161f775fbac6eba11e530a65')
    version('4.1', '4edee38cc29f687bd0c8eb361096a455')
    version('4.0', 'c0b98b611df227ae050bc1635c6940e0')

    depends_on ('mpi')
    depends_on ('blas')
    depends_on ('lapack')
    depends_on ('parmetis')
    depends_on ('metis')

    def install(self, spec, prefix):
        makefile_inc = []
        makefile_inc.extend([
            'PLAT         = _mac_x',
            'DSuperLUroot = %s' % self.stage.source_path, #self.stage.path, prefix
            'DSUPERLULIB  = $(DSuperLUroot)/lib/libsuperlu_dist.a',
            'BLASDEF      = -DUSE_VENDOR_BLAS',
            'BLASLIB      = -L%s -llapack %s -lblas' % (spec['lapack'].prefix.lib, spec['blas'].prefix.lib), # FIXME: avoid hardcoding blas/lapack lib names
            'METISLIB     = -L%s -lmetis' % spec['metis'].prefix.lib,
            'PARMETISLIB  = -L%s -lparmetis' % spec['parmetis'].prefix.lib,
            'FLIBS        =',
            'LIBS         = $(DSUPERLULIB) $(BLASLIB) $(PARMETISLIB) $(METISLIB)',
            'ARCH         = ar',
            'ARCHFLAGS    = cr',
            'RANLIB       = true',
            'CC           = mpicc', # FIXME avoid hardcoding MPI compiler names
            'CFLAGS       = -fPIC -std=c99 -O2 -I%s -I%s' %(spec['parmetis'].prefix.include, spec['metis'].prefix.include),
            'NOOPTS       = -fPIC -std=c99',
            'FORTRAN      = mpif77',
            'F90FLAGS     = -O2',
            'LOADER       = mpif77',
            'LOADOPTS     =',
            'CDEFS        = -DAdd_'
            ])

        #with working_dir('src'):
        with open('make.inc', 'w') as fh:
            fh.write('\n'.join(makefile_inc))

        make("lib", parallel=False)

        # FIXME:
        # cd "EXAMPLE" do
        # system "make"

        # need to install by hand
        headers_location = join_path(self.prefix.include,'superlu_dist')
        mkdirp(headers_location)
        # FIXME: fetch all headers in the folder automatically
        for header in ['Cnames.h','cublas_utils.h','dcomplex.h','html_mainpage.h','machines.h','old_colamd.h','psymbfact.h','superlu_ddefs.h','superlu_defs.h','superlu_enum_consts.h','superlu_zdefs.h','supermatrix.h','util_dist.h']:
            superludist_header = join_path(self.stage.source_path, 'SRC/',header)
            install(superludist_header, headers_location)

        superludist_lib = join_path(self.stage.source_path, 'lib/libsuperlu_dist.a')
        install(superludist_lib,self.prefix.lib)
