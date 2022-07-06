# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySklearn(PythonPackage):
    """Python module for machine learning built on top of SciPy"""

    homepage = "https://pypi.org/project/sklearn/"
    pypi     = "sklearn/sklearn-0.0.tar.gz"

    version('0.0', sha256='e23001573aa194b834122d2b9562459bf5ae494a2d59ca6b8aa22c85a44c0e31')

    depends_on('python@3.8:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
