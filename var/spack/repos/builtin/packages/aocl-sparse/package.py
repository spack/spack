# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import inspect


class AoclSparse(CMakePackage):
    """AOCL-Sparse is a library that contains basic linear algebra subroutines
    for sparse matrices and vectors optimized for AMD EPYC family of processors.
    It is designed to be used with C and C++. Current functionality of sparse
    library supports SPMV function with CSR and ELLPACK formats."""

    homepage = "https://developer.amd.com/amd-aocl/aocl-sparse/"
    url = "https://github.com/amd/aocl-sparse/archive/2.2.tar.gz"
    git = "https://github.com/amd/aocl-sparse.git"

    maintainers = ['amd-toolchain-support']

    version('2.2',  sha256='33c2ed6622cda61d2613ee63ff12c116a6cd209c62e54307b8fde986cd65f664')

    conflicts("%gcc@:9.1.999", msg="Minimum required GCC version is 9.2.0")

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release'))
    variant('shared', default=True,
            description='Build shared library')

    depends_on('boost')

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """

        builddir = self.stage.source_path

        if self.spec.variants['build_type'].value == 'Debug':
            builddir = join_path(self.stage.source_path, 'build', 'debug')
        else:
            builddir = join_path(self.stage.source_path, 'build', 'release')

        mkdirp(builddir)
        return builddir

    def cmake(self, spec, prefix):
        """Runs ``cmake`` in the build directory"""
        args = [
            "../..",
            "-DCMAKE_INSTALL_PREFIX:PATH={0}".format(spec.prefix),
            "-DCMAKE_CXX_COMPILER={0}".format(os.path.basename(spack_cxx))
        ]

        if spec.variants['build_type'].value == 'Debug':
            args.append("-DCMAKE_BUILD_TYPE=Debug")
        else:
            args.append("-DCMAKE_BUILD_TYPE=Release")

        args.extend([
            "-DBUILD_SHARED_LIBS:BOOL=%s" % (
                'ON' if '+shared' in spec else 'OFF'
            )
        ])

        args.extend([
            "-DBUILD_CLIENTS_BENCHMARKS:BOOL=%s" % (
                'ON' if self.run_tests else 'OFF'
            )
        ])

        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).cmake(*args)

    # Check that self.prefix is there after installation
    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check(self):
        """ Simple test to test the installation by running
        one of the aocl-sparse examples, after compiling the
        library with benchmarks.
        """
        dso_suffix = 'so' if '+shared' in self.spec else 'a'

        if self.spec.variants['build_type'].value == 'Debug':
            build_path = join_path(self.stage.source_path, 'build', 'debug')
            lib_path = join_path(build_path,
                                 'library',
                                 'libaoclsparse-d.{0}'.format(dso_suffix))
        else:
            build_path = join_path(self.stage.source_path, 'build', 'release')
            lib_path = join_path(build_path,
                                 'library',
                                 'libaoclsparse.{0}'.format(dso_suffix))

        # with working_dir(join_path(build_path, 'tests', 'staging')):
        bin_path = join_path(build_path, 'tests', 'staging', 'aoclsparse-bench')
        bin_args = " --function=csrmv --precision=d "
        bin_args = bin_args + "--sizem=1000 --sizen=1000 --sizennz=4000 --verify=1 "
        unit_test = bin_path + bin_args + lib_path
        os.system(unit_test)
