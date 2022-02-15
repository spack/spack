# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTenacity(PythonPackage):
    """Retrying library for Python"""

    homepage = "https://github.com/jd/tenacity"
    pypi     = "tenacity/tenacity-6.3.1.tar.gz"

    version('6.3.1', sha256='e14d191fb0a309b563904bbc336582efe2037de437e543b38da749769b544d7f')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))

    depends_on('py-setuptools',     type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-six@1.9.0:', type=('build', 'run'))

    depends_on('py-futures@3.0:',    when='^python@:2', type=('build', 'run'))
    depends_on('py-monotonic@0.6:',  when='^python@:2', type=('build', 'run'))
    depends_on('py-typing@3.7.4.1:', when='^python@:2', type=('build', 'run'))
