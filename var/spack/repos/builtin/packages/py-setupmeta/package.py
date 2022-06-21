# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetupmeta(PythonPackage):
    """Simplify your setup.py."""

    homepage = "https://github.com/codrsquad/setupmeta"
    pypi = "setupmeta/setupmeta-3.3.0.tar.gz"

    version('3.3.0', sha256='32914af4eeffb8bf1bd45057254d9dff4d16cb7ae857141e07698f7ac19dc960')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
