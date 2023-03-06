# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack import *


class Fckit(CMakePackage):
    """A Fortran toolkit for interoperating Fortran with C/C++."""

    homepage = "https://software.ecmwf.int/wiki/display/fckit"
    git = "https://github.com/ecmwf/fckit.git"
    url = "https://github.com/ecmwf/fckit/archive/0.9.0.tar.gz"

    maintainers = ['climbfuji']

    version('master', branch='master')
    version('develop', branch='develop')
    version("0.10.0", sha256="f16829f63a01cdef5e158ed2a51f6d4200b3fe6dce8f251af158141a1afe482b")
    version("0.9.5", sha256="183cd78e66d3283d9e6e8e9888d3145f453690a4509fb701b28d1ac6757db5de")

    depends_on('mpi')
    depends_on('python')
    depends_on('ecbuild', type=('build'))

    variant('build_type', default='RelWithDebInfo',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    variant('eckit', default=True)
    depends_on('eckit+mpi', when='+eckit')

    variant('openmp', default=True, description='Use OpenMP?')
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "run"))
    variant('shared', default=True)
    variant("fismahigh", default=False, description="Apply patching for FISMA-high compliance")

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_ECKIT', 'eckit'),
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            "-DPYTHON_EXECUTABLE:FILEPATH=" + self.spec['python'].command.path,
            '-DFYPP_NO_LINE_NUMBERING=ON'
        ]

        if '~shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        if self.spec.satisfies('%intel') or self.spec.satisfies('%gcc'):
            cxxlib = 'stdc++'
        elif self.spec.satisfies('%clang') or self.spec.satisfies('%apple-clang'):
            cxxlib = 'c++'
        else:
            raise InstallError("C++ library not configured for compiler")
        args.append('-DECBUILD_CXX_IMPLICIT_LINK_LIBRARIES={}'.format(cxxlib))

        return args

    @when("+fismahigh")
    def patch(self):
        patterns = ["tools/install-*", "tools/github-sha*", ".travis.yml"]
        for pattern in patterns:
            for path in glob.glob(pattern):
                os.remove(path)
