# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNodeenv(PythonPackage):
    """Node.js virtual environment"""

    homepage = "https://github.com/ekalinin/nodeenv"
    pypi = "nodeenv/nodeenv-1.3.3.tar.gz"

    version('1.5.0', sha256='ab45090ae383b716c4ef89e690c41ff8c2b257b85b309f01f3654df3d084bd7c')
    version('1.4.0', sha256='26941644654d8dd5378720e38f62a3bac5f9240811fb3b8913d2663a17baa91c')
    version('1.3.5', sha256='7389d06a7ea50c80ca51eda1b185db7b9ec38af1304d12d8b8299d6218486e91')
    version('1.3.4', sha256='ff860d311cb9cee1a74e7056b6526436eceb2d5177f584b128eca3530849c1ec')
    version('1.3.3', sha256='ad8259494cf1c9034539f6cced78a1da4840a4b157e23640bc4a0c0546b0cb7a')

    depends_on('py-setuptools', type='build')
