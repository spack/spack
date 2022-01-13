# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMatplotlibscalebar(PythonPackage):
    """Provides a new artist for matplotlib to display a scale bar,
     aka micron bar."""

    homepage = "https://github.com/ppinard/matplotlib-scalebar"
    git      = "https://github.com/ppinard/matplotlib-scalebar.git"

    version('develop', git=git, branch='master')
    version('0.6.1', git=git, tag='0.6.1')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-matplotlib', type=('build', 'run'))
