# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScinum(PythonPackage):
    """Scientific numbers with multiple uncertainties and
       correlation-aware, gaussian propagation and numpy"""

    homepage = "https://github.com/riga/scinum"
    pypi     = "scinum/scinum-1.2.0.tar.gz"

    version('1.2.0', sha256='31802d9b580f3a89c0876f34432851bc4def9cb2844d6f3c8e044480f2dd2f91')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
