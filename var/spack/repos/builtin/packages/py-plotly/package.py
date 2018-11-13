# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPlotly(PythonPackage):
    """An interactive, browser-based graphing library for Python"""

    homepage = "https://plot.ly/python/"
    url      = "https://github.com/plotly/plotly.py/archive/v2.2.0.tar.gz"

    version('2.2.0', '835802cdc6743439ff993447dfe47a0e')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.3.0', type=('build', 'run'))
    depends_on('py-six@1.8.0', type=('build', 'run'))
    depends_on('py-pytz@2014.9', type=('build', 'run'))
