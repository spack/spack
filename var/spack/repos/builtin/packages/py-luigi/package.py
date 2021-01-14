# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLuigi(PythonPackage):
    """Workflow mgmgt + task scheduling + dependency resolution"""

    homepage = "https://github.com/spotify/luigi"
    url      = "https://pypi.io/packages/source/l/luigi/luigi-2.8.3.tar.gz"

    version('3.0.2', sha256='b4b1ccf086586d041d7e91e68515d495c550f30e4d179d63863fea9ccdbb78eb')
    version('3.0.1', sha256='f158f4e093638bf734e2f4f08261bdba414bac7187ab69f1d6f8c95b1c408409')
    version('2.8.3', sha256='8b5c84a3c3f4df07309056d3b98348b93c054f1931b7ee22fc29e7989f645c9e')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('python@3.6:',         type=('build', 'run'), when='@3:')

    depends_on('py-setuptools', type='build')

    depends_on('py-tornado@4.0:4.99', type=('build', 'run'), when='@:2.99')
    depends_on('py-tornado@5.0:5.99', type=('build', 'run'), when='@3.0.1')
    depends_on('py-tornado@5.0:6.99', type=('build', 'run'), when='@3.0.2:')

    depends_on('py-python-daemon@:2.1', type=('build', 'run'))
    depends_on('py-python-dateutil@2.7.5:2.99', when='@2.8.3:', type=('build', 'run'))

    depends_on('py-pytest@3.3.0:', type='test')
