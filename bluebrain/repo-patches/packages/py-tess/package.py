# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack import *


class PyTess(PythonPackage):
    """A module for calculating and analyzing Voronoi tessellations"""

    homepage = "https://github.com/wackywendell/tess"
    url = "https://pypi.io/packages/source/t/tess/tess-0.3.0.tar.gz"

    version('0.3.1', sha256='e48734ebe2bb096461d6ddafdda2792650400af1d7a90c98cef53bd6364916d2')
    version('0.3.0', sha256='68105859bf10c04bf2df73450f1f800fa842d1323be65a81ca447f2528fa5ad6')

    depends_on('py-cython', type='build')
    depends_on('py-setuptools', type='build')

    def patch(self):
        os.unlink("tess/_voro.cpp")
