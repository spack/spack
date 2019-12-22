# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBoto3(PythonPackage):
    """The AWS SDK for Python."""

    homepage = "https://github.com/boto/boto3"
    url      = "https://pypi.io/packages/source/b/boto3/boto3-1.10.38.tar.gz"

    import_modules = [
        'boto3', 'boto3.s3', 'boto3.resources', 'boto3.dynamodb',
        'boto3.docs', 'boto3.ec2'
    ]

    version('1.10.38', sha256='6cdb063b2ae5ac7b93ded6b6b17e3da1325b32232d5ff56e6800018d4786bba6')
    version('1.9.169', sha256='9d8bd0ca309b01265793b7e8d7b88c1df439737d77c8725988f0277bbf58d169')

    depends_on('py-setuptools', type='build')
    depends_on('py-botocore@1.13.38:1.13.999',  when='@1.10.38', type=('build', 'run'))
    depends_on('py-botocore@1.12.169:1.12.999', when='@1.9.169', type=('build', 'run'))
    depends_on('py-jmespath@0.7.1:0.999', type=('build', 'run'))
    depends_on('py-s3transfer@0.2.0:0.2.999', type=('build', 'run'))
