# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPauvr(PythonPackage):
    """pauvr: a plotting package designed for nanopore and PacBio long reads"""

    homepage = "https://github.com/conchoecia/pauvre"
    git      = "https://github.com/conchoecia/pauvre.git"

    version('develop', branch='develop')
    version('master',  branch='master')
    version('0.1.86',  tag='0.1.86')

    depends_on('python@3:',        type=('build', 'run'))
    depends_on('py-matplotlib',    type=('build', 'run'))
    depends_on('py-biopython',     type=('build', 'run'))
    depends_on('py-pandas',        type=('build', 'run'))
    depends_on('py-pillow',        type=('build', 'run'))
