# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyNeuror(PythonPackage):
    """A collection of tools to repair morphologies."""

    homepage = "https://github.com/BlueBrain/NeuroR"
    git = "https://github.com/BlueBrain/NeuroR.git"
    url = "https://pypi.io/packages/source/n/neuror/NeuroR-1.2.3.tar.gz"

    version('develop', branch='master')
    version('1.2.3', sha256='eb1c06748bf7706919cd78ab92bbb2420d5ac1dcaf54566c6f5aca403c63c215')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:', type='run')
    depends_on('py-matplotlib@2.2.3:', type='run')
    depends_on('py-morph-tool@0.1.14:', type='run')
    depends_on('py-morphio@2.1.1:', type='run')
    depends_on('py-neurom@2.0:', type='run')
    depends_on('py-numpy@1.19.2:', type='run')
    depends_on('py-nptyping@1.3.0:', type='run')
    depends_on('py-pandas@0.24.2:', type='run')
    depends_on('py-pyquaternion@0.9.2:', type='run')
    depends_on('py-scipy@1.2.0:', type='run')
