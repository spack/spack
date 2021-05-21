# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumpyQuaternion(PythonPackage):
    """Add a quaternion dtype to NumPy"""

    homepage = "https://github.com/moble/quaternion"
    url      = "https://pypi.io/packages/source/n/numpy-quaternion/numpy-quaternion-2020.11.2.17.0.49.tar.gz"

    maintainers = ['moble']

    version('2020.11.2.17.0.49', sha256='f65547201fdfa41590b72cfd6ed573e1e9201ca15f19dad429efb8e70e0a4d39')
    version('2019.12.11.22.25.52', sha256='21d7bfbc08ad7ba882a05262fc67daf96e9e394fe442d1b62a4b8829259d6688')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
