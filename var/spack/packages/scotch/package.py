from spack import *
import os

class Scotch(Package):
    """Scotch is a software package for graph and mesh/hypergraph
       partitioning, graph clustering, and sparse matrix ordering."""
    homepage = "http://www.labri.fr/perso/pelegrin/scotch/"
    url      = "http://gforge.inria.fr/frs/download.php/file/34099/scotch_6.0.3.tar.gz"
    list_url = "http://gforge.inria.fr/frs/?group_id=248"

    version('6.0.3', '10b0cc0f184de2de99859eafaca83cfc')

    variant('mpi', default=False, description='Activate the compilation of PT-Scotch')
    variant('compression', default=True, description='Activate the posibility to use compressed files')
    variant('esmumps', default=False, description='Activate the compilation of the lib esmumps needed by mumps')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('mpi', when='+mpi')
    depends_on('zlib', when='+compression')
    depends_on('flex')
    depends_on('bison')

    def compiler_specifics(self, makefile_inc, defines):
        if self.compiler.name == 'gcc':
            defines.append('-Drestrict=__restrict')
        elif self.compiler.name == 'intel':
            defines.append('-restrict')

        makefile_inc.append('CCS       = $(CC)')

        if '+mpi' in self.spec:
            makefile_inc.extend([
                    'CCP       = %s' % os.path.join(self.spec['mpi'].prefix.bin, 'mpicc'),
                    'CCD       = $(CCP)'
                    ])
        else:
            makefile_inc.extend([
                    'CCP       = mpicc', # It is set but not used
                    'CCD       = $(CCS)'
                    ])



    def library_build_type(self, makefile_inc, defines):
        makefile_inc.extend([
            'LIB       = .a',
            'CLIBFLAGS = ',
            'RANLIB    = ranlib',
            'AR	       = ar',
            'ARFLAGS   = -ruv '
            ])

    @when('+shared')
    def library_build_type(self, makefile_inc, defines):
        makefile_inc.extend([
            'LIB       = .so',
            'CLIBFLAGS = -shared -fPIC',
            'RANLIB    = echo',
            'AR	       = $(CC)',
            'ARFLAGS   = -shared $(LDFLAGS) -o'
            ])

    def extra_features(self, makefile_inc, defines):
        ldflags = []
        
        if '+compression' in self.spec:
            defines.append('-DCOMMON_FILE_COMPRESS_GZ')
            ldflags.append('-L%s -lz' % (self.spec['zlib'].prefix.lib))

        defines.append('-DCOMMON_PTHREAD')
        ldflags.append('-lm -lrt -pthread')
           
        makefile_inc.append('LDFLAGS   = %s' % ' '.join(ldflags))

            
    def write_make_inc(self):
        makefile_inc = []
        defines = [ 
            '-DCOMMON_RANDOM_FIXED_SEED',
            '-DSCOTCH_DETERMINISTIC',
            '-DSCOTCH_RENAME',
            '-DIDXSIZE64' ]

        self.library_build_type(makefile_inc, defines)
        self.compiler_specifics(makefile_inc, defines)
        self.extra_features(makefile_inc, defines)

        makefile_inc.extend([
            'EXE       =',
            'OBJ       = .o',
            'MAKE      = make',
            'CAT       = cat',
            'LN        = ln',
            'MKDIR     = mkdir',
            'MV        = mv',
            'CP        = cp',
            'CFLAGS    = -O3 %s' % (' '.join(defines)),
            'LEX       = %s -Pscotchyy -olex.yy.c' % os.path.join(self.spec['flex'].prefix.bin , 'flex'),
            'YACC      = %s -pscotchyy -y -b y' %    os.path.join(self.spec['bison'].prefix.bin, 'bison'),
            'prefix    = %s' % self.prefix,
            ''
            ])

        with open('Makefile.inc', 'w') as fh:
            fh.write('\n'.join(makefile_inc))

    def patch(self):
        with working_dir('src'):
            self.write_make_inc()
            
    def install(self, spec, prefix):
        targets = ['scotch']
        if '+mpi' in self.spec:
            targets.append('ptscotch')

        if '+esmumps' in self.spec:
            targets.append('esmumps')
            if '+mpi' in self.spec:
                targets.append('ptesmumps')

        with working_dir('src'):
            for app in targets:
                make(app, parallel=(not app=='ptesmumps'))

        
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('man/man1', prefix.share_man1)

