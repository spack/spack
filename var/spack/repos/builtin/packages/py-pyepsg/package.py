# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyepsg(PythonPackage):
    """Provides simple access to http://epsg.io/."""

    homepage = "https://pyepsg.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/p/pyepsg/pyepsg-0.3.2.tar.gz"

    version('0.3.2', 'b0644187068a9b58378a5c58ad55b991')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests',   type=('build', 'run'))
