# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyPyproj(PythonPackage):
    """Python interface to PROJ (cartographic projections and
    coordinate transformations library)."""

    homepage = "https://github.com/pyproj4/pyproj"
    pypi = "pyproj/pyproj-2.2.0.tar.gz"
    git      = "https://github.com/pyproj4/pyproj.git"

    maintainers = ['citibeth', 'adamjstewart']

    version('3.1.0',   sha256='67b94f4e694ae33fc90dfb7da0e6b5ed5f671dd0acc2f6cf46e9c39d56e16e1a')
    version('3.0.1',   sha256='bfbac35490dd17f706700673506eeb8170f8a2a63fb5878171d4e6eef242d141')
    version('3.0.0',   sha256='539e320d06e5441edadad2e2ab276e1877445eca384fc1c056b5501453d433c2')
    version('2.6.1',   sha256='52556f245f1112f121091937b47738d1fbcbd0f13be6fb32689de31ab0975d24')
    version('2.6.0',   sha256='977542d2f8cf2981cf3ad72cedfebcd6ac56977c7aa830d9b49fa7888b56e83d')
    version('2.2.0',   sha256='0a4f793cc93539c2292638c498e24422a2ec4b25cb47545addea07724b2a56e5')
    version('2.1.3',   sha256='99c52788b01a7bb9a88024bf4d40965c0a66a93d654600b5deacf644775f424d')
    version('1.9.6',   sha256='e0c02b1554b20c710d16d673817b2a89ff94738b0b537aead8ecb2edc4c4487b', deprecated=True)
    version('1.9.5.1', sha256='53fa54c8fa8a1dfcd6af4bf09ce1aae5d4d949da63b90570ac5ec849efaf3ea8', deprecated=True)

    # In setup.cfg and setup.py
    depends_on('python@3.7:', when='@3.1:', type=('build', 'link', 'run'))
    depends_on('python@3.6:', when='@3.0:', type=('build', 'link', 'run'))
    depends_on('python@3.5:', when='@2.3:', type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@2.2:', type=('build', 'link', 'run'))
    depends_on('python@2.6:2.8,3.3:', type=('build', 'link', 'run'))

    # In setup.py
    # https://pyproj4.github.io/pyproj/stable/installation.html#installing-from-source
    depends_on('proj')
    depends_on('proj@7.2:', when='@3.0.1:')
    depends_on('proj@7.2.0:7.2',  when='@3.0.0')
    depends_on('proj@6.2:7.0', when='@2.4:2.6')
    depends_on('proj@6.1:7.0', when='@2.2:2.3')
    depends_on('proj@6.0:6', when='@2.0:2.1')
    depends_on('proj@:5.2', when='@:1.9')

    # In setup.py
    depends_on('py-setuptools', type='build')
    depends_on('py-certifi', when='@3.0:', type=('build', 'run'))
    depends_on('py-aenum', when='@2.2.0:2.2 ^python@:3.5', type=('build', 'run'))

    # In pyproject.toml
    depends_on('py-cython@0.28.4:', when='@2.0:')

    def setup_build_environment(self, env):
        # https://pyproj4.github.io/pyproj/stable/installation.html#pyproj-build-environment-variables
        env.set('PROJ_VERSION', self.spec['proj'].version)
        env.set('PROJ_DIR', self.spec['proj'].prefix)
        env.set('PROJ_LIBDIR', self.spec['proj'].libs.directories[0])
        env.set('PROJ_INCDIR', self.spec['proj'].headers.directories[0])
