# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyYte(PythonPackage):
    """YTE is a template engine for YAML format that utilizes the YAML
    structure in combination with Python expressions for enabling to
    dynamically build YAML documents."""

    homepage = "https://github.com/koesterlab/yte"
    pypi = "yte/yte-1.2.0.tar.gz"
    maintainers = ['marcusboden']
    version('1.2.0', '0368f220bb96fb3290bbd5a90e3d218af483d0d3e5abf9b08b24e29b150f151e')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-poetry-core@1:', type='build')

    depends_on('py-plac@1.3.4:1', type=('build', 'run'))
    depends_on('py-pyyaml@6.0:6', type=('build', 'run'))
