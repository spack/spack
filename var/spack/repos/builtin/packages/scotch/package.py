from spack import *
import os, re

class Scotch(Package):
    """Scotch is a software package for graph and mesh/hypergraph
       partitioning, graph clustering, and sparse matrix ordering."""

    homepage = "http://www.labri.fr/perso/pelegrin/scotch/"
    url      = "http://gforge.inria.fr/frs/download.php/latestfile/298/scotch_6.0.3.tar.gz"
    base_url = "http://gforge.inria.fr/frs/download.php/latestfile/298"
    list_url = "http://gforge.inria.fr/frs/?group_id=248"

    version('6.0.3', '10b0cc0f184de2de99859eafaca83cfc')
    version('6.0.0', 'c50d6187462ba801f9a82133ee666e8e')
    version('5.1.10b', 'f587201d6cf5cf63527182fbfba70753')

    variant('mpi', default=False, description='Activate the compilation of PT-Scotch')
    variant('compression', default=True, description='Activate the posibility to use compressed files')
    variant('esmumps', default=False, description='Activate the compilation of the lib esmumps needed by mumps')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('flex')
    depends_on('bison')
    depends_on('mpi', when='+mpi')
    depends_on('zlib', when='+compression')

    # NOTE: Versions of Scotch up to version 6.0.0 don't include support for
    # building with 'esmumps' in their default packages.  In order to enable
    # support for this feature, we must grab the 'esmumps' enabled archives
    # from the Scotch hosting site.  These alternative archives include a strict
    # superset of the behavior in their default counterparts, so we choose to
    # always grab these versions for older Scotch versions for simplicity.
    @when('@:6.0.0')
    def url_for_version(self, version):
        return '%s/scotch_%s_esmumps.tar.gz' % (Scotch.base_url, version)

    @when('@6.0.1:')
    def url_for_version(self, version):
        return super(Scotch, self).url_for_version(version)

    # NOTE: Several of the 'esmumps' enabled Scotch releases up to version 6.0.0
    # have broken build scripts that don't properly build 'esmumps' as a separate
    # target, so we need a patch procedure to remove 'esmumps' from existing targets
    # and to add it as a standalone target.
    @when('@:6.0.0')
    def patch(self):
        makefile_path = os.path.join('src', 'Makefile')
        with open(makefile_path, 'r') as makefile:
            esmumps_enabled = any(re.search(r'^esmumps(\s*):(.*)$', line) for line in makefile.readlines())

        if not esmumps_enabled:
            mff = FileFilter(makefile_path)
            mff.filter(r'^.*((esmumps)|(ptesmumps)).*(install).*$', '')

            makefile_esmumps_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Makefile.esmumps')
            with open(makefile_path, 'a') as makefile:
                makefile.write('\ninclude %s\n' % makefile_esmumps_path)

    @when('@6.0.1:')
    def patch(self):
        pass

    # NOTE: Configuration of Scotch is achieved by writing a 'Makefile.inc' file
    # that contains all of the configuration variables and their desired values
    # for the installation.  This function writes this file based on the given
    # installation variants.
    def configure(self):
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
            (self.spec['mpi'].mpicc if '+mpi' in self.spec else 'mpicc'))
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
        self.configure()

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
