# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCheetah(PythonPackage):
    """Cheetah is a template engine and code generation tool."""

    homepage = "https://pypi.python.org/pypi/Cheetah/2.4.4"
    url      = "https://pypi.io/packages/source/C/Cheetah/Cheetah-2.3.0.tar.gz"

    version('2.3.0', 'e28ffef7f5c1660d66196639f162d9ce')
