# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.gmsh import Gmsh as BuiltinGmsh


class Gmsh(BuiltinGmsh):
    version('4.9.0', sha256='b8ef133c9b66ffe12df1747e72d4acf19f1eb1e9cd95eb0f577cbc4081d9bea3')
