# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPicmistandard(PythonPackage):
    """Standard input format for Particle-In-Cell codes"""

    homepage = "https://picmi-standard.github.io"
    git      = "https://github.com/picmi-standard/picmi.git"
    pypi     = 'picmistandard/picmistandard-0.0.18.tar.gz'

    maintainers = ['ax3l', 'dpgrote', 'RemiLehe']

    version('develop', branch='master')
    version('0.0.19', sha256='4b7ba1330964fbfd515e8ea2219966957c1386e0896b92d36bd9e134afb02f5a')
    version('0.0.18', sha256='68c208c0c54b4786e133bb13eef0dd4824998da4906285987ddee84e6d195e71')
    # 0.15 - 0.17 have broken install logic: missing requirements.txt on pypi
    version('0.0.16', sha256='b7eefdae1c43119984226b2df358c86fdeef7495084e47b3575e3d07e790ba30',
            url='https://github.com/picmi-standard/picmi/archive/refs/tags/0.0.14.tar.gz')
    version('0.0.14', sha256='8f83b25b281fc0309a0c4f75c7605afd5fa0ef4df3b3ac115069478c119bc8c3')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy@1.15:1', type=('build', 'run'))
    depends_on('py-scipy@1.5:1', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    @property
    def build_directory(self):
        if self.spec.satisfies('@develop') or self.spec.satisfies('@0.0.16'):
            return 'PICMI_Python'
        else:
            return './'
