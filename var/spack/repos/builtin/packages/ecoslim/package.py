# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Ecoslim(CMakePackage):
    """EcoSLIM is a Lagrangian, particle-tracking code that simulates
    advective and diffusive movement of water parcels. This code can
    be used to simulate age, diagnose travel times, source water
    composition and flowpaths. It integrates seamlessly with
    ParFlow-CLM."""

    homepage = "https://github.com/reedmaxwell/EcoSLIM"
    url      = "https://github.com/reedmaxwell/EcoSLIM/archive/refs/tags/v1.3.tar.gz"
    git      = "git@github.com:reedmaxwell/EcoSLIM.git"

    maintainers = ['smithsg84']

    version('1.3', sha256='b532e570b4767e4fa84123d8773732150679e8e3d7fecd5c6e99fb1d4dc57b84')
    version('develop', branch='develop')

    def cmake_args(self):
        """Populate cmake arguments for EcoSLIM."""
        spec = self.spec

        cmake_args = []

        return cmake_args

