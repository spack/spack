from spack import *

class Ravel(Package):
    """Ravel is a parallel communication trace visualization tool that
       orders events according to logical time."""

    homepage = "https://github.com/scalability-llnl/ravel"
    url = 'https://github.com/scalability-llnl/ravel/archive/v1.0.0.tar.gz'

    version('1.0.0', 'b25fece58331c2adfcce76c5036485c2')

    # TODO: make this a build dependency
    depends_on('cmake@2.8.9:')

    depends_on('muster@1.0.1:')
    depends_on('otf')
    depends_on('otf2')
    depends_on('qt@5:')

    def install(self, spec, prefix):
        cmake('-Wno-dev', *std_cmake_args)
        make()
        make("install")
