# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPlotlyHelper(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/plotly-helper"
    git      = "ssh://bbpcode.epfl.ch/nse/plotly-helper"

    version('develop', branch='master')
    version('0.0.2', tag='plotly-helper-v0.0.2')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-neurom@mut_morphio+plotly', type='run')
