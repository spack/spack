# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNilearn(PythonPackage):
    """Statistical learning for neuroimaging in Python."""

    homepage = "https://nilearn.github.io/"
    pypi     = "nilearn/nilearn-0.7.1.tar.gz"

    version('0.8.1', sha256='a0489940855130f35bbc4cac0750479a6f82025215ea7b1d778faca064219298')
    version('0.8.0', sha256='f2d3dc81005f829f3a183efa6c90d698ea6818c06264d2e3f03e805c4340febb')
    version('0.7.1', sha256='8b1409a5e1f0f6d1a1f02555c2f11115a2364f45f1e57bcb5fb3c9ea11f346fa')
    version('0.6.2', sha256='cfc6cfda59a6f4247189f8ccf92e364de450460a15c0ec21bdb857c420dd198c')
    version('0.4.2', sha256='5049363eb6da2e7c35589477dfc79bf69929ca66de2d7ed2e9dc07acf78636f4')

    depends_on('python@3.6:', when='@0.8:', type=('build', 'run'))
    depends_on('python@3.5:', when='@0.6:', type=('build', 'run'))
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    variant('plotting', default=False, description='Enable plotting functionalities')

    depends_on('py-numpy@1.16:', when='@0.8:', type=('build', 'run'))
    depends_on('py-numpy@1.11:', when='@0.5:', type=('build', 'run'))
    depends_on('py-numpy@1.6.1:', type=('build', 'run'))
    depends_on('py-scipy@1.2:', when='@0.8:', type=('build', 'run'))
    depends_on('py-scipy@0.19:', when='@0.6:', type=('build', 'run'))
    depends_on('py-scipy@0.17:', when='@0.5:', type=('build', 'run'))
    depends_on('py-scipy@0.14:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.21:', when='@0.8:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.19:', when='@0.7:', type=('build', 'run'))
    # sklearn.linear_model.base was deprecated in py-scikit.learn@0.24
    depends_on('py-scikit-learn@0.19:0.23', when='@0.6.0:0.6', type=('build', 'run'))
    # older py-nilearn versions use import sklearn.external.joblib which was
    # deprecated in py-scikit-learn@0.23:
    depends_on('py-scikit-learn@0.15:0.22', when='@:0.5', type=('build', 'run'))
    depends_on('py-joblib@0.12:', when='@0.7:', type=('build', 'run'))
    depends_on('py-joblib@0.11:', when='@0.6:', type=('build', 'run'))
    depends_on('py-nibabel@2.5:', when='@0.8:', type=('build', 'run'))
    depends_on('py-nibabel@2.0.2:', type=('build', 'run'))
    depends_on('py-pandas@0.24.0:', when='@0.8:', type=('build', 'run'))
    depends_on('py-pandas@0.18.0:', when='@0.7:', type=('build', 'run'))
    depends_on('py-requests@2:', when='@0.7:', type=('build', 'run'))

    depends_on('py-matplotlib@2.0:', when='@0.6: +plotting', type=('build', 'run'))
    # older py-nilearn versions use matplotlib.cm.revcmap which was deprecated
    # in py-matplotlib@3.4:
    depends_on('py-matplotlib@1.1.1:3.3', when='@:0.6 +plotting', type=('build', 'run'))

    @property
    def import_modules(self):
        modules = [
            'nilearn',
            'nilearn.connectome',
            'nilearn.datasets',
            'nilearn.decoding',
            'nilearn.decomposition',
            'nilearn.image',
            'nilearn.input_data',
            'nilearn.masking',
            'nilearn.mass_univariate',
            'nilearn.regions',
            'nilearn.signal',
            'nilearn.surface',
        ]

        if self.spec.satisfies('@0.6:'):
            modules.append('nilearn.externals')

        if self.spec.satisfies('@0.7:'):
            modules.append('nilearn.glm')

        if '+plotting' in self.spec:
            modules.append('nilearn.plotting')
            if self.spec.satisfies('@0.7:'):
                modules.append('nilearn.reporting')

        return modules
