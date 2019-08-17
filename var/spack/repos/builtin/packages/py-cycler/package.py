# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCycler(PythonPackage):
    """Composable style cycles."""

    homepage = "http://matplotlib.org/cycler/"
    url      = "https://github.com/matplotlib/cycler/archive/v0.10.0.tar.gz"

    version('0.10.0', '83dd0df7810e838b59e4dd9fa6e2d198')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
