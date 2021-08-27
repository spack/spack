# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNilearn(PythonPackage):
    """Statistical learning for neuroimaging in Python."""

    homepage = "https://nilearn.github.io/"
    pypi     = "nilearn/nilearn-0.7.1.tar.gz"

    version('0.8.0', sha256='f2d3dc81005f829f3a183efa6c90d698ea6818c06264d2e3f03e805c4340febb')
    version('0.7.1', sha256='8b1409a5e1f0f6d1a1f02555c2f11115a2364f45f1e57bcb5fb3c9ea11f346fa')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@0.8.0:')
    depends_on('py-setuptools', type='build')

    variant('plotting', default=False, description='Enable plotting functionalities')

    depends_on('py-numpy@1.16:', type=('build', 'run'), when='@0.8:')
    depends_on('py-scipy@1.2:', type=('build', 'run'), when='@0.8:')
    depends_on('py-scikit-learn@0.21:', type=('build', 'run'), when='@0.8:')
    depends_on('py-joblib@0.12:', type=('build', 'run'))
    depends_on('py-nibabel@2.5:', type=('build', 'run'), when='@0.8:')
    depends_on('py-pandas@0.24.0:', type=('build', 'run'), when='@0.8:')
    depends_on('py-requests@2:', type=('build', 'run'))
    depends_on('py-matplotlib@2.0:', type=('build', 'run'), when='+plotting')

    depends_on('py-numpy@1.11:', type=('build', 'run'), when='@:0.7')
    depends_on('py-scipy@0.19:', type=('build', 'run'), when='@:0.7')
    depends_on('py-scikit-learn@0.19:', type=('build', 'run'), when='@:0.7')
    depends_on('py-nibabel@2.0.2:', type=('build', 'run'), when='@:0.7')
    depends_on('py-pandas@0.18.0:', type=('build', 'run'), when='@:0.7')
