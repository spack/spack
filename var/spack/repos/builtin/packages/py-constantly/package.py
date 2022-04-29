# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyConstantly(PythonPackage):
    """Symbolic constants in Python"""

    homepage = "https://github.com/twisted/constantly"
    pypi     = "constantly/constantly-15.1.0.tar.gz"

    version('15.1.0', sha256='586372eb92059873e29eba4f9dec8381541b4d3834660707faf8ba59146dfc35')

    depends_on('py-setuptools', type='build')
