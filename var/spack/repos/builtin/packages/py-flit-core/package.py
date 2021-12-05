# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlitCore(PythonPackage):
    """Distribution-building parts of Flit."""

    homepage = "https://github.com/takluyver/flit"
    pypi = "flit-core/flit_core-3.3.0.tar.gz"
    maintainers = ['takluyver']

    version('3.5.1', sha256='3083720351a6cb00e0634a1ec0e26eae7b273174c3c6c03d5b597a14203b282e')
    version('3.3.0', sha256='b1404accffd6504b5f24eeca9ec5d3c877f828d16825348ba81515fa084bd5f0')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-wheel', type='build')
    depends_on('py-tomli', type='run')
