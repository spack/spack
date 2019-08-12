# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySh(PythonPackage):
    """Python subprocess interface"""

    homepage = "https://github.com/amoffat/sh"
    url      = "https://pypi.io/packages/source/s/sh/sh-1.12.9.tar.gz"

    version('1.12.9', 'ddc128a8d943d25afa6e01af11e0063b')
    version('1.11',   '7af8df6c92d29ff927b6db0146bddec3')

    depends_on('py-setuptools', type='build')
