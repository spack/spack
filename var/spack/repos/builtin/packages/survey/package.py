# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Survey(CMakePackage):
    """Survey is a high-level performance tool product from Trenza, Inc.
       The survey collector/analytics framework is a new generation,
       high-level, light-weight multi-platform Linux tool set that
       targets metric collection for high-level performance analysis
       of applications running on both single node and on large-scale
       platforms, including the Cray platforms.

       The collector is designed to work on sequential, MPI, OpenMP,
       and hybrid codes and directly leverages several interfaces
       available for tools inside current MPI implementations including:
       MPICH, MVAPICH, MPT, and OpenMPI. It also supports multiple
       architectures and has been tested on machines based on Intel,
       AMD, ARM, and IBM P8/9 processors and integrated GPUs.
    """

    # To access the survey source and build with
    # spack please contact: Trenza Inc. via:
    # dmont@trenzasynergy.com
    homepage = "http://www.trenzasynergy.com"
    git      = "git@gitlab.com:trenza/survey.git"

    maintainers = ['jgalarowicz']

    version('develop', branch='master')
    version('1.0.0', branch='1.0.0')

    # MPI variants
    variant('openmpi', default=False,
            description="Build mpi collector for openmpi \
                         MPI when variant is enabled.")
    variant('mpt', default=False,
            description="Build mpi collector for SGI \
                         MPT MPI when variant is enabled.")
    variant('mvapich2', default=False,
            description="Build mpi collector for mvapich2\
                         MPI when variant is enabled.")
    variant('mvapich', default=False,
            description="Build mpi collector for mvapich\
                         MPI when variant is enabled.")
    variant('mpich2', default=False,
            description="Build mpi collector for mpich2\
                         MPI when variant is enabled.")
    variant('mpich', default=False,
            description="Build mpi collector for mpich\
                         MPI when variant is enabled.")
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    # must have cmake at 3.12 or greater to find python3
    depends_on('cmake@3.12:')

    # for collectors
    depends_on("libmonitor@2021.04.27+commrank", type=('build', 'link', 'run'))

    depends_on("papi@5:", type=('build', 'link', 'run'))
    depends_on("gotcha@master", type=('build', 'link', 'run'))
    depends_on("llvm-openmp@9.0.0", type=('build', 'link', 'run'))

    # MPI Installations
    depends_on("openmpi", when='+openmpi')
    depends_on("mpich@:", when='+mpich')
    depends_on("mpich@2:", when='+mpich2')
    depends_on("mvapich2@2:", when='+mvapich2')
    depends_on("mvapich2@:1", when='+mvapich')
    depends_on("mpt", when='+mpt')

    depends_on("python@3:", type=('build', 'link', 'run'))
    depends_on("py-setuptools", type=('build', 'link', 'run'))
    depends_on("py-pip", type=('build', 'link', 'run'))
    depends_on("py-python-dateutil", type=('build', 'link', 'run'))
    depends_on("py-pandas", type=('build', 'link', 'run'))
    depends_on("py-psutil", type=('build', 'link', 'run'))
    depends_on("py-sqlalchemy", type=('build', 'link', 'run'))
    depends_on("py-pbr", type=('build', 'link', 'run'))

    extends('python')

    parallel = False

    def set_mpi_cmake_options(self, spec, cmake_options):
        # Appends to cmake_options the options that will enable the appropriate
        # MPI implementations

        mpi_options = []

        # openmpi
        if spec.satisfies('+openmpi'):
            mpi_options.append('-DOPENMPI_DIR=%s' % spec['openmpi'].prefix)
        # mpich
        if spec.satisfies('+mpich'):
            mpi_options.append('-DMPICH_DIR=%s' % spec['mpich'].prefix)
        # mpich2
        if spec.satisfies('+mpich2'):
            mpi_options.append('-DMPICH2_DIR=%s' % spec['mpich2'].prefix)
        # mvapich
        if spec.satisfies('+mvapich'):
            mpi_options.append('-DMVAPICH_DIR=%s' % spec['mvapich'].prefix)
        # mvapich2
        if spec.satisfies('+mvapich2'):
            mpi_options.append('-DMVAPICH2_DIR=%s' % spec['mvapich2'].prefix)
        # mpt
        if spec.satisfies('+mpt'):
            mpi_options.append('-DMPT_DIR=%s' % spec['mpt'].prefix)

        cmake_options.extend(mpi_options)

    def cmake_args(self):
        spec = self.spec

        # Add in paths for finding package config files that tell us
        # where to find these packages
        cmake_args = [
            '-DCMAKE_VERBOSE_MAKEFILE=ON',
            '-DTLS_MODEL=implicit',
            '-DLIBMONITOR_DIR=%s' % spec['libmonitor'].prefix,
            '-DPAPI_DIR=%s' % spec['papi'].prefix,
            '-DLIBIOMP_DIR=%s' % spec['llvm-openmp'].prefix,
            '-DPYTHON_DIR=%s' % spec['python'].prefix,
            '-DGOTCHA_DIR=%s' % spec['gotcha'].prefix
        ]

        # Add any MPI implementations coming from variant settings
        self.set_mpi_cmake_options(spec, cmake_args)
        return cmake_args

    @property
    def python_lib_dir(self):
        python_vers_phrase = 'python{0}'.format(
                             self.spec['python'].version.up_to(2))
        return join_path('lib', python_vers_phrase)

    @property
    def site_packages_dir(self):
        return join_path(self.python_lib_dir, 'site-packages')

    def setup_run_environment(self, env):
        """Set up the compile and runtime environments for a package."""

        # Set SURVEY_MPI_IMPLEMENTATON to the appropriate mpi implementation
        # This is needed by survey to deploy the correct
        # mpi runtimes.
        # Users may have to set the SURVEY_MPI_IMPLEMENTATION variable
        # manually or create separate module files, if multiple mpi's
        # are specified in the build
        if self.spec.satisfies('+mpich'):
            env.set('SURVEY_MPI_IMPLEMENTATION', "mpich")

        if self.spec.satisfies('+mvapich'):
            env.set('SURVEY_MPI_IMPLEMENTATION', "mvapich")

        if self.spec.satisfies('+mvapich2'):
            env.set('SURVEY_MPI_IMPLEMENTATION', "mvapich2")

        if self.spec.satisfies('+mpt'):
            env.set('SURVEY_MPI_IMPLEMENTATION', "mpt")

        if self.spec.satisfies('+openmpi'):
            env.set('SURVEY_MPI_IMPLEMENTATION', "openmpi")

        env.prepend_path('MANPATH', self.spec.prefix.share.man)

        env.prepend_path('PATH', self.spec['python'].prefix.bin)
        env.prepend_path('PYTHONPATH',
                         join_path(self.prefix, self.site_packages_dir))
        # These are external packages whose site-packages directories are needed
        # in order to load survey with one module load command.  If these statements
        # are not present.  The corresponding module files will need to be loaded
        # These are explicit depends_on packages
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['python'].prefix, self.site_packages_dir))
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-pandas'].prefix,
                                   self.site_packages_dir))
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-python-dateutil'].prefix,
                                   self.site_packages_dir))
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-setuptools'].prefix,
                                   self.site_packages_dir))
        # These are not-explicit depends_on packages
        # but they must be known in the spec for survey, so it works.
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-numpy'].prefix,
                                   self.site_packages_dir))
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-pytz'].prefix,
                                   self.site_packages_dir))
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-six'].prefix,
                                   self.site_packages_dir))
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-psutil'].prefix,
                                   self.site_packages_dir))
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-sqlalchemy'].prefix,
                                   self.site_packages_dir))
        env.prepend_path('PYTHONPATH',
                         join_path(self.spec['py-pbr'].prefix,
                                   self.site_packages_dir))
