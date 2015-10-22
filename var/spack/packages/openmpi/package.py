import os

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

    version('1.8.2', 'ab538ed8e328079d566fc797792e016e',
            url='http://www.open-mpi.org/software/ompi/v1.8/downloads/openmpi-1.8.2.tar.gz')
    version('1.6.5', '03aed2a4aa4d0b27196962a2a65fc475',
            url = "http://www.open-mpi.org/software/ompi/v1.6/downloads/openmpi-1.6.5.tar.bz2")

    patch('ad_lustre_rwcontig_open_source.patch', when="@1.6.5")
    patch('llnl-platforms.patch', when="@1.6.5")

    provides('mpi@:2')


    def setup_dependent_environment(self, module, spec, dep_spec):
        """For dependencies, make mpicc's use spack wrapper."""
        os.environ['OMPI_CC']  = 'cc'
        os.environ['OMPI_CXX'] = 'c++'
        os.environ['OMPI_FC'] = 'f90'


    def install(self, spec, prefix):
        config_args = ["--prefix=%s" % prefix]

        # TODO: use variants for this, e.g. +lanl, +llnl, etc.
        # use this for LANL builds, but for LLNL builds, we need:
        #     "--with-platform=contrib/platform/llnl/optimized"
        if self.version == ver("1.6.5") and '+lanl' in spec:
            config_args.append("--with-platform=contrib/platform/lanl/tlcc2/optimized-nopanasas")

        # TODO: Spack should make it so that you can't actually find
        # these compilers if they're "disabled" for the current
        # compiler configuration.
        if not self.compiler.f77 and not self.compiler.fc:
            config_args.append("--enable-mpi-fortran=no")

        configure(*config_args)
        make()
        make("install")

        self.filter_compilers()


    def filter_compilers(self):
        """Run after install to make the MPI compilers use the
           compilers that Spack built the package with.

           If this isn't done, they'll have CC, CXX, F77, and FC set
           to Spack's generic cc, c++, f77, and f90.  We want them to
           be bound to whatever compiler they were built with.
        """
        kwargs = { 'ignore_absent' : True, 'backup' : False, 'string' : False }
        dir = os.path.join(self.prefix, 'share/openmpi/')

        cc_wrappers = ['mpicc-vt-wrapper-data.txt', 'mpicc-wrapper-data.txt',
                       'ortecc-wrapper-data.txt', 'shmemcc-wrapper-data.txt']

        cxx_wrappers = ['mpic++-vt-wrapper-data.txt', 'mpic++-wrapper-data.txt']

        fc_wrappers = ['mpifort-vt-wrapper-data.txt',
                       'mpifort-wrapper-data.txt', 'shmemfort-wrapper-data.txt']

        for wrapper in cc_wrappers:
            filter_file('compiler=.*', 'compiler=%s' % self.compiler.cc,
                        os.path.join(dir, wrapper), **kwargs)

        for wrapper in cxx_wrappers:
            filter_file('compiler=.*', 'compiler=%s' % self.compiler.cxx,
                        os.path.join(dir, wrapper), **kwargs)

        for wrapper in fc_wrappers:
            filter_file('compiler=.*', 'compiler=%s' % self.compiler.fc,
                        os.path.join(dir, wrapper), **kwargs)
