# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PySeaborn(PythonPackage):
    """Seaborn: statistical data visualization.

    Seaborn is a library for making attractive and informative statistical
    graphics in Python. It is built on top of matplotlib and tightly
    integrated with the PyData stack, including support for numpy and pandas
    data structures and statistical routines from scipy and statsmodels."""

    homepage = "https://seaborn.pydata.org/"
    pypi = "seaborn/seaborn-0.7.1.tar.gz"

    version('0.11.2',    sha256='cf45e9286d40826864be0e3c066f98536982baf701a7caa386511792d61ff4f6')
    version('0.11.1', sha256='44e78eaed937c5a87fc7a892c329a7cc091060b67ebd1d0d306b446a74ba01ad')
    version('0.9.0', sha256='76c83f794ca320fb6b23a7c6192d5e185a5fcf4758966a0c0a54baee46d41e2f')
    version('0.7.1', sha256='fa274344b1ee72f723bab751c40a5c671801d47a29ee9b5e69fcf63a18ce5c5d')

    depends_on('python@3.6:', when='@0.10:', type='build')
    depends_on('py-setuptools', type='build')

    depends_on('py-numpy@1.15:', when='@0.11:', type=('build', 'run'))
    depends_on('py-numpy@1.9.3:', when='@0.9:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy@1:', when='@0.11:', type=('build', 'run'))
    depends_on('py-scipy@1.0.1:', when='@0.10:', type=('build', 'run'))
    depends_on('py-scipy@0.14:', when='@0.9.0:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-pandas@0.23:', when='@0.11:', type=('build', 'run'))
    depends_on('py-pandas@0.22:', when='@0.10:', type=('build', 'run'))
    depends_on('py-pandas@0.15.2:', when='@0.9:', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-matplotlib@2.2:', when='@0.11:', type=('build', 'run'))
    depends_on('py-matplotlib@2.1.2:', when='@0.10:', type=('build', 'run'))
    depends_on('py-matplotlib@1.4.3:', when='@0.9:', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
