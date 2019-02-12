# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gmodel(CMakePackage):
    """Gmsh model generation library

      Gmodel is a C++11 library that implements a minimal CAD kernel based
      on the .geo format used by the Gmsh mesh generation code, and is
      designed to make it easier for users to quickly construct CAD models
      for Gmsh.
    """
    homepage = "https://github.com/ibaned/gmodel"
    url      = "https://github.com/ibaned/gmodel/archive/v2.1.0.tar.gz"

    version('2.1.0', '80df0c6dc413a9ffa0f0e7b65118b05b643ba3e1bfcac28fb91d2d3ad017fda0')
