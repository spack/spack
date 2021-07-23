
# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOmegaconf(PythonPackage):
    """A hierarchical configuration system, with support for merging configurations from
    multiple sources (YAML config files, dataclasses/objects and CLI arguments)
    providing a consistent API regardless of how the configuration was created.
    """

    homepage = "https://github.com/omry/omegaconf"
    pypi     = "omegaconf/omegaconf-2.1.0.tar.gz"

    maintainers = ['calebrob6']

    version('2.1.0', sha256='a08aec03a63c66449b550b85d70238f4dee9c6c4a0541d6a98845dcfeb12439d')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-antlr4-python3-runtime@4.8', type=('build', 'run'))
    depends_on('py-pyyaml@5.1.0:', type=('build', 'run'))
