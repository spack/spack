from spack import *

class Openmpi(Package):
    """Open MPI is a project combining technologies and resources from
       several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI)
       in order to build the best MPI library available. A completely
       new MPI-2 compliant implementation, Open MPI offers advantages
       for system and software vendors, application developers and
       computer science researchers.
    """

    homepage = "http://www.open-mpi.org"
    url      = "http://www.open-mpi.org/software/ompi/v1.6/downloads/openmpi-1.6.5.tar.bz2"

    versions = { '1.6.5' : '03aed2a4aa4d0b27196962a2a65fc475', }

    provides('mpi@:2')

    patch('ad_lustre_rwcontig_open_source.patch')
    patch('llnl-platforms.patch')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-platform=contrib/platform/lanl/tlcc2/optimized-nopanasas")

        # TODO: implement variants next, so we can have LLNL and LANL options.
        # use above for LANL builds, but for LLNL builds, we need this
        #     "--with-platform=contrib/platform/llnl/optimized")

        make()
        make("install")
