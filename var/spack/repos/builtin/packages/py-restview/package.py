# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRestview(PythonPackage):
    """A viewer for ReStructuredText documents that renders them on the fly."""

    homepage = "https://mg.pov.lt/restview/"
    pypi = "restview/restview-2.6.1.tar.gz"

    version('2.9.2', sha256='790097eb587c0465126dde73ca06c7a22c5007ce1be4a1de449a13c0767b32dc')
    version('2.9.1', sha256='de87c84f19526bd4a76505f6d40b51b7bb03ca43b6067c93f82f1c7237ac9e84')
    version('2.9.0', sha256='d33748440af00ba4434c13c095ccfbde6e3237c3bd661198cf74066c0c027e7a')
    version('2.8.1', sha256='45320b4e52945d23b3f1aeacc7ff97a3b798204fe625f8b81ed5322326d5bcd1')
    version('2.8.0', sha256='5f6f1523228eab3269f59dd03ac560f7d370cd81df6fdbcb4914b5e6bd896a11')
    version('2.7.0', sha256='e7842100f3de179c68cfe7c2cf56c61509cd6068bc6dd58ab42c0ade5d5f97ec')
    version('2.6.1', sha256='14d261ee0edf30e0ebc1eb320428ef4898e97422b00337863556966b851fb5af')

    depends_on('python@2.7:2.8,3.3:3.5')
    depends_on('py-setuptools', type='build')
    depends_on('py-docutils@0.13.1:', type=('build', 'run'))
    depends_on('py-readme-renderer', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
