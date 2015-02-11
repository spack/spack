from spack import *

class Ravel(Package):
    """Ravel is a parallel communication trace visualization tool that
       orders events according to logical time."""

    homepage = "https://github.com/scalability-llnl/ravel"


    version('1.0', git="ssh://git@cz-stash.llnl.gov:7999/pave/ravel.git",
            branch='features/otf2export')

    depends_on('cmake@2.8.9:')

    depends_on('muster@1.0.1:')
    depends_on('otf')
    depends_on('otf2')
    depends_on('qt@5:')

    def install(self, spec, prefix):
        cmake(*std_cmake_args)
        make()
        make("install")
