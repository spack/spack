from spack import *
import os

class Hwloc(Package):
    """The Portable Hardware Locality (hwloc) software package
       provides a portable abstraction (across OS, versions,
       architectures, ...) of the hierarchical topology of modern
       architectures, including NUMA memory nodes, sockets, shared
       caches, cores and simultaneous multithreading. It also gathers
       various system attributes such as cache and memory information
       as well as the locality of I/O devices such as network
       interfaces, InfiniBand HCAs or GPUs. It primarily aims at
       helping applications with gathering information about modern
       computing hardware so as to exploit it accordingly and
       efficiently."""
    homepage = "http://www.open-mpi.org/projects/hwloc/"
    url      = "http://www.open-mpi.org/software/hwloc/v1.9/downloads/hwloc-1.9.tar.gz"

    # Install from sources
    if os.environ.has_key("MORSE_HWLOC_TAR") and os.environ.has_key("MORSE_HWLOC_TAR_MD5"):
        version('local', '%s' % os.environ['MORSE_HWLOC_TAR_MD5'],
                url = "file://%s" % os.environ['MORSE_HWLOC_TAR'])
    else:
        version('1.9', '1f9f9155682fe8946a97c08896109508')
        version('1.10.1', '27f2966df120a74df19dc244d5340107', url='http://www.open-mpi.org/software/hwloc/v1.10/downloads/hwloc-1.10.1.tar.gz')
        version('1.11.0', '150a6a0b7a136bae5443e9c2cf8f316c', url='http://www.open-mpi.org/software/hwloc/v1.11/downloads/hwloc-1.11.0.tar.gz')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
