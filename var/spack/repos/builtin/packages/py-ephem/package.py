# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEphem(PythonPackage):
    """PyEphem provides an ephem Python package for
    performing high-precision astronomy computations."""

    homepage = "https://rhodesmill.org/pyephem/"
    url      = "https://pypi.python.org/packages/source/e/ephem/ephem-3.7.6.0.tar.gz"

    version('3.7.6.0', sha256='7a4c82b1def2893e02aec0394f108d24adb17bd7b0ca6f4bc78eb7120c0212ac')

    variant('docs', default=False, description='build documentation')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # Prevent passing --single-version-externally-managed to
    # setup.py, which it does not support.
    # code copied from scons/package.py
    def install_args(self, spec, prefix):
        return ['--prefix={0}'.format(prefix), '--root=/']
