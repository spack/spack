# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGreenlet(PythonPackage):
    """Lightweight in-process concurrent programming"""

    homepage = "https://github.com/python-greenlet/greenlet"
    url      = "https://pypi.io/packages/source/g/greenlet/greenlet-0.4.13.tar.gz"

    version('0.4.13', sha256='0fef83d43bf87a5196c91e73cb9772f945a4caaff91242766c5916d1dd1381e4')
