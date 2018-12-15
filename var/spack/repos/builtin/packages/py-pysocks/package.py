# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPysocks(PythonPackage):
    """A Python SOCKS client module."""

    homepage = "https://github.com/Anorov/PySocks"
    url      = "https://pypi.io/packages/source/P/PySocks/PySocks-1.6.6.tar.gz"

    version('1.6.6', '571f4c23982fa86bf0e7a441f1b6c881')
    version('1.5.7', '68f4ad7a8d4fa725656ae3e9dd142d29')
