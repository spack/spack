# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class HsfCmaketools(Package):
    """CMake 'Find' modules for commonly used HEP Packages"""

    homepage = "https://github.com/HSF/cmaketools/"
    url      = "https://github.com/HSF/cmaketools/archive/1.8.tar.gz"
    git      = "https://github.com/HSF/cmaketools.git"

    maintainers = ['vvolkl']

    version('1.8', sha256='91af30f5701dadf80a5d7e0d808c224c934f0784a3aff2d3b69aff24f7e1db41')

    def install(self, spec, prefix):
        mkdir(join_path(prefix, "modules"))
        copy_tree('modules', join_path(prefix, 'modules'))
        copy("CMakeToolsConfig.cmake", prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('CMAKE_PREFIX_PATH', self.prefix)
