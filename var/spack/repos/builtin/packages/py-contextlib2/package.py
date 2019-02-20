# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyContextlib2(PythonPackage):
    """Backports and enhancements for the contextlib module"""

    homepage = "http://contextlib2.readthedocs.org/"
    url      = "https://files.pythonhosted.org/packages/6e/db/41233498c210b03ab8b072c8ee49b1cd63b3b0c76f8ea0a0e5d02df06898/contextlib2-0.5.5.tar.gz"

    version('0.5.5', sha256='509f9419ee91cdd00ba34443217d5ca51f5a364a404e1dce9e8979cea969ca48')
