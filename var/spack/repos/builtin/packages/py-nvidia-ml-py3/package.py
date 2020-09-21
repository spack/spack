# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNvidiaMlPy3(PythonPackage):
    """Python 3 Bindings for the NVIDIA Management Library"""

    homepage = "https://github.com/nicolargo/nvidia-ml-py3"
    url      = "https://github.com/nicolargo/nvidia-ml-py3/archive/master.zip"
    git      = "https://github.com/nicolargo/nvidia-ml-py3.git"
    version('master', branch='master')

    depends_on('python', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    def install(self, spec, prefix):
        setup_py('install', '--root=/', '--prefix={0}'.format(prefix))
