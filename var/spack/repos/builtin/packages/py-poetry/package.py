# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetry(PythonPackage):
    """Python dependency management and packaging made easy."""

    homepage = "https://python-poetry.org/"
    pypi     = "poetry/poetry-1.1.12.tar.gz"

    version('1.1.13', sha256='b905ed610085f568aa61574e0e09260c02bff9eae12ff672af39e9f399357ac4')
    version('1.1.12', sha256='5c66e2357fe37b552462a88b7d31bfa2ed8e84172208becd666933c776252567')

    depends_on('python@2.7,3.5:3', type=('build', 'run'))
    depends_on('py-poetry-core@1.0.7:1.0', type=('build', 'run'))
    depends_on('py-cleo@0.8.1:0.8', type=('build', 'run'))
    depends_on('py-clikit@0.6.2:0.6', type=('build', 'run'))
    depends_on('py-crashtest@0.3.0:0.3', when='^python@3.6:3', type=('build', 'run'))
    depends_on('py-requests@2.18:2', type=('build', 'run'))
    depends_on('py-cachy@0.3.0:0.3', type=('build', 'run'))
    depends_on('py-requests-toolbelt@0.9.1:0.9', type=('build', 'run'))
    depends_on('py-cachecontrol@0.12.4:0.12+filecache', when='^python@:3.5', type=('build', 'run'))
    depends_on('py-cachecontrol@0.12.9:0.12+filecache', when='^python@3.6:3', type=('build', 'run'))
    depends_on('py-pkginfo@1.4:1', type=('build', 'run'))
    depends_on('py-html5lib@1.0:1', type=('build', 'run'))
    depends_on('py-shellingham@1.1:1', type=('build', 'run'))
    depends_on('py-tomlkit@0.7:0', type=('build', 'run'))
    depends_on('py-pexpect@4.7:4', type=('build', 'run'))
    depends_on('py-packaging@20.4:20', type=('build', 'run'))
    depends_on('py-virtualenv@20.0.26:20', type=('build', 'run'))
    depends_on('py-typing@3.6:3', when='^python@2.7', type=('build', 'run'))
    depends_on('py-pathlib2@2.3:2', when='^python@2.7', type=('build', 'run'))
    depends_on('py-futures@3.3:3', when='^python@2.7', type=('build', 'run'))
    depends_on('py-glob2@0.6.0:0.6', when='^python@2.7', type=('build', 'run'))
    depends_on('py-functools32@3.2.3:3', when='^python@2.7', type=('build', 'run'))
    depends_on('py-keyring@18.0.1:18', when='^python@2.7', type=('build', 'run'))
    depends_on('py-keyring@20.0.1:20', when='^python@3.5', type=('build', 'run'))
    depends_on('py-keyring@21.2.0:21', when='@1.1.12 ^python@3.6:3', type=('build', 'run'))
    depends_on('py-keyring@21.2.0:', when='@1.1.13 ^python@3.6:3', type=('build', 'run'))
    depends_on('py-subprocess32@3.5:3', when='^python@2.7', type=('build', 'run'))
    depends_on('py-importlib-metadata@1.6:1', when='^python@:3.7', type=('build', 'run'))
