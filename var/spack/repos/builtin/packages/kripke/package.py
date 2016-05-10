from spack import *

class Kripke(Package):
    """Kripke is a simple, scalable, 3D Sn deterministic particle
       transport proxy/mini app.
    """
    homepage = "https://codesign.llnl.gov/kripke.php"
    url      = "https://codesign.llnl.gov/downloads/kripke-openmp-1.1.tar.gz"

    version('1.1', '7fe6f2b26ed983a6ce5495ab701f85bf')

    variant('mpi',    default=True, description='Build with MPI.')
    variant('openmp', default=True, description='Build with OpenMP enabled.')

    depends_on('mpi', when="+mpi")

    def install(self, spec, prefix):
        with working_dir('build', create=True):
            def enabled(variant):
                return (1 if variant in spec else 0)

            cmake('-DCMAKE_INSTALL_PREFIX:PATH=.',
                  '-DENABLE_OPENMP=%d' % enabled('+openmp'),
                  '-DENABLE_MPI=%d' % enabled('+mpi'),
                  '..',
                  *std_cmake_args)
            make()

            # Kripke does not provide install target, so we have to copy
            # things into place.
            mkdirp(prefix.bin)
            install('kripke', prefix.bin)
