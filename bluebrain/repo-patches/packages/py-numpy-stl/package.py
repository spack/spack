# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumpyStl(PythonPackage):
    """Library to make reading, writing and modifying both binary and ascii
    STL files easy"""

    homepage = "https://github.com/WoLpH/numpy-stl/"
    url = "https://pypi.io/packages/source/n/numpy-stl/numpy-stl-2.10.1.tar.gz"

    version('2.10.1', sha256='f6b529b8a8112dfe456d4f7697c7aee0aca62be5a873879306afe4b26fca963c', preferred=True)

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-pip', type='build')

    depends_on('py-numpy', type=("build", "run"))
    depends_on('py-python-utils@1.6.2:', type=("build", "run"))
