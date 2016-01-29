from spack import *
import os

class Hpx(Package):
    """The HPX-5 Runtime System. HPX-5 (High Performance ParalleX) is an
    open source, portable, performance-oriented runtime developed at
    CREST (Indiana University). HPX-5 provides a distributed
    programming model allowing programs to run unmodified on systems
    from a single SMP to large clusters and supercomputers with
    thousands of nodes. HPX-5 supports a wide variety of Intel and ARM
    platforms. It is being used by a broad range of scientific
    applications enabling scientists to write code that performs and
    scales better than contemporary runtimes."""
    homepage = "http://hpx.crest.iu.edu"
    url      = "http://hpx.crest.iu.edu/release/hpx-2.0.0.tar.gz"

    version('2.0.0', '3d2ff3aab6c46481f9ec65c5b2bfe7a6')
    version('1.3.0', '2260ecc7f850e71a4d365a43017d8cee')
    version('1.2.0', '4972005f85566af4afe8b71afbf1480f')
    version('1.1.0', '646afb460ecb7e0eea713a634933ce4f')
    version('1.0.0', '8020822adf6090bd59ed7fe465f6c6cb')

    def install(self, spec, prefix):
        os.chdir("./hpx/")
        configure('--prefix=%s' % prefix)
        make()
        make("install")
