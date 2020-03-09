# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class F18(CMakePackage):
    """F18 is a front-end for Fortran intended to replace the existing front-end
    in the Flang compiler"""

    # Package information
    homepage = "https://github.com/flang-compiler/f18"
    git      = "https://github.com/flang-compiler/f18.git"

    version('master', branch='master')

    # Variants
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    # Dependencies
    depends_on('cmake@3.9.0:', type='build')
    depends_on('llvm+clang@7:')

    # Conflicts
    compiler_warning = 'F18 requires a compiler with support for C++17'
    conflicts('%clang@:6', msg=compiler_warning)
    conflicts('%gcc@:7.1', msg=compiler_warning)
    conflicts('%intel', msg=compiler_warning)
    conflicts('%pgi', msg=compiler_warning)
