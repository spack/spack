# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arborx(CMakePackage):
    """ArborX is a performance-portable library for geometric search"""

    homepage = "https://github.com/arborx/arborx"
    url      = "https://github.com/arborx/arborx/archive/v1.1.tar.gz"
    git      = "https://github.com/arborx/arborx.git"

    tags = ['e4s']

    maintainers = ['aprokop']

    version('master',   branch='master')
    version('1.1',      sha256='2b5f2d2d5cec57c52f470c2bf4f42621b40271f870b4f80cb57e52df1acd90ce')
    version('1.0',      sha256='9b5f45c8180622c907ef0b7cc27cb18ba272ac6558725d9e460c3f3e764f1075')
    version('0.9-beta', sha256='b349b5708d1aa00e8c20c209ac75dc2d164ff9bf1b85adb5437346d194ba6c0d')

    # ArborX relies on Kokkos to provide devices, providing one-to-one matching
    # variants. The only way to disable those devices is to make sure Kokkos
    # does not provide them.
    kokkos_backends = {
        'serial': (True,  "enable Serial backend (default)"),
        'cuda': (False,  "enable Cuda backend"),
        'openmp': (False,  "enable OpenMP backend"),
        'rocm': (False,  "enable HIP backend"),
        'sycl': (False, "enable SYCL backend")
    }

    variant('mpi', default=True, description='enable MPI')
    for backend in kokkos_backends:
        deflt, descr = kokkos_backends[backend]
        variant(backend.lower(), default=deflt, description=descr)
    variant('trilinos', default=False, description='use Kokkos from Trilinos')

    depends_on('cmake@3.12:', type='build')
    depends_on('cmake@3.16:', type='build', when='@1.0:')
    depends_on('mpi', when='+mpi')

    # Standalone Kokkos
    depends_on('kokkos@3.1.00:', when='~trilinos')
    for backend in kokkos_backends:
        depends_on('kokkos+%s' % backend.lower(), when='~trilinos+%s' %
                   backend.lower())
    depends_on('kokkos+cuda_lambda', when='~trilinos+cuda')

    # Trilinos/Kokkos
    # Notes:
    # - current version of Trilinos package does not allow disabling Serial
    # - current version of Trilinos package does not allow enabling CUDA
    depends_on('trilinos+kokkos', when='+trilinos')
    depends_on('trilinos+openmp', when='+trilinos+openmp')
    conflicts('~serial', when='+trilinos')
    conflicts('+cuda', when='+trilinos')

    def cmake_args(self):
        spec = self.spec

        options = [
            '-DKokkos_ROOT=%s' % (spec['kokkos'].prefix if '~trilinos' in spec
                                  else spec['trilinos'].prefix),
            self.define_from_variant('ARBORX_ENABLE_MPI', 'mpi')
        ]

        if '+cuda' in spec:
            # Only Kokkos allows '+cuda' for now
            options.append(
                '-DCMAKE_CXX_COMPILER=%s' % spec["kokkos"].kokkos_cxx)

        return options

    examples_src_dir = "examples"

    @run_after('install')
    def setup_build_tests(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.examples_src_dir])

    @property
    def cached_tests_work_dir(self):
        """The working directory for cached test sources."""
        return join_path(self.test_suite.current_test_cache_dir,
                         self.examples_src_dir)

    def build_tests(self):
        """Build the stand-alone/smoke test."""

        arborx_dir = self.spec['arborx'].prefix
        cmake_prefix_path = "-DCMAKE_PREFIX_PATH={0}".format(arborx_dir)
        if '+mpi' in self.spec:
            cmake_prefix_path += ";{0}".format(self.spec['mpi'].prefix)

        cmake_args = [".",
                      cmake_prefix_path,
                      "-DCMAKE_CXX_COMPILER={0}".format(self.compiler.cxx),
                      self.define('Kokkos_ROOT', self.spec['kokkos'].prefix
                                  if '~trilinos' in self.spec
                                  else self.spec['trilinos'].prefix)]

        self.run_test("cmake", cmake_args,
                      purpose="test: calling cmake",
                      work_dir=self.cached_tests_work_dir)

        self.run_test("make", [],
                      purpose="test: building the tests",
                      work_dir=self.cached_tests_work_dir)

    def test(self):
        """Perform stand-alone/smoke tests on the installed package."""
        self.build_tests()

        self.run_test("ctest", ["-V"],
                      purpose="test: running the tests",
                      installed=False,
                      work_dir=self.cached_tests_work_dir)
