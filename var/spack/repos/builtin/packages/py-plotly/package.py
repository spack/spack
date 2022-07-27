# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlotly(PythonPackage):
    """An interactive, browser-based graphing library for Python"""

    homepage = "https://plot.ly/python/"
    pypi = "plotly/plotly-2.2.0.tar.gz"

    version('5.2.2', sha256='809f0674a7991daaf4f287964d617d24e9fa44463acd5a5352ebd874cfd98b07')
    version('2.2.0', sha256='ca668911ffb4d11fed6d7fbb12236f8ecc6a7209db192326bcb64bdb41451a58')

    depends_on('python@3.6:', when='@5.2.2:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))

    depends_on('py-pytz',             when='@:2.2.0', type=('build', 'run'))
    depends_on('py-decorator@4.0.6:', when='@:2.2.0', type=('build', 'run'))
    depends_on('py-nbformat@4.2.0:',  when='@:2.2.0', type=('build', 'run'))
    depends_on('py-requests',         when='@:2.2.0', type=('build', 'run'))

    depends_on('py-tenacity@6.2.0:',  when='@5.2.2:', type=('build', 'run'))
