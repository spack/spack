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
    url = "http://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-1.10.1.tar.bz2"
    list_url = "http://www.open-mpi.org/software/ompi/"
    list_depth = 3

    version('1.10.2', 'b2f43d9635d2d52826e5ef9feb97fd4c')
    version('1.10.1', 'f0fcd77ed345b7eafb431968124ba16e')
    version('1.10.0', '280cf952de68369cebaca886c5ce0304')
    version('1.8.8', '0dab8e602372da1425e9242ae37faf8c')
    version('1.6.5', '03aed2a4aa4d0b27196962a2a65fc475')

    patch('ad_lustre_rwcontig_open_source.patch', when="@1.6.5")
    patch('llnl-platforms.patch', when="@1.6.5")
    patch('configure.patch', when="@1.10.0:1.10.1")

    variant('psm', default=False, description='Build support for the PSM library.')
    variant('psm2', default=False, description='Build support for the Intel PSM2 library.')
    variant('verbs', default=False, description='Build support for OpenFabrics verbs.')
    variant('mxm', default=False, description='Build Mellanox Messaging support')

    variant('thread_multiple', default=False, description='Enable MPI_THREAD_MULTIPLE support')

    # TODO : variant support for alps, loadleveler  is missing
    variant('tm', default=False, description='Build TM (Torque, PBSPro, and compatible) support')
    variant('slurm', default=False, description='Build SLURM scheduler component')

    variant('pmi', default=False, description='Build PMI support, optionally adding DIR to the search path')
    variant('sqlite3', default=False, description='Build sqlite3 support')

    # TODO : support for CUDA is missing

    provides('mpi@:2.2', when='@1.6.5')
    provides('mpi@:3.0', when='@1.7.5:')

    depends_on('hwloc')

    def url_for_version(self, version):
        return "http://www.open-mpi.org/software/ompi/v%s/downloads/openmpi-%s.tar.bz2" % (version.up_to(2), version)


    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)

    @property
    def verbs(self):
        # Up through version 1.6, this option was previously named --with-openib
        if self.spec.satisfies('@:1.6'):
            return 'openib'
        # In version 1.7, it was renamed to be --with-verbs
        elif self.spec.satisfies('@1.7:'):
            return 'verbs'

    def install(self, spec, prefix):
        config_args = ["--prefix=%s" % prefix,
                       "--with-hwloc=%s" % spec['hwloc'].prefix,
                       "--enable-shared",
                       "--enable-static"]
        # Variant based arguments
        config_args.extend([
            # Schedulers
            '--with-tm' if '+tm' in spec else '--without-tm',
            '--with-slurm' if '+slurm' in spec else '--without-slurm',
            # Fabrics
            '--with-psm' if '+psm' in spec else '--without-psm',
            '--with-psm2' if '+psm2' in spec else '--without-psm2',
            ('--with-%s' % self.verbs) if '+verbs' in spec else ('--without-%s' % self.verbs),
            '--with-mxm' if '+mxm' in spec else '--without-mxm',
            # Other options
            '--enable-mpi-thread-multiple' if '+thread_multiple' in spec else '--disable-mpi-thread-multiple',
            '--with-pmi' if '+pmi' in spec else '--without-pmi',
            '--with-sqlite3' if '+sqlite3' in spec else '--without-sqlite3'
        ])

        # TODO: use variants for this, e.g. +lanl, +llnl, etc.
        # use this for LANL builds, but for LLNL builds, we need:
        #     "--with-platform=contrib/platform/llnl/optimized"
        if self.version == ver("1.6.5") and '+lanl' in spec:
            config_args.append("--with-platform=contrib/platform/lanl/tlcc2/optimized-nopanasas")

        if not self.compiler.f77 and not self.compiler.fc:
            config_args.append("--enable-mpi-fortran=no")

        configure(*config_args)
        make()
        make("install")

        self.filter_compilers()

    def filter_compilers(self):
        """Run after install to make the MPI compilers use the
           compilers that Spack built the package with.

           If this isn't done, they'll have CC, CXX and FC set
           to Spack's generic cc, c++ and f90.  We want them to
           be bound to whatever compiler they were built with.
        """
        kwargs = {'ignore_absent': True, 'backup': False, 'string': False}
        dir = os.path.join(self.prefix, 'share/openmpi/')

        cc_wrappers = ['mpicc-vt-wrapper-data.txt', 'mpicc-wrapper-data.txt',
                       'ortecc-wrapper-data.txt', 'shmemcc-wrapper-data.txt']

        cxx_wrappers = ['mpic++-vt-wrapper-data.txt', 'mpic++-wrapper-data.txt',
                        'ortec++-wrapper-data.txt']

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

        # These are symlinks in newer versions, so check that here
        f77_wrappers = ['mpif77-vt-wrapper-data.txt', 'mpif77-wrapper-data.txt']
        f90_wrappers = ['mpif90-vt-wrapper-data.txt', 'mpif90-wrapper-data.txt']

        for wrapper in f77_wrappers:
            path = os.path.join(dir, wrapper)
            if not os.path.islink(path):
                filter_file('compiler=.*', 'compiler=%s' % self.compiler.f77,
                            path, **kwargs)
        for wrapper in f90_wrappers:
            path = os.path.join(dir, wrapper)
            if not os.path.islink(path):
                filter_file('compiler=.*', 'compiler=%s' % self.compiler.fc,
                            path, **kwargs)
