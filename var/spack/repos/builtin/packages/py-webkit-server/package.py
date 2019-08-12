# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWebkitServer(PythonPackage):
    """a Webkit-based, headless web client"""

    homepage = "https://github.com/niklasb/webkit-server"
    url      = "https://pypi.io/packages/source/w/webkit-server/webkit-server-1.0.tar.gz"
    git      = "https://github.com/niklasb/webkit-server.git"

    version('develop', branch='master')
    version('1.0', '8463245c2b4f0264d934c0ae20bd4654')
