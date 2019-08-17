# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWcsaxes(PythonPackage):
    """WCSAxes is a framework for making plots of Astronomical data
    in Matplotlib."""

    homepage = "http://wcsaxes.readthedocs.io/en/latest/index.html"
    url      = "https://github.com/astrofrog/wcsaxes/archive/v0.8.tar.gz"

    version('0.8', 'de1c60fdae4c330bf5ddb9f1ab5ab920')

    extends('python', ignore=r'bin/')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))
