from spack import *

class Simgrid(Package):
    """To study the behavior of large-scale distributed systems such as Grids, Clouds, HPC or P2P systems."""
    homepage = "http://simgrid.gforge.inria.fr/index.html"
    url      = "http://gforge.inria.fr/frs/download.php/file/33686/SimGrid-3.11.1.tar.gz"

    version('3.11.1', 'eb15a815a609bc8784ed4d55baafe435')
    version('3.11', '358ed81042bd283348604eb1beb80224')
    version('3.10', 'a345ad07e37539d54390f817b7271de7')
    version('3.10', '2aca712d073fdd21a86dd2fcf1aabf12')

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)
        make()
        make("install")
