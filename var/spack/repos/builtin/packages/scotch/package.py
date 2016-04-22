from spack import *
import os

class Scotch(Package):
    """Scotch is a software package for graph and mesh/hypergraph
       partitioning, graph clustering, and sparse matrix ordering."""

    homepage = "http://www.labri.fr/perso/pelegrin/scotch/"
    url = "http://gforge.inria.fr/frs/download.php/latestfile/298/scotch_6.0.3.tar.gz"
    list_url = "http://gforge.inria.fr/frs/?group_id=248"

    version('6.0.3', '10b0cc0f184de2de99859eafaca83cfc')
    version('5.1.10b', '9b8622b39c141ecaca4a46298486fd99')

    variant('mpi', default=False, description='Activate the compilation of PT-Scotch')
    variant('compression', default=True, description='Activate the posibility to use compressed files')
    variant('esmumps', default=False, description='Activate the compilation of the lib esmumps needed by mumps')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('flex')
    depends_on('bison')
    depends_on('mpi', when='+mpi')
    depends_on('zlib', when='+compression')

    def validate(self, spec):
        # NOTE : Scotch v6.0.0 and older have separate tar files for their esmumps-
        # compatible versions.  In any normal circumstance, it would be better just
        # to use these tar files since they're more comprehensive, but they
        # unfortunately have very strange URLs that are non-uniform.  For the time
        # being, I'm going to just use the '~esmumps' URLs that are uniform for
        # the sake of simplicity.
        if spec.satisfies('@:6.0.0') and '+esmumps' in spec:
            raise RuntimeError('The "+esmumps" variant is only supported for Scotch v6.0.1+.')

    def patch(self):
        makefile_inc = []
        cflags = [
            '-O3',
            '-DCOMMON_RANDOM_FIXED_SEED',
            '-DSCOTCH_DETERMINISTIC',
            '-DSCOTCH_RENAME',
            '-DIDXSIZE64'
            ]

        ## Library Build Type ##

        if '+shared' in self.spec:
            makefile_inc.extend([
                'LIB       = .so',
                'CLIBFLAGS = -shared -fPIC',
                'RANLIB    = echo',
                'AR	       = $(CC)',
                'ARFLAGS   = -shared $(LDFLAGS) -o'
                ])
            cflags.append('-fPIC')
        else:
            makefile_inc.extend([
                'LIB       = .a',
                'CLIBFLAGS = ',
                'RANLIB    = ranlib',
                'AR	       = ar',
                'ARFLAGS   = -ruv '
                ])

        ## Compiler-Specific Options ##

        if self.compiler.name == 'gcc':
            cflags.append('-Drestrict=__restrict')
        elif self.compiler.name == 'intel':
            cflags.append('-restrict')

        makefile_inc.append('CCS       = $(CC)')
        makefile_inc.append('CCP       = %s' %
            (os.path.join(self.spec['mpi'].prefix.bin, 'mpicc') if '+mpi' in self.spec else 'mpicc'))
        makefile_inc.append('CCD       = $(CCS)')

        ## Extra Features ##

        ldflags = []

        if '+compression' in self.spec:
            cflags.append('-DCOMMON_FILE_COMPRESS_GZ')
            ldflags.append('-L%s -lz' % (self.spec['zlib'].prefix.lib))

        cflags.append('-DCOMMON_PTHREAD')
        ldflags.append('-lm -lrt -pthread')

        makefile_inc.append('LDFLAGS   = %s' % ' '.join(ldflags))

        ## General Features ##

        makefile_inc.extend([
            'EXE       =',
            'OBJ       = .o',
            'MAKE      = make',
            'CAT       = cat',
            'LN        = ln',
            'MKDIR     = mkdir',
            'MV        = mv',
            'CP        = cp',
            'CFLAGS    = %s' % ' '.join(cflags),
            'LEX       = %s -Pscotchyy -olex.yy.c' % os.path.join(self.spec['flex'].prefix.bin , 'flex'),
            'YACC      = %s -pscotchyy -y -b y' %    os.path.join(self.spec['bison'].prefix.bin, 'bison'),
            'prefix    = %s' % self.prefix
            ])

        with working_dir('src'):
            with open('Makefile.inc', 'w') as fh:
                fh.write('\n'.join(makefile_inc))

    def install(self, spec, prefix):
        self.validate(spec)

        targets = ['scotch']
        if '+mpi' in self.spec:
            targets.append('ptscotch')

        if '+esmumps' in self.spec:
            targets.append('esmumps')
            if '+mpi' in self.spec:
                targets.append('ptesmumps')

        with working_dir('src'):
            for target in targets:
                make(target, parallel=(target!='ptesmumps'))

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('man/man1', prefix.share_man1)
