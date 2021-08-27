# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RIrkernel(RPackage):
    """R kernel for Jupyter"""

    homepage = "https://irkernel.github.io/"
    git      = "https://github.com/IRkernel/IRkernel.git"

    version('1.2', commit='d7f868127b876fd490aeff2a75b4254a2898f96c')
    version('0.7', commit='9cdd284e03eb42d03fab18544b81f486852d5fe0')

    depends_on('r-repr', type=('build', 'run'))
    depends_on('r-irdisplay', type=('build', 'run'))
    depends_on('r-evaluate', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-pbdzmq', type=('build', 'run'))
    depends_on('r-devtools', type=('build', 'run'))
    depends_on('r-uuid', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
