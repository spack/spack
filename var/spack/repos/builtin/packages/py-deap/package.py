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

    depends_on('py-setuptools', type='build')

