# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMonai(PythonPackage):
    """AI Toolkit for Healthcare Imaging"""

    homepage = "https://monai.io/"

    url      = "https://github.com/Project-MONAI/MONAI/archive/refs/tags/0.8.1.tar.gz"

    version('0.8.1', sha256='e1227e6406cc47c23f6846f617350879ceba353915b948d917bf4308b17ea861')
    version('0.8.0', sha256='a63df7d5a680d9641c223ea090ff843a7d6f20bdb62095bd44f3b0480a4706ed')

    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('cuda', type=('build', 'run'))
