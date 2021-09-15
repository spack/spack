# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FeqParse(CMakePackage):
    """An equation parser Fortran class that
       is used to interpret and evaluate functions
       provided as strings."""

    homepage = "https://github.com/FluidNumerics/feq-parse"
    url      = "https://github.com/FluidNumerics/feq-parse"
    baseurl  = "https://github.com/FluidNumerics/feq-parse"
    git      = "https://github.com/FluidNumerics/feq-parse.git"

    maintainers = ['fluidnumerics-joe']

    version('v1.1.0', tag='v1.1.0')
    version('v1.0.2', tag='v1.0.2')
    version('master', branch='master')

    depends_on('cmake@3.0.2:', type='build')
