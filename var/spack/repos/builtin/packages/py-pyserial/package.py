# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyserial(PythonPackage):
    """Python Serial Port Extension"""

    homepage = "https://github.com/pyserial/pyserial"
    url      = "https://pypi.io/packages/source/p/pyserial/pyserial-3.1.1.tar.gz"

    version('3.1.1', '2f72100de3e410b36d575e12e82e9d27')

    depends_on('py-setuptools', type='build')
