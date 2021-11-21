# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class PyOpen3d(PythonPackage):
    """Open3D: A Modern Library for 3D Data Processing."""

    homepage = "http://www.open3d.org/"
    url      = "https://github.com/isl-org/Open3D/archive/refs/tags/v0.13.0.tar.gz"

    version('0.13.0', sha256='b5994a9853f1c01e59f6d682ef0cc42c73071fd49c3e30593dc2f21ec61cf940')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@40.8:', type='build')
    depends_on('py-wheel@0.36:', type='build')
    depends_on('py-numpy@1.18:', type=('build', 'run'))

    build_directory = 'python'

    def patch(self):
        setup = FileFilter(os.path.join('python', 'setup.py'))
        setup.filter('@PYPI_PACKAGE_NAME@', 'open3d', string=True)
        setup.filter('@PROJECT_VERSION@', str(self.version), string=True)
