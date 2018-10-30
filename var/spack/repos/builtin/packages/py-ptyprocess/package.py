# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPtyprocess(PythonPackage):
    """Run a subprocess in a pseudo terminal"""

    homepage = "https://pypi.python.org/pypi/ptyprocess"
    url      = "https://pypi.io/packages/source/p/ptyprocess/ptyprocess-0.5.1.tar.gz"

    version('0.5.1', '94e537122914cc9ec9c1eadcd36e73a1')
