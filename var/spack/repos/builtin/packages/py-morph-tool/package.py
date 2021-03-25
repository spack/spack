# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMorphTool(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://github.com/BlueBrain/morph-tool"
    git      = "https://github.com/BlueBrain/morph-tool.git"
    url      = "https://pypi.io/packages/source/m/morph-tool/morph-tool-0.2.5.tar.gz"

    version('develop', branch='master')
    version('2.4.0', sha256='268915ad48f2a2475bbc4685bd1a3610f22978fee1cb4d376d87f45ae4a028e1')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-bluepyopt@1.9.37:', type='run')
    depends_on('py-click@6.7:', type='run')
    depends_on('py-deprecation@2.1.0:', type='run')
    depends_on('py-more-itertools@8.6.0:', type='run')
    depends_on('py-morphio@2.7.0:', type='run')
    depends_on('py-neurom@1.8.0:', type='run')
    depends_on('py-numpy@1.14:', type='run')
    depends_on('py-pandas@1.0.3:', type='run')
    depends_on('py-xmltodict@0.12:', type='run')

    depends_on('py-plotly@4.1:', type='run')
    depends_on('py-dask+bag@2.19:', type='run')
    depends_on('neuron+python@7.8:', type='run')
