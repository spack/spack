# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyClick(PythonPackage):
    """A simple wrapper around optparse for powerful command line utilities."""

    homepage = "http://github.com/mitsuhiko/click"
    url = "https://pypi.io/packages/source/c/click/click-6.6.tar.gz"

    version('6.6', 'd0b09582123605220ad6977175f3e51d')

    depends_on('py-setuptools', type='build')
