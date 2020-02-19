##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyDeap(PythonPackage):
    """Distributed Evolutionary Algorithms in Python"""

    homepage = "https://github.com/deap/deap"
    url = "https://pypi.io/packages/source/d/deap/deap-1.2.2.tar.gz"

    version('1.2.2', sha256='95c63e66d755ec206c80fdb2908851c0bef420ee8651ad7be4f0578e9e909bcf')

    depends_on('py-setuptools', type='build')
