# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPlotlyHelper(PythonPackage):
    """Package that makes plotly easy."""

    homepage = "https://github.com/bluebrain/plotly-helper"
    git = "https://github.com/BlueBrain/plotly-helper.git"
    url = "https://pypi.io/packages/source/p/plotly-helper/plotly-helper-0.0.7.tar.gz"

    version('develop', branch='master')
    version('0.0.8', sha256='fda9f3c744c679b74ef2f34fa0e0fd00426a95b6e8604a57904c7438628f9233')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-plotly@3.4.2:', type=('build', 'run'))
    depends_on('py-numpy@1.15.4:', type=('build', 'run'))
    depends_on('py-neurom+plotly@3.0:3.999', type=('build', 'run'))
    depends_on('py-click@6.0:', type=('build', 'run'))
