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
    version('0.0.7', sha256='9cd3f005b65f6697b9229f2c2d1ef483ac5b62e036463fa28b267f8ffd861b54')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-plotly@3.4.2:', type='run')
    depends_on('py-numpy@1.15.4:', type='run')
    depends_on('py-neurom+plotly@3.0:3.999', type='run', when='@0.0.8:')
    depends_on('py-neurom+plotly@2.0:2.999', type='run', when='@:0.0.7')
    depends_on('py-click@6.0:', type='run')
