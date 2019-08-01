# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT

# ----------------------------------------------------------------------------
#
#     spack install py-deap
#
# You can edit this file again by typing:
#
#     spack edit py-deap
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyDeap(PythonPackage):
    """Distributed Evolutionary Algorithms in Python."""

    homepage = "http://deap.readthedocs.org/"
    url      = "https://github.com/DEAP/deap/archive/1.2.2.tar.gz"

    version('1.2.2', sha256='7a1940201962574ec7eba34981f9db3541631b391d5f1cead80b6d7af29aa7da')
    version('1.2.1', sha256='47374b34b05e8dbc20ef36fe4e712391c9b24981c49ecc80331e49a8bebc8408')
    version('1.0.1', sha256='ab5d4de37a21609853cc1f89b1c1be96decce25248e2436f819ed34d8c4487a7')

    depends_on('py-setuptools', type='build')

