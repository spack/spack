# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTerminado(PythonPackage):
    """Terminals served to term.js using Tornado websockets"""

    homepage = "https://pypi.python.org/pypi/terminado"
    url      = "https://pypi.io/packages/source/t/terminado/terminado-0.6.tar.gz"

    version('0.8.1', '616515f562939e979b67c72b667afba9')
    version('0.6', '5b6c65da27fe1ed07a9f80f0588cdaba')

    depends_on('py-tornado@4:', type=('build', 'run'))
    depends_on('py-ptyprocess', type=('build', 'run'))
