# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCheetah3(PythonPackage):
    """Cheetah is a template engine and code generation tool."""

    homepage = "https://pypi.python.org/pypi/Cheetah3/"
    url      = "https://pypi.io/packages/source/C/Cheetah3/Cheetah3-3.2.4.tar.gz"

    version('3.2.4', sha256='caabb9c22961a3413ac85cd1e5525ec9ca80daeba6555f4f60802b6c256e252b')

    depends_on('py-setuptools', type=('build'))
