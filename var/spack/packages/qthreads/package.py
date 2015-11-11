from spack import *

class Qthreads(Package):
    """The qthreads API is designed to make using large numbers of
       threads convenient and easy, and to allow portable access to
       threading constructs used in massively parallel shared memory
       environments. The API maps well to both MTA-style threading and
       PIM-style threading, and we provide an implementation of this
       interface in both a standard SMP context as well as the SST
       context. The qthreads API provides access to full/empty-bit
       (FEB) semantics, where every word of memory can be marked
       either full or empty, and a thread can wait for any word to
       attain either state."""
    homepage = "http://www.cs.sandia.gov/qthreads/"
    url      = "https://qthreads.googlecode.com/files/qthread-1.10.tar.bz2"

    version('1.10', '5af8c8bbe88c2a6d45361643780d1671')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
