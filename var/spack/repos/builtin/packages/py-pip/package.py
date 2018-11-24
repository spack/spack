# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPip(PythonPackage):
    """The PyPA recommended tool for installing Python packages."""

    homepage = "https://pypi.python.org/pypi/pip"
    url      = "https://pypi.io/packages/source/p/pip/pip-9.0.1.tar.gz"

    version('18.1', sha256='c0a292bd977ef590379a3f05d7b7f65135487b67470f6281289a94e015650ea1')
    version('10.0.1', '83a177756e2c801d0b3a6f7b0d4f3f7e')
    version('9.0.1', '35f01da33009719497f01a4ba69d63c9')

    depends_on('python@2.6:2.8,3.3:')

    # Most Python packages only require setuptools as a build dependency.
    # However, pip requires setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
