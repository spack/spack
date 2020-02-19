##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyArrow(PythonPackage):
    """Better dates & times for Python"""

    homepage = "https://arrow.readthedocs.org"
    url      = "https://github.com/crsmithdev/arrow/archive/0.10.0.tar.gz"

    version('0.10.0', sha256='4ed4f6c86e9d3e75a1f77af13d6f5a08f6891ab5c815b20f1f7b7c88ffcad118')

    depends_on('py-backports-functools-lru-cache', when='^python@:2.8')
    depends_on('py-dateutil')
    depends_on('py-setuptools', type='build')
