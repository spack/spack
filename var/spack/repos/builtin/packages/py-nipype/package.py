# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNipype(PythonPackage):
    """Neuroimaging in Python: Pipelines and Interfaces."""

    homepage = "https://github.com/nipy/nipype"
    pypi     = "nipype/nipype-1.6.0.tar.gz"

    version('1.7.0', sha256='e689fe2e5049598c9cd3708e8df1cac732fa1a88696f283e3bc0a70fecb8ab51')
    version('1.6.1', sha256='8428cfc633d8e3b8c5650e241e9eedcf637b7969bcd40f3423334d4c6b0992b5')
    version('1.6.0', sha256='bc56ce63f74c9a9a23c6edeaf77631377e8ad2bea928c898cc89527a47f101cf')
    version('1.4.2', sha256='069dcbb0217f13af6ee5a7f1e58424b9061290a3e10d7027d73bf44e26f820db')

    depends_on('python@3.6:', when='@1.5:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-click@6.6:', type=('build', 'run'))
    depends_on('py-networkx@2:', when='@1.6:', type=('build', 'run'))
    depends_on('py-networkx@1.9:', type=('build', 'run'))
    depends_on('py-nibabel@2.1:', type=('build', 'run'))
    depends_on('py-numpy@1.15.3:', when='^python@3.7:', type=('build', 'run'))
    depends_on('py-numpy@1.13:', when='@1.5: ^python@:3.6', type=('build', 'run'))
    depends_on('py-numpy@1.12:', when='^python@:3.6', type=('build', 'run'))
    depends_on('py-packaging', type=('build', 'run'))
    depends_on('py-prov@1.5.2:', type=('build', 'run'))
    depends_on('py-pydot@1.2.3:', type=('build', 'run'))
    depends_on('py-pydotplus', when='@:1.5', type=('build', 'run'))
    depends_on('py-python-dateutil@2.2:', type=('build', 'run'))
    depends_on('py-rdflib@5:', when='@1.5:', type=('build', 'run'))
    depends_on('py-scipy@0.14:', type=('build', 'run'))
    depends_on('py-simplejson@3.8:', type=('build', 'run'))
    depends_on('py-traits@4.6:4,5.1:', type=('build', 'run'))
    depends_on('py-filelock@3:', type=('build', 'run'))
    depends_on('py-etelemetry@0.2:', when='@1.5:', type=('build', 'run'))
    depends_on('py-etelemetry', type=('build', 'run'))
