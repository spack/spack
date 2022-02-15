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
    version('0.13.1', sha256='85a7bedb304f862fdc9138e98c84617ec7821f01439fde2989e179d7aba37ff0')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-cached-property@1.0:', type=('build', 'run'))
    depends_on('py-h5py@3.0.1:3.999', type=('build', 'run'))
    depends_on('py-libsonata@0.1.6:0.999', type=('build', 'run'))
    depends_on('py-morphio@3.0.0:3.999', type=('build', 'run'))
    depends_on('py-morph-tool@2.4.3:2.999', type=('build', 'run'))
    depends_on('py-numpy@1.8:1.999', type=('build', 'run'))
    depends_on('py-pandas@1.0.0:1.999', type=('build', 'run'))
    depends_on('py-click@7.0:', type=('build', 'run'))
    depends_on('py-more-itertools@8.2.0:', type=('build', 'run'))
