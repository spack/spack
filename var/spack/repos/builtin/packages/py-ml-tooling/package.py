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
#     spack install py-ml-tooling
#
# You can edit this file again by typing:
#
#     spack edit py-ml-tooling
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyMlTooling(PythonPackage):
    """Utility library for Machine Learning."""

    homepage = "https://ml-tooling.readthedocs.io"
    url      = "https://github.com/andersbogsnes/ml_tooling/archive/0.7.tar.gz"

    version('0.7', sha256='1d9ca6eea886959621ee84405c8b652d3015e7e9e1f6a774b64a03b5892342e1')

    depends_on('py-setuptools',       type='build')
    depends_on('py-scikit-learn',     type=('build', 'run'))
    depends_on('py-pandas',           type=('build', 'run'))
    depends_on('py-matplotlib',       type=('build', 'run'))
    depends_on('py-numpy',            type=('build', 'run'))
    depends_on('py-gitpython',        type=('build', 'run'))
    depends_on('py-joblib',           type=('build', 'run'))

