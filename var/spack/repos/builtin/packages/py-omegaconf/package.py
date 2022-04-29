
# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyOmegaconf(PythonPackage):
    """A hierarchical configuration system, with support for merging configurations from
    multiple sources (YAML config files, dataclasses/objects and CLI arguments)
    providing a consistent API regardless of how the configuration was created.
    """

    homepage = "https://github.com/omry/omegaconf"
    url      = 'https://github.com/omry/omegaconf/archive/refs/tags/v2.1.0.tar.gz'

    maintainers = ['calebrob6']

    version('2.1.0', sha256='0168f962822b7059c7553c4346541596ea48c0b542628d41a348a12eeaf971ff')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-antlr4-python3-runtime@4.8', type=('build', 'run'))
    depends_on('py-pyyaml@5.1.0:', type=('build', 'run'))
    depends_on('py-dataclasses', when='^python@:3.6', type=('build', 'run'))
    depends_on('java', type='build')
