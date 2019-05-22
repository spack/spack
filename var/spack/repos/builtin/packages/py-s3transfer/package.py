# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyS3transfer(PythonPackage):
    """S3transfer is a Python library for managing Amazon S3 transfers"""

    homepage = "https://github.com/boto/s3transfer"
    url      = "https://pypi.io/packages/source/s/s3transfer/s3transfer-0.2.0.tar.gz"

    version('0.2.0', sha256='f23d5cb7d862b104401d9021fc82e5fa0e0cf57b7660a1331425aab0c691d021')
    version('0.1.13', sha256='90dc18e028989c609146e241ea153250be451e05ecc0c2832565231dacdf59c1')

    depends_on('py-setuptools', type='build')
    depends_on('py-botocore@1.3.0:1.99', type=('build', 'run'),
               when='@0.1.13')
    depends_on('py-botocore@1.12.36:1.99', type=('build', 'run'),
               when='@0.2:')
    depends_on('py-futures@2.2.0:3.999', when='^python@:2.99',
               type=('build', 'run'))
    depends_on('py-nose', type='test')
    depends_on('py-mock', type='test')
