# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyS3transfer(PythonPackage):
    """S3transfer is a Python library for managing Amazon S3 transfers."""

    homepage = "https://github.com/boto/s3transfer"
    pypi = "s3transfer/s3transfer-0.2.1.tar.gz"

    depends_on('python@3.6:', when='@0.5.0', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.6:', when='@0.4.2', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@0.3.4', type=('build', 'run'))

    version('0.5.0', sha256='50ed823e1dc5868ad40c8dc92072f757aa0e653a192845c94a3b676f4a62da4c')
    version('0.4.2', sha256='cb022f4b16551edebbb31a377d3f09600dbada7363d8c5db7976e7f47732e1b2')
    version('0.3.4', sha256='7fdddb4f22275cf1d32129e21f056337fd2a80b6ccef1664528145b72c49e6d2')
    version('0.2.1', sha256='6efc926738a3cd576c2a79725fed9afde92378aa5c6a957e3af010cb019fac9d')

    depends_on('py-setuptools', type='build')
    depends_on('py-botocore@1.12.36:1', type=('build', 'run'))
    depends_on('py-futures@2.2:3', type=('build', 'run'), when='^python@:2')
