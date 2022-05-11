# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyPythonFmask(PythonPackage):
    """A set of command line utilities and Python modules that implement
       the FMASK algorithm for Landsat and Sentinel-2"""

    homepage = "https://www.pythonfmask.org/en/latest/"
    url      = "https://github.com/ubarsc/python-fmask/archive/pythonfmask-0.5.4.tar.gz"

    version('0.5.4', sha256='a216aa3108de837fec182602b2b4708442746be31fc1585906802437784a63fe')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')
    depends_on('py-rios',       type=('build', 'run'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))
    depends_on('gdal+python',   type=('build', 'run'))
