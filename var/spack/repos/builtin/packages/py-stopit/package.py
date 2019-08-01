# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT

# ----------------------------------------------------------------------------
#
#     spack install py-stopit
#
# You can edit this file again by typing:
#
#     spack edit py-stopit
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyStopit(PythonPackage):
    """Raise asynchronous exceptions in other threads, control the timeout of blocks or callables with two context managers and two decorators."""

    homepage = "https://pypi.org/project/stopit/"
    url      = "https://files.pythonhosted.org/packages/35/58/e8bb0b0fb05baf07bbac1450c447d753da65f9701f551dca79823ce15d50/stopit-1.1.2.tar.gz"

    version('1.1.2', sha256='f7f39c583fd92027bd9d06127b259aee7a5b7945c1f1fa56263811e1e766996d')

    depends_on('py-setuptools', type='build')

