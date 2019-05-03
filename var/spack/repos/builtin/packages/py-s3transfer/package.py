# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyS3transfer(PythonPackage):
    """S3transfer is a Python library for managing Amazon S3 transfers"""

    homepage = "git://github.com/boto/s3transfer"
    url      = "https://pypi.io/packages/source/s/s3transfer/s3transfer-0.1.13.tar.gz"

    version('0.1.13', sha256='90dc18e028989c609146e241ea153250be451e05ecc0c2832565231dacdf59c1')

    depends_on('py-botocore@1.3.0:1.99', type=('build', 'run'))
    depends_on('py-futures@2.2.0:3.999', when='^python@:2.99', type=('build', 'run'))
    depends_on('py-nose', type='test')
    depends_on('py-mock', type='test')
    depends_on('py-coverage', type='test')
