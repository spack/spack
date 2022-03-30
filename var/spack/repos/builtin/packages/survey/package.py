# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Survey(CMakePackage):
    """Survey is a high level performance tool product from Trenza, Inc.
       The survey collector/analytics framework is a new generation,
       high level, lightweight multiplatform Linux tool set that
       targets metric collection for high level performance analysis
       of applications running on both single node and on large scale
       platforms, including the Cray platforms.

       The collector is designed to work on sequential, MPI, OpenMP,
       and hybrid codes and directly leverages several interfaces
       available for tools inside current MPI implementations including:
       MPICH, MVAPICH, MPT, and OpenMPI. It also supports multiple
       architectures and has been tested on machines based on Intel,
       AMD, ARM, and IBM P8/9 processors and integrated GPUs.

       Survey is a licensed product with the source not openly available.
       To access the survey source and build with spack please contact:
       Trenza Inc. via: dmont@trenzasynergy.com or
                        jeg@trenzasynergy.com
    """

    homepage = "http://www.trenzasynergy.com"
    git      = "ssh://git@gitlab.com/trenza/survey.git"

    maintainers = ['jgalarowicz']

    version('master', branch='master')
    version('1.0.3', tag='1.0.3')
    version('1.0.2', tag='1.0.2')
    version('1.0.1.1', tag='1.0.1.1')
    version('1.0.1', tag='1.0.1')
    version('1.0.0', branch='1.0.0')

    variant('mpi', default=False,
            description="Enable mpi, build MPI data collector")

    variant('tls_model', default='implicit',
            description='The TLS model to build with',
            values=('implicit', 'explicit'))

    # must have cmake at 3.12 or greater to find python3
    depends_on('cmake@3.12:', type='build')

    # for collectors
    depends_on("libmonitor@2021.04.27+commrank", type=('build', 'link', 'run'), when='@:1.0.2')
    depends_on('libmonitor@2021.11.08+commrank', type=('build', 'link', 'run'), when='@1.0.3:')

    depends_on("papi@5:", type=('build', 'link', 'run'))
    depends_on("gotcha@master", type=('build', 'link', 'run'))
    depends_on("llvm-openmp@9.0.0", type=('build', 'link', 'run'), when='@:1.0.2')
    depends_on('llvm-openmp@12.0.1', type=('build', 'link', 'run'), when='@1.0.3:')

    # MPI Installation
    depends_on("mpi", when="+mpi")

    depends_on("python@3:", type=('build', 'link', 'run'))
    depends_on("py-setuptools", type='build')
    depends_on("py-pip", type='build')
    depends_on("py-pandas", type=('build', 'run'))
    depends_on("py-psutil", type=('build', 'run'))
    depends_on("py-sqlalchemy", type=('build', 'run'))
    depends_on("py-pyyaml", type=('build', 'run'))

    extends('python')

    parallel = False

    def get_mpi_cmake_options(self, spec):
        # Returns MPI cmake_options that will enable the appropriate
        # MPI implementation is specified as a cmake argument.
        mpi_args = ['-D%s_DIR=%s' % (spec['mpi'].name.upper(), spec['mpi'].prefix)]
        return mpi_args

    def cmake_args(self):
        spec = self.spec

        if 'tls_model=implicit' in spec:
            spack_tls_model = "implicit"
        else:
            spack_tls_model = "explicit"

        # Add in paths for finding package config files that tell us
        # where to find these packages
        cmake_args = [
            '-DCMAKE_VERBOSE_MAKEFILE=ON',
            '-DTLS_MODEL=%s' % spack_tls_model,
            '-DLIBMONITOR_DIR=%s' % spec['libmonitor'].prefix,
            '-DPAPI_DIR=%s' % spec['papi'].prefix,
            '-DLIBIOMP_DIR=%s' % spec['llvm-openmp'].prefix,
            '-DPYTHON_DIR=%s' % spec['python'].prefix,
            '-DGOTCHA_DIR=%s' % spec['gotcha'].prefix
        ]

        # Add any MPI implementations coming from variant settings
        mpi_options = self.get_mpi_cmake_options(spec)
        cmake_args.extend(mpi_options)
        return cmake_args

    def setup_run_environment(self, env):
        """Set up the compile and runtime environments for a package."""

        # Set SURVEY_MPI_IMPLEMENTATON to the appropriate mpi implementation
        # This is needed by survey to deploy the correct mpi runtimes.
        env.set('SURVEY_MPI_IMPLEMENTATION', self.spec['mpi'].name.lower())
        # For compatibility reasons we need
        env.prepend_path('PATH', self.spec['python'].prefix.bin)
