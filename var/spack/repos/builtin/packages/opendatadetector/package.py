# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

class Opendatadetector(CMakePackage):
    """Open Data Detector for High Energy Physics."""
    homepage = "https://gitlab.cern.ch/acts/OpenDataDetector.git"
    git      = "https://gitlab.cern.ch/acts/OpenDataDetector.git"

    maintainers = ['vvolkl']

    version('main', branch='main')
    version("v2", tag="v2")
    version("v1", tag="v1")

    depends_on('dd4hep')
    depends_on('root')
    depends_on('boost')

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append('-DCMAKE_CXX_STANDARD=%s' % self.spec['root'].variants['cxxstd'].value)
        return args

    def setup_run_environment(self, env):
        env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
        env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib64)
