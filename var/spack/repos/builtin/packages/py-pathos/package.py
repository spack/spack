# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPathos(PythonPackage):
    """Parallel graph management and execution in heterogeneous computing """

    homepage = "https://github.com/uqfoundation/pathos"
    pypi = "pathos/pathos-0.2.3.tar.gz"

    version('0.2.5', sha256='21ae2cb1d5a76dcf57d5fe93ae8719c7339f467e246163650c08ccf35b87c846')
    version('0.2.4', sha256='610dc244b6b5c240396ae392bb6f94d7e990b0062d4032c5e9ab00b594ed8720')
    version('0.2.3', sha256='954c5b0a8b257c375e35d311c65fa62a210a3d65269195557de38418ac9f61f9')
    version('0.2.0', sha256='2f4e67e7914c95fb0cce766bab173eb2c5860ee420108fa183099557ac2e50e9')

    depends_on('python@2.6:2.8,3.1:')

    depends_on('py-setuptools@0.6:', type='build')
    depends_on('py-multiprocess@0.70.7:', type=('build', 'run'))
    depends_on('py-pox@0.2.5:', type=('build', 'run'))
    depends_on('py-ppft@1.6.4.9:', type=('build', 'run'))
    depends_on('py-dill@0.2.9:', type=('build', 'run'))

    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        if version >= Version('0.2.2'):
            url += '/pathos-{0}.tar.gz'
        else:
            url += '/pathos-{0}.zip'

        url = url.format(version)
        return url
