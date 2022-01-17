# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepysnap(PythonPackage):
    """Pythonic Sonata circuits access API"""

    homepage = "https://github.com/BlueBrain/snap"
    git      = "https://github.com/BlueBrain/snap.git"
    url      = "https://pypi.io/packages/source/b/bluepysnap/bluepysnap-0.12.0.tar.gz"

    version('develop', branch='master')
    version('0.13.0', sha256='7a59cf06db9c22b16b717ae1164f4108282c146b78fbf538197d838920121d16')
    version('0.12.0', sha256='a2cc24031905310941296ca975814ee0c0f27229a2c133d6a13ca92cc8dc6c9b')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-cached-property@1.0:', type=('build', 'run'))
    depends_on('py-h5py@3.0.1:3.999', type=('build', 'run'))
    depends_on('py-libsonata@0.1.6:0.999', type=('build', 'run'))
    depends_on('py-morphio@3.0.0:3.999', type=('build', 'run'))
    depends_on('py-morph-tool@2.4.3:2.999', type=('build', 'run'))
    depends_on('py-numpy@1.8:1.999', type=('build', 'run'))
    depends_on('py-pandas@1.0.0:1.999', type=('build', 'run'))
    depends_on('py-click@7.0:7.999', type=('build', 'run'))
    depends_on('py-more-itertools@8.2.0:', type=('build', 'run'))
