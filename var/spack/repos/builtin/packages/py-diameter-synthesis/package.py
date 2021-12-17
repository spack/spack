# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDiameterSynthesis(PythonPackage):
    """Python library to generate synthetic diameters for neurons."""

    homepage = "https://github.com/BlueBrain/diameter-synthesis"
    git      = "https://github.com/BlueBrain/diameter-synthesis.git"

    version('0.2.5', tag='0.2.5')

    depends_on('py-setuptools', type='build')

    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-numpy@1.15.0:', type=('build', 'run'))
    depends_on('py-scipy@0.13.3:', type=('build', 'run'))
    depends_on('py-matplotlib@2.2:', type=('build', 'run'))
    depends_on('py-pandas@0.24:', type=('build', 'run'))
    depends_on('py-neurom@3.0:3.999', type=('build', 'run'))
    depends_on('py-morphio@2.3.4:', type=('build', 'run'))
    depends_on('py-jsonschema@3:', type=('build', 'run'))
