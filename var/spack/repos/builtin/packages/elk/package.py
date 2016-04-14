from spack import *
import spack

class Elk(Package):
    '''An all-electron full-potential linearised augmented-plane wave
    (FP-LAPW) code with many advanced features.'''

    homepage = 'http://elk.sourceforge.net/'
    url      = 'https://sourceforge.net/projects/elk/files/elk-3.3.17.tgz'

    version('3.3.17', 'f57f6230d14f3b3b558e5c71f62f0592')

    # Elk provides these libraries, but allows you to specify your own
    variant('blas',   default=True, description='Build with custom BLAS library')
    variant('lapack', default=True, description='Build with custom LAPACK library')
    variant('fft',    default=True, description='Build with custom FFT library')

    # Elk does not provide these libraries, but allows you to use them
    variant('mpi',    default=True, description='Enable MPI parallelism')
    variant('openmp', default=True, description='Enable OpenMP support')
    variant('libxc',  default=True, description='Link to Libxc functional library')

    depends_on('blas',   when='+blas')
    depends_on('lapack', when='+lapack')
    depends_on('fftw',   when='+fft')
    depends_on('mpi',    when='+mpi')
    depends_on('libxc',  when='+libxc')

    # Cannot be built in parallel
    parallel = False


    def configure(self, spec):
        # Dictionary of configuration options
        config = {
            'MAKE':      'make',
            'F90':       join_path(spack.build_env_path, 'f90'),
            'F77':       join_path(spack.build_env_path, 'f77'),
            'AR':        'ar',
            'LIB_FFT':   'fftlib.a',
            'SRC_MPI':   'mpi_stub.f90',
            'SRC_OMP':   'omp_stub.f90',
            'SRC_libxc': 'libxcifc_stub.f90',
            'SRC_FFT':   'zfftifc.f90'
        }

        # Compiler-specific flags
        flags = ''
        if   self.compiler.name == 'intel':
            flags = '-O3 -ip -unroll -no-prec-div -openmp'
        elif self.compiler.name == 'gcc':
            flags = '-O3 -ffast-math -funroll-loops -fopenmp'
        elif self.compiler.name == 'pgi':
            flags = '-O3 -mp -lpthread'
        elif self.compiler.name == 'g95':
            flags = '-O3 -fno-second-underscore'
        elif self.compiler.name == 'nag':
            flags = '-O4 -kind=byte -dusty -dcfuns'
        elif self.compiler.name == 'xl':
            flags = '-O3 -qsmp=omp'
        config['F90_OPTS'] = flags
        config['F77_OPTS'] = flags

        # BLAS/LAPACK support
        blas   = 'blas.a'
        lapack = 'lapack.a'
        if '+blas'   in spec:
            blas   = join_path(spec['blas'].prefix.lib,   'libblas.so')
        if '+lapack' in spec:
            lapack = join_path(spec['lapack'].prefix.lib, 'liblapack.so')
        config['LIB_LPK'] = ' '.join([lapack, blas]) # lapack must come before blas

        # FFT support
        if '+fft' in spec:
            config['LIB_FFT'] = join_path(spec['fftw'].prefix.lib, 'libfftw3.so')
            config['SRC_FFT'] = 'zfftifc_fftw.f90'

        # MPI support
        if '+mpi' in spec:
            config.pop('SRC_MPI')
            config['F90'] = join_path(spec['mpi'].prefix.bin, 'mpif90')
            config['F77'] = join_path(spec['mpi'].prefix.bin, 'mpif77')

        # OpenMP support
        if '+openmp' in spec:
            config.pop('SRC_OMP')

        # Libxc support
        if '+libxc' in spec:
            config['LIB_libxc'] = ' '.join([
                join_path(spec['libxc'].prefix.lib, 'libxcf90.so'),
                join_path(spec['libxc'].prefix.lib, 'libxc.so')
            ])
            config['SRC_libxc'] = ' '.join([
                'libxc_funcs.f90',
                'libxc.f90',
                'libxcifc.f90'
            ])

        # Write configuration options to include file
        with open('make.inc', 'w') as inc:
            for key in config:
                inc.write('{0} = {1}\n'.format(key, config[key]))


    def install(self, spec, prefix):
        # Elk only provides an interactive setup script
        self.configure(spec)

        make()
        make('test')

        # The Elk Makefile does not provide an install target
        mkdirp(prefix.bin)

        install('src/elk',                   prefix.bin)
        install('src/eos/eos',               prefix.bin)
        install('src/spacegroup/spacegroup', prefix.bin)

        install_tree('examples', join_path(prefix, 'examples'))
        install_tree('species',  join_path(prefix, 'species'))

