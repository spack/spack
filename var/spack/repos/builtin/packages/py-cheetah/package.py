# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCheetah(PythonPackage):
    """Cheetah is a template engine and code generation tool."""

    pypi = "Cheetah3/Cheetah3-3.2.6.tar.gz"

    version('3.2.6', sha256='f1c2b693cdcac2ded2823d363f8459ae785261e61c128d68464c8781dba0466b')
    version('2.3.0', sha256='2a32d7f7f70be98c2d57aa581f979bc799d4bf17d09fc0e7d77280501edf3e53')

    depends_on('py-setuptools', type='build')
    depends_on('py-markdown@2.0.1:', type=('build', 'run'))
