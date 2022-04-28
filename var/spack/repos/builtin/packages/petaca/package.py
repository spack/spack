# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Petaca(CMakePackage):
    """A collection of modern Fortran modules.

    Modules include:
    - Parameter lists
    - map_any_type
    - fortran_dynamic_loader
    - timer_tree_type
    - yajl_fort
    - json
    """

    homepage = "https://petaca.readthedocs.io/en/master"
    git      = "https://github.com/nncarlson/petaca.git"
    url      = "https://github.com/nncarlson/petaca/archive/refs/tags/v22.03.tar.gz"

    maintainers = ['pbrady']

    version('develop', branch="master")
    version('22.03', sha256='e6559e928c7cca6017ef0582c204eee775f6bb3f927f1c224c515c2ad574cc32')
    version('21.03', commit='f17df95193ca1a3879687a59a91a123be25e3efa')

    depends_on('cmake@3.3:', type='build')
    depends_on('yajl@2.0.1:')

    # override RelWithDebugInfo since those flags aren't set in petaca
    variant('build_type', default="Release",
            description='Type build type to build',
            values=('Debug', 'Release'))

    variant('shared', default=False, description='build shared libraries')

    variant('std_name', default=False, description='enables std_mod_proc_name with intel')

    # copied from openmpi/package.py to ensure fortran support
    @run_before('cmake')
    def die_without_fortran(self):
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError(
                'petaca requires both C and Fortran compilers!'
            )

    def cmake_args(self):
        return [
            self.define('ENABLE_TESTS', self.run_tests),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_STD_MOD_PROC_NAME", "std_name")
        ]
