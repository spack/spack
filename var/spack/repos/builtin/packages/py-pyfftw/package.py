# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyfftw(PythonPackage):
    """A pythonic wrapper around FFTW, the FFT library,
    presenting a unified interface for all the supported transforms."""

    homepage = "http://hgomersall.github.com/pyFFTW"
    url      = "https://pypi.io/packages/source/p/pyFFTW/pyFFTW-0.10.4.tar.gz"

    version('0.10.4', '7fb59450308881bb48d9f178947d950e')

    depends_on('fftw')
    depends_on('py-setuptools',    type='build')
    depends_on('py-cython',        type='build')
    depends_on('py-numpy@1.6:',    type=('build', 'run'))
    depends_on('py-scipy@0.12.0:', type=('build', 'run'))
