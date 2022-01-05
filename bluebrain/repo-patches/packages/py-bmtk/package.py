# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBmtk(PythonPackage):
    """The Brain Modeling Toolkit"""

    homepage = "https://github.com/AllenInstitute/bmtk"
    url      = "https://pypi.io/packages/source/b/bmtk/bmtk-0.0.8.tar.gz"

    version('0.0.8', sha256='00ab884a94e4f19f26d64476021c036178332396a10bc5d02164dfd633f169f4')

    depends_on('python@3.6:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    depends_on('py-jsonschema',   type=('run'))
    depends_on('py-pandas',       type=('run'))
    depends_on('py-numpy',        type=('run'))
    depends_on('py-six',          type=('run'))
    depends_on('py-h5py',         type=('run'))
    depends_on('py-matplotlib',   type=('run'))
    depends_on('py-scipy',        type=('run'))
    depends_on('py-scikit-image', type=('run'))
    depends_on('py-sympy',        type=('run'))
