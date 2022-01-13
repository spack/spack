# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyOpencvPython(PythonPackage):
    """Pre-built CPU-only OpenCV packages for Python."""

    homepage = "https://pypi.org/project/opencv-python"
    url      = "https://files.pythonhosted.org/packages/01/9b/be08992293fb21faf35ab98e06924d7407fcfca89d89c5de65442631556a/opencv-python-4.5.3.56.tar.gz"

    version('4.5.3.56', sha256='3c001d3feec7f3140f1fb78dfc52ca28122db8240826882d175a208a89d2731b')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('cmake', type='build')
    depends_on('py-numpy', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-scikit-build', type='build')
