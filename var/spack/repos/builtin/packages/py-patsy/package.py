# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPatsy(PythonPackage):
    """A Python package for describing statistical models and for
    building design matrices."""

    homepage = "https://github.com/pydata/patsy"
    url      = "https://pypi.io/packages/source/p/patsy/patsy-0.4.1.zip"

    version('0.4.1', '9445f29e3426d1ed30d683a1e1453f84')

    variant('splines', description="Offers spline related functions")

    depends_on('py-setuptools',  type='build')
    depends_on('py-numpy',       type=('build', 'run'))
    depends_on('py-scipy',       type=('build', 'run'), when="+splines")
    depends_on('py-six',         type=('build', 'run'))

    depends_on('py-nose', type='test')
