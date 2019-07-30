# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-pyod
#
# You can edit this file again by typing:
#
#     spack edit py-pyod
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPyod(PythonPackage):
    """A Python Toolbox for Scalable Outlier Detection (Anomaly Detection)."""

    homepage = "http://pyod.readthedocs.io"
    url      = "https://github.com/yzhao062/pyod/archive/v0.7.0.tar.gz"

    version('0.7.0', sha256='8048f23f0e85c689f533966b190293ccb9b352334b2c03f0fdcc9c227fdd8462')

    depends_on('py-setuptools',     type='build')
    depends_on('py-joblib',         type=('build', 'run'))
    depends_on('py-matplotlib',     type=('build', 'run'))
    depends_on('py-numpy',          type=('build', 'run'))
    depends_on('py-numba',          type=('build', 'run'))
    depends_on('py-scipy',          type=('build', 'run'))
    depends_on('py-scikit-learn',   type=('build', 'run'))
    depends_on('py-six',            type=('build', 'run'))

