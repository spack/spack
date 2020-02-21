# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepysnap(PythonPackage):
    """Pythonic Sonata circuits access API"""

    homepage = "https://github.com/BlueBrain/snap"
    git      = "git@github.com:BlueBrain/snap.git"
    url      = "https://pypi.io/packages/source/b/bluepysnap"

    version('0.2.0', tag='v0.2.0')
    version('0.1.2', tag='v0.1.2')
    version('0.1.1', tag='v0.1.1')
    version('0.1.0', tag='v0.1.0')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-functools32', type='run', when='^python@:3.1.99')
    depends_on('py-cached-property@1.0:', type='run')
    depends_on('py-h5py@2.2:', type='run')
    depends_on('py-libsonata@0.0.3:', type='run')
    depends_on('py-neurom@1.3:', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-six@1.0:', type='run')

    depends_on('py-click@7.0:', type='run')
    depends_on('py-pathlib2@2.3:', type='run')
