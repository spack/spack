# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGreenlet(PythonPackage):
    """Lightweight in-process concurrent programming"""

    homepage = "https://github.com/python-greenlet/greenlet"
    url      = "https://pypi.io/packages/source/g/greenlet/greenlet-0.4.13.tar.gz"

    version('0.4.13', '6e0b9dd5385f81d478451ec8ed1d62b3')
