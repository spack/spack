from spack import *

class Gasnet(Package):
    """GASNet is a language-independent, low-level networking layer
       that provides network-independent, high-performance communication
       primitives tailored for implementing parallel global address space
       SPMD languages and libraries such as UPC, Co-Array Fortran, SHMEM,
       Cray Chapel, and Titanium.
    """
    homepage = "http://gasnet.lbl.gov"
    url      = "http://gasnet.lbl.gov/GASNet-1.24.0.tar.gz"

    version('1.24.0', 'c8afdf48381e8b5a7340bdb32ca0f41a')


    def install(self, spec, prefix):
        # TODO: don't use paths with @ in them.
        change_sed_delimiter('@', ';', 'configure')

        configure("--prefix=%s" % prefix,
                  # TODO: factor IB suport out into architecture description.
                  "--enable-ibv",
                  "--enable-udp",
                  "--disable-mpi",
                  "--enable-par",
                  "--enable-mpi-compat",
                  "--enable-segment-fast",
                  "--disable-aligned-segments",
                  # TODO: make an option so that Legion can request builds with/without this.
                  # See the Legion webpage for details on when to/not to use.
                  "--disable-pshm",
                  "--with-segment-mmap-max=64MB")

        make()
        make("install")
