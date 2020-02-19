##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyGcovr(PythonPackage):
    """generate code coverage reports with gcc/gcov"""

    homepage = "https://gcovr.com/"
    url      = "https://github.com/gcovr/gcovr/archive/4.1.tar.gz"

    version('4.1', sha256='1ad8042fd4dc4c355fd7e605d395eefa2a59b1677dfdc308e0ef00083e8b37ee')

    depends_on('py-setuptools', type='build')
    depends_on('py-jinja2', type=('build', 'run'))
