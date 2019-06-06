# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTess(PythonPackage):
    """A module for calculating and analyzing Voronoi tessellations"""

    homepage = "https://github.com/wackywendell/tess"
    url = "https://pypi.io/packages/source/t/tess/tess-0.3.0.tar.gz"

    version('0.3.0', sha256='68105859bf10c04bf2df73450f1f800fa842d1323be65a81ca447f2528fa5ad6', preferred=True)

    depends_on('py-setuptools', type='build')
