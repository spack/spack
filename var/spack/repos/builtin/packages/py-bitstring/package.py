# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBitstring(PythonPackage):
    """Simple construction, analysis and modification of binary data."""

    homepage = "http://pythonhosted.org/bitstring"
    url      = "https://pypi.io/packages/source/b/bitstring/bitstring-3.1.5.zip"

    version('3.1.5', '70689a282f66625d0c7c3579a13e66db')
