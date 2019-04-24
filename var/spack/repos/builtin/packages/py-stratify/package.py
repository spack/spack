# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyStratify(PythonPackage):
    """Vectorized interpolators that are especially useful for
    Nd vertical interpolation/stratification of atmospheric and
    oceanographic datasets.
    """

    homepage = "https://github.com/SciTools-incubator/python-stratify"
    url      = "https://github.com/SciTools-incubator/python-stratify/archive/v0.1.tar.gz"

    version('0.1', sha256='e154383bd2336122d153daa85f5ec9f5ba7639df0bf6ee66a52a7fb7b30d3377')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-cython',     type=('build', 'run'))
