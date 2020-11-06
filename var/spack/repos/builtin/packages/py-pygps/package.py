# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygps(PythonPackage):
    """pyGPs is a Python library for Gaussian Process (GP)
       Regression and Classification."""

    homepage = "https://github.com/marionmari/pyGPs"
    url      = "https://files.pythonhosted.org/packages/05/68/90138cccbdd5aa95b69761d4b3ef7d90594094c574c0696a09af64a6e3c1/pyGPs-1.3.5.tar.gz"

    version('1.3.5', sha256='5af668415a7bf1666c7c6da3bb09d29e48c395862c6feb23964b476972a015d4')

    depends_on('py-setuptools',  type='build')
    depends_on('py-numpy',       type=('build', 'run'))
    depends_on('py-scipy@0.13:', type=('build', 'run'))
    depends_on('py-matplotlib',  type=('build', 'run'))
    depends_on('py-future',      type=('build', 'run'))
