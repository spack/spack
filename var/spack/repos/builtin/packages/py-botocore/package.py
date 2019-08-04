# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBotocore(PythonPackage):
    """Low-level, data-driven core of boto 3."""

    homepage = "https://github.com/boto/botocore"
    url      = "https://pypi.io/packages/source/b/botocore/botocore-1.12.169.tar.gz"

    import_modules = ['botocore']

    version('1.12.169', sha256='25b44c3253b5ed1c9093efb57ffca440c5099a2d62fa793e8b6c52e72f54b01e')

    depends_on('py-setuptools', type='build')
    depends_on('py-jmespath@0.7.1:0.999', type=('build', 'run'))
    depends_on('py-docutils@0.10:', type=('build', 'run'))
    depends_on('py-ordereddict@1.1', type=('build', 'run'), when='^python@2.6.0:2.6.999')
    depends_on('py-simplejson@3.3.0', type=('build', 'run'), when='^python@2.6.0:2.6.999')
    depends_on('py-python-dateutil@2.1:2.999', type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:2.6', type=('build', 'run'), when='^python@2.6.0:2.6.999')
    depends_on('py-urllib3@1.20:1.25', type=('build', 'run'))
    depends_on('py-urllib3@1.20:1.23', type=('build', 'run'), when='^python@2.6.0:2.6.999')
    depends_on('py-urllib3@1.20:1.22', type=('build', 'run'), when='^python@3.3.0:3.3.999')
    depends_on('py-mock', type='test')
    depends_on('py-nose', type='test')
