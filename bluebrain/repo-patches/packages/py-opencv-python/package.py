# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyOpencvPython(PythonPackage):
    """Pre-built CPU-only OpenCV packages for Python."""

    pypi = "opencv-python/opencv_python-4.6.0.66.tar.gz"

    version('4.6.0.66', sha256='c5bfae41ad4031e66bb10ec4a0a2ffd3e514d092652781e8b1ac98d1b59f1158')
    version('4.5.3.56', sha256='3c001d3feec7f3140f1fb78dfc52ca28122db8240826882d175a208a89d2731b')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('cmake', type='build')
    depends_on('py-numpy', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-scikit-build', type='build')
