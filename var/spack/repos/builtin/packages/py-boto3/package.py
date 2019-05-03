# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBoto3(PythonPackage):
    """Boto3 is the Amazon Web Services (AWS) Software Development
       Kit (SDK) for Python, which allows Python developers to write
       software that makes use of services like Amazon S3 and Amazon EC2"""

    homepage = "https://github.com/boto/boto3"
    url      = "https://pypi.io/packages/source/b/boto3/boto3-1.9.61.tar.gz"

    version('1.9.61', sha256='cd606ce834df58c3401bbe44a4a00de972094da14bbc1c00c7238707f1f03fe0')

    depends_on('py-botocore@1.12.61:1.12.99', type=('build', 'run'))
    depends_on('py-futures', when='^python@:2.99', type=('build', 'run'))
    depends_on('py-jmespath@0.7.1:0.99', type=('build', 'run'))
    depends_on('py-s3transfer@0.1.10:0.1.99', type=('build', 'run'))
    depends_on('py-urllib3', type=('build', 'run'))
