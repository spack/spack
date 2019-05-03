# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBotocore(PythonPackage):
    """A low-level interface to a growing number of Amazon Web Services.
       The botocore package is the foundation for the AWS CLI as well
       as boto3"""

    homepage = "https://github.com/boto/botocore"
    url      = "https://pypi.io/packages/source/b/botocore/botocore-1.12.61.tar.gz"

    version('1.12.61', sha256='946c24b616cc885d490a6999026125524e85751540eb4af501673d0f5bc7eee1')

    depends_on('py-jmespath@0.7.1:0.99', type=('build', 'run'))
    depends_on('py-docutils@0.10:', type=('build', 'run'))
    depends_on('py-dateutil@2.1:2.7.0', type=('build', 'run'),
               when='^python@2.6:2.6.999')
    depends_on('py-dateutil@2.1:2.999', type=('build', 'run'),
               when='^python@2.7:2.999')
    depends_on('py-urllib3@1.20:1.25', type=('build', 'run'),
               when='^python@3.4:')
    depends_on('py-urllib3@1.20:1.23', type=('build', 'run'),
               when='^python@3.3')
    depends_on('py-urllib3@1.20:1.25', type=('build', 'run'),
               when='^python@2.7')
    depends_on('py-urllib3@1.20:1.24', type=('build', 'run'),
               when='^python@2.6')
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-nose', type='test')
    depends_on('py-mock', type='test')
    depends_on('py-tox@2.5.0:2.99', type='test')
