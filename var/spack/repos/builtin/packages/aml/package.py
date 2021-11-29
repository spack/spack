# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Aml(AutotoolsPackage):
    """
    AML: Building Blocks for Memory Management.

    For information on AML please visit AML homepage.

    Possible variants for aml spack package are:
    - `+cuda`: enables library features implementation over cuda runtime library.
    All cuda variants from the spack package "cuda" are allowed.
    - `+hip`: enables library features implementation over hip runtime library.
    All variants from the spack package "hip" are allowed.
    - `+ze`: enables library features implementation over intel level_zero
    library. This feature relies on aml 'automagick' detection until a spack
    package becomes available.
    - `+hwloc`: enables library features implementation over hwloc library.
    If `+hwloc` variant is used, `hwloc@2.0:` is used as a dependency for
    building hwloc features.
    - `+opencl`: enables library features implementation over opencl library.
    If `+rocm` and `+opencl` are used together, `rocm-opencl` is used as a
    dependency for building opencl features.
    - `+all`: enables all above variants.
    - `openmp-targets={spir64,}`: Enable interoperability of pointers between
    intel OpenMP and intel level_zero for spir64 openmp targets.
    - `hip-platform={amd,nvidia}`: Compile aml with this hip backend
    implementation. Under the hood, hip calls either amd or cuda functions.

    Examples:
    ========

    - spack install aml +cuda +hwloc +hip +ze +opencl
    - spack install aml +cuda +hip hip-platform=nvidia
    - spack install aml +ze openmp-targets=spir64
    """

    homepage = "https://argo-aml.readthedocs.io/"

    maintainers = ['perarnau']

    test_requires_compiler = True

    tags = ['e4s']

    # Package sources
    ###################################

    url = 'https://github.com/anlsys/aml/releases/download/v0.2.0/aml-0.2.0.tar.gz'
    git = 'https://github.com/anlsys/aml.git'

    # version string is generated from git tags, requires entire repo
    version('master', branch='master', submodules=True, get_full_repo=True)

    version('0.2.0',
            sha256='2044a2f3f1d7a19827dd9c0726172b690189b4d3fe938656c4160c022468cc4a')
    version('0.1.0',
            sha256='cc89a8768693f1f11539378b21cdca9f0ce3fc5cb564f9b3e4154a051dcea69b',
            deprecated=True)

    # Generate possible variants.
    #############################

    for b in ['opencl', 'hwloc', 'ze', 'hip', 'cuda']:
        variant(b, default=False,
                description="Enable features relying on {} backend.".format(b))
    variant('openmp-targets', values=disjoint_sets(('spir64')),
            description="Intel OpenMP target architecture setting.")
    variant('hip-platform', values=disjoint_sets(('amd', 'nvidia')),
            description="Hip backend platform.")

    # Dependencies management
    #########################

    # aml always depends on libnuma
    depends_on('numactl')

    # - cuda dependency. We use the environment variable CUDA_HOME in the configure.
    depends_on('cuda', when='+cuda')
    # - hip dependency. We use the environment variable HIP_PATH in the configure.
    depends_on('hip', when='+hip')
    # - level_zero is not in any spack package at this moment.
    # - hwloc >= 2.1 becomes a dependency when +hwloc variant is used.
    depends_on('hwloc@2.1:', when='+hwloc')
    # - ocl-icd >= 2.1 becomes a dependency when +opencl variant is used.
    depends_on('ocl-icd@2.1:', when='+opencl')

    # when on master, we need all the autotools and extras to generate files.
    with when('@master'):
        depends_on('m4', type='build')
        depends_on('autoconf', type='build')
        depends_on('automake', type='build')
        depends_on('libtool', type='build')
        # Required to have pkg config macros in configure.
        depends_on('pkgconf', type='build')
        # Required to generate AML version in configure.
        depends_on('git', type='build')

    # Configure options management
    ###########################################

    # This is the function to overload to pass all hwloc flag.
    def configure_args(self):
        config_args = []
        for b in ['opencl', 'hwloc', 'ze', 'hip', 'cuda']:
            config_args.extend(self.with_or_without(b))
        if 'openmp-targets=spir64' in self.spec:
            config_args += ['--with-openmp-flags="-fiopenmp -fopenmp-targets=spir64"']
        if 'hip-platform=amd' in self.spec:
            config_args += ['--with-hip-platform=amd']
        if 'hip-platform=nvidia' in self.spec:
            config_args += ['--with-hip-platform=nvidia']
        return config_args

    # Tests
    #########################

    smoke_test = '0_hello'
    smoke_test_src = join_path('doc', 'tutorials', 'hello_world', smoke_test + '.c')

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(self.smoke_test_src)

    def run_install_tutorial_check(self):
        """Run tutorial tests as install checks"""

        src = join_path(self.test_suite.current_test_cache_dir, self.smoke_test_src)
        cc_exe = os.environ['CC']
        cc_options = ['-o', self.smoke_test, src,
                      '-I{0}'.format(self.prefix.include),
                      '-I{0}'.format(self.spec['numactl'].prefix.include),
                      '-L{0}'.format(self.prefix.lib),
                      '-laml', '-lexcit', '-lpthread']

        self.run_test(cc_exe, cc_options,
                      purpose='test: compile {0} tutorial'.format(self.smoke_test))
        self.run_test(self.smoke_test,
                      purpose='test: run {0} tutorial'.format(self.smoke_test))

    def test(self):
        self.run_install_tutorial_check()
