from spack import *

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
    list_url = "http://www.open-mpi.org/software/hwloc/"
    list_depth = 3

    version('1.11.3', 'c1d36a9de6028eac1d18ea4782ef958f')
    version('1.11.2', 'e4ca55c2a5c5656da4a4e37c8fc51b23')
    version('1.11.1', 'feb4e416a1b25963ed565d8b42252fdc')
    version('1.9',    '1f9f9155682fe8946a97c08896109508')

    depends_on('libpciaccess')

    def url_for_version(self, version):
        return "http://www.open-mpi.org/software/hwloc/v%s/downloads/hwloc-%s.tar.gz" % (version.up_to(2), version)

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
