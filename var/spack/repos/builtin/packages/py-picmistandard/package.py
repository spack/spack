# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPicmistandard(PythonPackage):
    """Standard input format for Particle-In-Cell codes"""

    homepage = "https://picmi-standard.github.io"
    url      = "https://github.com/picmi-standard/picmi/archive/refs/tags/0.0.14.tar.gz"
    git      = "https://github.com/picmi-standard/picmi.git"

    maintainers = ['ax3l', 'dpgrote', 'RemiLehe']

    version('develop', branch='master')
    version('0.0.14', sha256='b7eefdae1c43119984226b2df358c86fdeef7495084e47b3575e3d07e790ba30')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    build_directory = 'PICMI_Python'
