# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeepsig(PythonPackage):
    """deep-significance: Easy and Better Significance Testing for Deep Neural
    Networks"""

    homepage = "https://github.com/Kaleidophon/deep-significance"
    pypi     = "deepsig/deepsig-1.2.0.tar.gz"
    git      = "https://github.com/Kaleidophon/deep-significance.git"

    # The tarball for pypi is missing files using github
    version('1.2.0', url='https://github.com/Kaleidophon/deep-significance/archive/refs/tags/v1.2.0.zip',
            sha256='4fc5d572d1bec91849daacdbba5722bd216e8398c1a8dc362d7671ff5d16548f')

    depends_on('python@3.5.3:',         type=('build', 'run'))
    depends_on('py-setuptools',         type='build')
    depends_on('py-numpy@1.19.5',       type=('build', 'run'))
    depends_on('py-scipy@1.6.0',        type=('build', 'run'))
    depends_on('py-tqdm@4.59.0',        type=('build', 'run'))
    depends_on('py-joblib@1.0.1',       type=('build', 'run'))
    depends_on('py-pandas@1.3.3',       type=('build', 'run'))
    depends_on('py-dill@0.3.4',         type=('build', 'run'))
