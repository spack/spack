# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMatplotlibInline(PythonPackage):
    """Inline Matplotlib backend for Jupyter."""

    homepage = "https://github.com/ipython/matplotlib-inline"
    pypi     = "matplotlib-inline/matplotlib-inline-0.1.2.tar.gz"

    version('0.1.3', sha256='a04bfba22e0d1395479f866853ec1ee28eea1485c1d69a6faf00dc3e24ff34ee')
    version('0.1.2', sha256='f41d5ff73c9f5385775d5c0bc13b424535c8402fe70ea8210f93e11f3683993e')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-traitlets', type=('build', 'run'))
