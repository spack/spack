# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPywavelets(PythonPackage):
    """PyWavelets is a free Open Source library for wavelet transforms
       in Python"""

    homepage = "https://github.com/PyWavelets"
    url = "https://pypi.io/packages/source/P/PyWavelets/PyWavelets-0.5.2.tar.gz"

    version('0.5.2', sha256='ce36e2f0648ea1781490b09515363f1f64446b0eac524603e5db5e180113bed9')

    import_modules = ['pywt', 'pywt.data']

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy@1.9.1:',  type=('build', 'run'))
