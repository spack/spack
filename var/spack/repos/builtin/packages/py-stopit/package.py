# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
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

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://pypi.org/project/stopit/"
    url      = "https://files.pythonhosted.org/packages/35/58/e8bb0b0fb05baf07bbac1450c447d753da65f9701f551dca79823ce15d50/stopit-1.1.2.tar.gz"

    version('1.1.2', sha256='f7f39c583fd92027bd9d06127b259aee7a5b7945c1f1fa56263811e1e766996d')

    depends_on('py-setuptools', type='build')

