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
    version('1.4.2', sha256='f5e18ebddf59a60ce650c24eb49042057cf97990d63aee3ceb58b7acff823255')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@6.7:', type=('build', 'run'))
    depends_on('py-matplotlib@2.2.3:', type=('build', 'run'))
    depends_on('py-morph-tool@2.9.0:2.999', type=('build', 'run'))
    depends_on('py-morphio@3.0:3.999', type=('build', 'run'))
    depends_on('py-neurom@3.0:3.999', type=('build', 'run'))
    depends_on('py-numpy@1.19.2:', type=('build', 'run'))
    depends_on('py-nptyping@1.3.0:', type=('build', 'run'))
    depends_on('py-pandas@0.24.2:', type=('build', 'run'))
    depends_on('py-pyquaternion@0.9.2:', type=('build', 'run'))
    depends_on('py-scipy@1.2.0:', type=('build', 'run'))
